#!/usr/bin/env python3
"""Validate one immutable PayGuard public source candidate without network access."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from urllib.parse import unquote, urlsplit


MANIFEST_NAME = "public_export_manifest.json"
DETACHED_NAME = "public_export_manifest.sha256"
CONTROL_FILES = {MANIFEST_NAME, DETACHED_NAME}
MAX_FILE_BYTES = 2_000_000
PACKAGE_DIGEST_ALGORITHM = "sha256(sorted utf-8 '<file_sha256>  <relative_path>\\n' records; manifest and detached hash excluded)"
LOCAL_EXPORT_STATUS = "LOCAL_EXPORT_CANDIDATE_REVIEW_REQUIRED"
PUBLISHED_SOURCE_STATUS = "PUBLIC_SOURCE_PUBLISHED"
LOCAL_REMAINING_GATES = (
    "EXACT_FINAL_BYTES_SECURITY_REVIEW",
    "INDEPENDENT_RED_TEAM_ACCEPTANCE",
    "REPOSITORY_VISIBILITY",
    "DEVPOST_SUBMISSION",
)
PUBLISHED_REMAINING_GATES = (
    "DEVPOST_SUBMISSION",
)
PUBLISHED_CURRENT_STATE = (
    "public source publication is complete",
    "only devpost submission remains in the competition submission path",
)
PUBLISHED_RELEASE_ASSETS = {
    "SECURITY.md": (
        "public export, owner-rights and deploy approval remain open",
    ),
    "docs/decisions/2026Q4/architecture.md": (
        "pending: external receipt binding",
        "public export, deployment and independent release acceptance remain open",
        "third-party notices and public artifact proof remain open",
        "repository publication, video and submission remain frozen",
        "security, repository-visibility, video and devpost evidence remain required",
        "production, provider mutations, public release",
    ),
    "docs/decisions/2026Q4/us_mainline_contract.md": (
        "security, rights, export, repository-visibility, video and submission gates",
        "public repository, video or devpost submission readiness",
    ),
    "docs/decisions/2026Q4/payguard_us_architecture_status.svg": (
        "frozen public release",
        "public not ready",
    ),
}
FORBIDDEN_PARTS = {
    ".cache", ".codex", ".cursor", ".git", ".github", ".pytest_cache", ".venv",
    ".vscode", "__pycache__", "archive", "build", "dist", "logs", "node_modules",
    "output", "rollback",
}
FORBIDDEN_NAMES = {
    ".mcp.json", "credentials.json", "service-account.json", "service_account.json",
}
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".jsonl", ".jsx", ".lock", ".md", ".py", ".sh", ".svg", ".toml", ".txt"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HAN_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
MAPPED_SOURCE_PATHS = {"tools/run.sh": "tools/public_run.sh"}


class CandidateRejected(ValueError):
    """A public-candidate invariant failed."""


def reject(code: str) -> None:
    raise CandidateRejected(code)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def safe_relative(value: str) -> bool:
    path = Path(value)
    return bool(path.parts) and not path.is_absolute() and all(part not in {"", ".", ".."} for part in path.parts)


def forbidden_relative(value: str) -> bool:
    path = Path(value)
    return (
        not safe_relative(value)
        or any(part in FORBIDDEN_PARTS for part in path.parts)
        or path.name in FORBIDDEN_NAMES
        or path.name == ".env"
        or path.name.startswith(".env.")
        or path.suffix in {".pyc", ".pyo"}
    )


def strict_json_bytes(payload: bytes) -> dict:
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                reject("JSON_DUPLICATE_KEY")
            result[key] = value
        return result

    try:
        result = json.loads(payload, object_pairs_hook=unique)
    except CandidateRejected:
        raise
    except (UnicodeError, ValueError, RecursionError):
        reject("JSON_MALFORMED")
    if not isinstance(result, dict):
        reject("JSON_OBJECT_REQUIRED")
    return result


def regular_files(root: Path) -> dict[str, Path]:
    if root.is_symlink() or not root.is_dir():
        reject("CANDIDATE_ROOT_INVALID")
    files: dict[str, Path] = {}
    for directory, names, filenames in os.walk(root, followlinks=False):
        current = Path(directory)
        for name in names:
            path = current / name
            if path.is_symlink():
                reject("CANDIDATE_SYMLINK_REJECTED")
        for name in filenames:
            path = current / name
            relative = path.relative_to(root).as_posix()
            try:
                info = path.lstat()
            except OSError:
                reject("CANDIDATE_FILE_UNREADABLE")
            if path.is_symlink():
                reject("CANDIDATE_SYMLINK_REJECTED")
            if not stat.S_ISREG(info.st_mode):
                reject("CANDIDATE_SPECIAL_FILE_REJECTED")
            if forbidden_relative(relative):
                reject("CANDIDATE_FORBIDDEN_PATH")
            if info.st_size > MAX_FILE_BYTES:
                reject("CANDIDATE_FILE_TOO_LARGE")
            if relative in files:
                reject("CANDIDATE_DUPLICATE_PATH")
            files[relative] = path
    return files


def package_digest(rows: dict[str, dict]) -> str:
    payload = "".join(f"{rows[path]['sha256']}  {path}\n" for path in sorted(rows)).encode("utf-8")
    return sha256_bytes(payload)


def validate_manifest(root: Path, files: dict[str, Path]) -> tuple[dict, dict[str, dict], str]:
    if not CONTROL_FILES <= set(files):
        reject("MANIFEST_CONTROL_MISSING")
    manifest_bytes = files[MANIFEST_NAME].read_bytes()
    manifest_hash = sha256_bytes(manifest_bytes)
    expected_detached = f"{manifest_hash}  {MANIFEST_NAME}\n".encode("ascii")
    if files[DETACHED_NAME].read_bytes() != expected_detached:
        reject("DETACHED_MANIFEST_HASH_MISMATCH")
    manifest = strict_json_bytes(manifest_bytes)
    required = {
        "schema_version", "status", "publication_authorized", "public_artifact_id",
        "created_at_utc", "package_digest_algorithm", "package_digest_sha256",
        "file_count", "files", "dependency_locks", "owner_attestation",
        "raw_bounded_prompt_disclosure", "remaining_gates",
    }
    if set(manifest) != required:
        reject("MANIFEST_SCHEMA_MISMATCH")
    if manifest["schema_version"] != "payguard.public_export.v2":
        reject("MANIFEST_SCHEMA_MISMATCH")
    release_contracts = {
        LOCAL_EXPORT_STATUS: (False, LOCAL_REMAINING_GATES),
        PUBLISHED_SOURCE_STATUS: (True, PUBLISHED_REMAINING_GATES),
    }
    if not isinstance(manifest["status"], str):
        reject("MANIFEST_STATUS_INVALID")
    release_contract = release_contracts.get(manifest["status"])
    if release_contract is None:
        reject("MANIFEST_STATUS_INVALID")
    expected_authorized, expected_gates = release_contract
    if (
        manifest["publication_authorized"] is not expected_authorized
        or manifest["remaining_gates"] != list(expected_gates)
    ):
        reject("MANIFEST_RELEASE_STATE_INVALID")
    if not re.fullmatch(r"payguard-public-source-[a-f0-9]{16}", manifest["public_artifact_id"] or ""):
        reject("MANIFEST_PUBLIC_ID_INVALID")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", manifest["created_at_utc"] or ""):
        reject("MANIFEST_UTC_INVALID")
    if manifest["package_digest_algorithm"] != PACKAGE_DIGEST_ALGORITHM:
        reject("PACKAGE_DIGEST_ALGORITHM_INVALID")
    raw_rows = manifest["files"]
    if not isinstance(raw_rows, list) or not raw_rows:
        reject("MANIFEST_FILES_INVALID")
    rows: dict[str, dict] = {}
    for row in raw_rows:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256", "source_path", "source_sha256"}:
            reject("MANIFEST_ROW_INVALID")
        relative = row.get("path")
        source_path = row.get("source_path")
        if not isinstance(relative, str) or forbidden_relative(relative) or relative in CONTROL_FILES or relative in rows:
            reject("MANIFEST_PATH_INVALID")
        if not isinstance(source_path, str) or forbidden_relative(source_path):
            reject("MANIFEST_SOURCE_PATH_INVALID")
        expected_source_path = MAPPED_SOURCE_PATHS.get(relative, relative)
        if source_path != expected_source_path:
            reject("MANIFEST_SOURCE_PATH_MISMATCH")
        path = files.get(relative)
        if path is None:
            reject("MANIFEST_FILE_MISSING")
        payload = path.read_bytes()
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256_bytes(payload):
            reject("MANIFEST_FILE_HASH_MISMATCH")
        if not re.fullmatch(r"[a-f0-9]{64}", row.get("source_sha256") or ""):
            reject("MANIFEST_SOURCE_HASH_INVALID")
        if row["source_sha256"] != row["sha256"]:
            reject("MANIFEST_SOURCE_HASH_MISMATCH")
        rows[relative] = row
    if set(files) != set(rows) | CONTROL_FILES:
        reject("MANIFEST_UNLISTED_FILE")
    if manifest["file_count"] != len(rows):
        reject("MANIFEST_FILE_COUNT_MISMATCH")
    for mapped_path, source_path in MAPPED_SOURCE_PATHS.items():
        mapped = rows.get(mapped_path)
        source = rows.get(source_path)
        if (
            mapped is None
            or source is None
            or mapped["source_path"] != source_path
            or mapped["source_sha256"] != source["sha256"]
            or mapped["sha256"] != source["sha256"]
            or mapped["bytes"] != source["bytes"]
        ):
            reject("MANIFEST_MAPPED_SOURCE_MISMATCH")
    digest = package_digest(rows)
    if manifest["package_digest_sha256"] != digest:
        reject("PACKAGE_DIGEST_MISMATCH")
    expected_id = f"payguard-public-source-{digest[:16]}"
    if manifest["public_artifact_id"] != expected_id:
        reject("MANIFEST_PUBLIC_ID_INVALID")
    owner = manifest["owner_attestation"]
    if owner != {"accepted": True, "scope": "RECORDED_OWNER_RIGHTS_AND_ENTRANT_ELIGIBILITY"}:
        reject("MANIFEST_OWNER_ATTESTATION_INVALID")
    return manifest, rows, manifest_hash


def validate_runner(root: Path, rows: dict[str, dict]) -> None:
    public_path = "tools/public_run.sh"
    entry_path = "tools/run.sh"
    if public_path not in rows or entry_path not in rows:
        reject("PUBLIC_RUNNER_MISSING")
    if rows[public_path]["sha256"] != rows[entry_path]["sha256"]:
        reject("PUBLIC_RUNNER_DIGEST_MISMATCH")
    if (root / public_path).read_bytes() != (root / entry_path).read_bytes():
        reject("PUBLIC_RUNNER_BYTES_MISMATCH")
    if not os.access(root / public_path, os.X_OK) or not os.access(root / entry_path, os.X_OK):
        reject("PUBLIC_RUNNER_NOT_EXECUTABLE")
    text = (root / public_path).read_text(encoding="utf-8")
    for forbidden in ("audit)", "verify)", "readiness)", "package-check)"):
        if forbidden in text:
            reject("PUBLIC_RUNNER_INTERNAL_COMMAND_EXPOSED")


def validate_toolkit(root: Path, rows: dict[str, dict]) -> None:
    """The optional private SDK profile is excluded from the public package."""
    if any(path.startswith("integrations/paypal_toolkit/") for path in rows):
        reject("PUBLIC_TOOLKIT_PROFILE_EXCLUDED")


def markdown_targets(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        reject("MARKDOWN_INVALID")
    return [match.group(1).strip() for match in MARKDOWN_LINK.finditer(text)]


def validate_links(root: Path, rows: dict[str, dict]) -> int:
    count = 0
    for relative in sorted(rows):
        if not relative.endswith(".md"):
            continue
        source = root / relative
        for raw_target in markdown_targets(source):
            target = raw_target
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = target.split()[0]
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or target.startswith("#"):
                continue
            decoded = unquote(parsed.path)
            if not decoded:
                continue
            if decoded.startswith("/"):
                reject("MARKDOWN_ABSOLUTE_LINK_REJECTED")
            candidate = (source.parent / decoded).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                reject("MARKDOWN_LINK_ESCAPE")
            if not candidate.exists():
                reject("MARKDOWN_LINK_MISSING")
            count += 1
    return count


def validate_public_text(root: Path, rows: dict[str, dict]) -> None:
    private_temp = "/private" + "/tmp"
    private_user = "/" + "Users/"
    private_home = "/" + "home/"
    region_tokens = tuple(token.casefold() for token in ("Asia/" + "Tai" + "pei", "Tai" + "wan", "Tai" + "pei"))
    windows_drive = re.compile(r"(?i)(?<![a-z0-9])[a-z]:(?:/|" + re.escape("\\") + r")")
    windows_unc = re.compile(
        r"(?<![A-Za-z0-9._-])"
        + re.escape("\\\\")
        + r"[A-Za-z0-9][A-Za-z0-9._-]{0,252}[\\/][A-Za-z0-9$._-]+"
    )
    for relative in sorted(rows):
        path = root / relative
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"requirements.lock"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            reject("PUBLIC_TEXT_ENCODING_INVALID")
        if private_temp in text:
            reject("PORTABLE_TEMP_PATH_VIOLATION")
        if private_user in text or private_home in text or windows_drive.search(text) or windows_unc.search(text):
            reject("PRIVATE_ABSOLUTE_PATH_VIOLATION")
        folded = text.casefold()
        if any(token in folded for token in region_tokens) or HAN_PATTERN.search(text):
            reject("US_SCOPE_RESIDUE")


def validate_release_docs(root: Path, manifest: dict) -> None:
    if manifest["status"] != PUBLISHED_SOURCE_STATUS:
        return
    forbidden = (
        "publication is not authorized",
        "publication remains closed",
        "public release remains closed",
    )
    for relative in ("README.md", "docs/submission/quickstart.md"):
        try:
            folded = (root / relative).read_text(encoding="utf-8").casefold()
        except (OSError, UnicodeError):
            reject("PUBLISHED_RELEASE_DOC_INVALID")
        if any(phrase in folded for phrase in forbidden):
            reject("PUBLISHED_RELEASE_DOC_INVALID")
        if "complete repository run instructions" not in folded:
            reject("PUBLISHED_RELEASE_DOC_INVALID")
        if "hosted demo" not in folded or "optional" not in folded or "unperformed" not in folded:
            reject("PUBLISHED_RELEASE_DOC_INVALID")
    for relative, contradictions in PUBLISHED_RELEASE_ASSETS.items():
        try:
            folded = (root / relative).read_text(encoding="utf-8").casefold()
        except (OSError, UnicodeError):
            reject("PUBLISHED_RELEASE_ASSET_INVALID")
        if any(statement not in folded for statement in PUBLISHED_CURRENT_STATE):
            reject("PUBLISHED_RELEASE_ASSET_INVALID")
        if any(contradiction in folded for contradiction in contradictions):
            reject("PUBLISHED_RELEASE_ASSET_INVALID")


def python_lock_tokens(path: Path) -> set[str]:
    tokens = set()
    pattern = re.compile(r"([a-z0-9][a-z0-9_.-]*)==([^\s\\]+)(?:\s+\\)?")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.fullmatch(line.strip())
        if match:
            tokens.add(f"{match.group(1)}=={match.group(2)}")
    if not tokens:
        reject("DEPENDENCY_LOCK_EMPTY")
    return tokens


def frontend_lock_tokens(path: Path) -> set[str]:
    document = strict_json_bytes(path.read_bytes())
    packages = document.get("packages")
    if not isinstance(packages, dict):
        reject("FRONTEND_LOCK_INVALID")
    tokens = set()
    for key, value in packages.items():
        if not key.startswith("node_modules/"):
            continue
        if not isinstance(value, dict) or not isinstance(value.get("version"), str) or not isinstance(value.get("license"), str):
            reject("FRONTEND_LICENSE_METADATA_MISSING")
        tokens.add(f"{key.removeprefix('node_modules/')}@{value['version']}")
    return tokens


def validate_notices(root: Path, manifest: dict, rows: dict[str, dict]) -> None:
    notice_path = root / "THIRD_PARTY_NOTICES.md"
    if "THIRD_PARTY_NOTICES.md" not in rows:
        reject("THIRD_PARTY_NOTICE_MISSING")
    notice = notice_path.read_text(encoding="utf-8")
    locks = {
        "root_python": "requirements.lock",
        "gemini_python": "integrations/gemini/requirements.lock",
        "frontend_npm": "frontend/package-lock.json",
    }
    expected_hashes = {name: rows[path]["sha256"] for name, path in locks.items()}
    if manifest["dependency_locks"] != expected_hashes:
        reject("DEPENDENCY_LOCK_HASH_MISMATCH")
    for digest in expected_hashes.values():
        if digest not in notice:
            reject("THIRD_PARTY_LOCK_IDENTITY_MISSING")
    tokens = set()
    for path in (locks["root_python"], locks["gemini_python"]):
        tokens.update(python_lock_tokens(root / path))
    tokens.update(frontend_lock_tokens(root / locks["frontend_npm"]))
    if any(f"`{token}`" not in notice for token in tokens):
        reject("THIRD_PARTY_DEPENDENCY_MISSING")


def validate_disclosure(manifest: dict, rows: dict[str, dict]) -> None:
    expected = {
        "intent": "INTENTIONAL_PUBLIC_EXECUTABLE_PRODUCT_SOURCE",
        "path": "backend/app/ai_brief.py",
        "sha256": rows.get("backend/app/ai_brief.py", {}).get("sha256"),
    }
    if manifest["raw_bounded_prompt_disclosure"] != expected or expected["sha256"] is None:
        reject("PROMPT_DISCLOSURE_INVALID")


def validate_candidate(root: Path) -> dict:
    try:
        original = root.lstat()
    except OSError:
        reject("CANDIDATE_ROOT_INVALID")
    if stat.S_ISLNK(original.st_mode) or not stat.S_ISDIR(original.st_mode):
        reject("CANDIDATE_ROOT_INVALID")
    try:
        resolved = root.resolve(strict=True)
    except OSError:
        reject("CANDIDATE_ROOT_INVALID")
    files = regular_files(resolved)
    manifest, rows, manifest_hash = validate_manifest(resolved, files)
    validate_runner(resolved, rows)
    validate_toolkit(resolved, rows)
    link_count = validate_links(resolved, rows)
    validate_public_text(resolved, rows)
    validate_release_docs(resolved, manifest)
    validate_notices(resolved, manifest, rows)
    validate_disclosure(manifest, rows)
    return {
        "status": "PASS",
        "public_artifact_id": manifest["public_artifact_id"],
        "file_count": len(rows),
        "relative_links_checked": link_count,
        "manifest_sha256": manifest_hash,
        "package_digest_sha256": manifest["package_digest_sha256"],
        "release_status": manifest["status"],
        "publication_authorized": manifest["publication_authorized"],
    }


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1:
        print(json.dumps({"status": "FAILED", "reason": "ARGUMENTS_REJECTED"}, sort_keys=True))
        return 64
    root = Path(args[0]) if args else Path(__file__).absolute().parents[1]
    try:
        result = validate_candidate(root)
    except (CandidateRejected, OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"status": "FAILED", "reason": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
