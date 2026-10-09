#!/usr/bin/env python3
"""Build one default-deny PayGuard public source candidate outside the source root."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile

try:
    from validate_public_candidate import (
        DETACHED_NAME,
        LOCAL_EXPORT_STATUS,
        LOCAL_REMAINING_GATES,
        MANIFEST_NAME,
        PACKAGE_DIGEST_ALGORITHM,
        PUBLISHED_REMAINING_GATES,
        PUBLISHED_SOURCE_STATUS,
        validate_candidate,
    )
except ModuleNotFoundError:
    from tools.validate_public_candidate import (
        DETACHED_NAME,
        LOCAL_EXPORT_STATUS,
        LOCAL_REMAINING_GATES,
        MANIFEST_NAME,
        PACKAGE_DIGEST_ALGORITHM,
        PUBLISHED_REMAINING_GATES,
        PUBLISHED_SOURCE_STATUS,
        validate_candidate,
    )


PROJECT_ROOT = Path(__file__).absolute().parents[1]
MAX_FILE_BYTES = 2_000_000
ROOT_FILES = (
    ".gitignore",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "pyproject.toml",
    "requirements.lock",
)
EXACT_FILES = (
    "backend/SECURITY.md",
    "data/knowledge/payguard_us_official_v2/chunks.jsonl",
    "data/knowledge/payguard_us_official_v2/scenario_cards.v1.json",
    "data/knowledge/payguard_us_official_v2/sources.json",
    "docs/decisions/2026Q4/architecture.md",
    "docs/decisions/2026Q4/case_intake_contract.md",
    "docs/decisions/2026Q4/console_contract.md",
    "docs/decisions/2026Q4/payguard_us_architecture_status.svg",
    "docs/decisions/2026Q4/policy_engine_v1.md",
    "docs/decisions/2026Q4/threat_model.md",
    "docs/decisions/2026Q4/us_mainline_contract.md",
    "docs/decisions/2026Q4/us_official_source_register.md",
    "docs/submission/quickstart.md",
    "docs/submission/video_script.md",
    "frontend/index.html",
    "frontend/package-lock.json",
    "frontend/package.json",
    "frontend/vite.config.js",
    "integrations/gemini/check_runtime.py",
    "integrations/gemini/pyproject.toml",
    "integrations/gemini/requirements.lock",
    "integrations/gemini/run.sh",
    "integrations/gemini/test_worker.py",
    "integrations/gemini/worker.py",
    "policies/US/paypal_aup_reference_v1/manifest.json",
    "policies/US/paypal_aup_reference_v1/source_index.json",
    "policies/registry.json",
    "tests/frontend_ai_contract.mjs",
    "tests/frontend_operator_labels.mjs",
    "tests/frontend_recording_contract.mjs",
    "tests/frontend_zip_api_parity.mjs",
    "tests/frontend_zip_contract.mjs",
    "tools/build_public_candidate.py",
    "tools/public_run.sh",
    "tools/validate_public_candidate.py",
)
TREE_FILES = {
    "backend/app": (
        "__init__.py", "ai_brief.py", "lmstudio_brief.py", "main.py", "paypal.py",
        "paypal_tools.py", "schemas.py", "store.py",
    ),
    "frontend/src": (
        "AnalyticsDashboard.css", "AnalyticsDashboard.jsx", "App.jsx", "PolicyPanel.jsx",
        "ReferencePanel.jsx", "api.js", "index.css", "main.jsx", "operatorLabels.js",
        "pseudonymizedExport.js", "referenceContract.js", "reviewZip.js",
    ),
    "src/payguard": (
        "__init__.py", "advisory_eval.py", "applicability.py", "case_cards.py",
        "case_contract.py", "case_intake.py", "cli.py", "dispute_evidence.py",
        "document_privacy.py", "engines.py", "ingest.py", "policy.py", "privacy.py",
        "reference_policy.py", "reporting.py", "retrieval.py", "review.py",
    ),
    "tests": (
        "test_advisory_eval.py", "test_ai_api.py", "test_ai_brief.py", "test_api.py",
        "test_applicability.py", "test_boundaries.py", "test_case_cards.py",
        "test_case_intake.py", "test_dispute_evidence.py", "test_document_privacy.py",
        "test_engines.py", "test_gemini_worker.py", "test_lmstudio_brief.py",
        "test_paypal_tools.py", "test_policy_api.py", "test_policy_gateway_integration.py",
        "test_public_export_builder.py", "test_reference_api.py", "test_reference_policy.py",
        "test_retrieval.py", "test_sandbox_receipts.py",
    ),
}
MAPPED_FILES = {"tools/run.sh": "tools/public_run.sh"}
EXECUTABLE_PATHS = {
    "integrations/gemini/run.sh",
    "tools/public_run.sh",
    "tools/run.sh",
}
REQUIRED_RELEASE_UNIT_FILES = frozenset({
    "frontend/src/operatorLabels.js",
    "tests/frontend_operator_labels.mjs",
    "tests/frontend_recording_contract.mjs",
})


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def source_paths() -> tuple[str, ...]:
    paths = set(ROOT_FILES) | set(EXACT_FILES)
    for directory, names in TREE_FILES.items():
        paths.update(f"{directory}/{name}" for name in names)
    if any(path.startswith("integrations/paypal_toolkit/") for path in paths):
        raise RuntimeError("SOURCE_TOOLKIT_PROFILE_EXCLUDED")
    if len(paths) != sum(len(group) for group in (ROOT_FILES, EXACT_FILES)) + sum(len(names) for names in TREE_FILES.values()):
        raise RuntimeError("SOURCE_ALLOWLIST_DUPLICATE")
    missing_release_units = sorted(REQUIRED_RELEASE_UNIT_FILES - paths)
    if missing_release_units:
        raise RuntimeError(f"SOURCE_RELEASE_UNIT_MISSING:{','.join(missing_release_units)}")
    return tuple(sorted(paths))


def read_source(relative: str) -> tuple[bytes, int]:
    parts = Path(relative).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise RuntimeError(f"SOURCE_BOUNDARY_REJECTED:{relative}")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None or os.open not in os.supports_dir_fd:
        raise RuntimeError("SOURCE_NOFOLLOW_UNAVAILABLE")
    directory_flags = os.O_RDONLY | directory | nofollow | getattr(os, "O_CLOEXEC", 0)
    file_flags = os.O_RDONLY | nofollow | getattr(os, "O_CLOEXEC", 0)
    descriptors: list[int] = []
    try:
        root_fd = os.open(PROJECT_ROOT, directory_flags)
        descriptors.append(root_fd)
        parent_fd = root_fd
        for part in parts[:-1]:
            parent_fd = os.open(part, directory_flags, dir_fd=parent_fd)
            descriptors.append(parent_fd)
        file_fd = os.open(parts[-1], file_flags, dir_fd=parent_fd)
        descriptors.append(file_fd)
        before = os.fstat(file_fd)
        if not stat.S_ISREG(before.st_mode):
            raise RuntimeError(f"SOURCE_BOUNDARY_REJECTED:{relative}")
        if before.st_size > MAX_FILE_BYTES:
            raise RuntimeError(f"SOURCE_SIZE_REJECTED:{relative}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(file_fd, min(65_536, MAX_FILE_BYTES + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise RuntimeError(f"SOURCE_SIZE_REJECTED:{relative}")
        after = os.fstat(file_fd)
        identity_before = (
            before.st_dev, before.st_ino, before.st_mode, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        )
        identity_after = (
            after.st_dev, after.st_ino, after.st_mode, after.st_size,
            after.st_mtime_ns, after.st_ctime_ns,
        )
        payload = b"".join(chunks)
        if identity_before != identity_after or len(payload) != before.st_size:
            raise RuntimeError(f"SOURCE_READ_DRIFT:{relative}")
        return payload, stat.S_IMODE(before.st_mode)
    except RuntimeError:
        raise
    except OSError:
        raise RuntimeError(f"SOURCE_BOUNDARY_REJECTED:{relative}") from None
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def write_candidate_file(root: Path, relative: str, payload: bytes, mode: int) -> None:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    target.chmod(0o755 if relative in EXECUTABLE_PATHS else mode & 0o666 or 0o644)


def package_digest(rows: list[dict]) -> str:
    payload = "".join(f"{row['sha256']}  {row['path']}\n" for row in sorted(rows, key=lambda item: item["path"])).encode("utf-8")
    return sha256_bytes(payload)


def build_candidate(destination: Path, *, published_source: bool = False) -> dict:
    if not isinstance(published_source, bool):
        raise RuntimeError("RELEASE_MODE_INVALID")
    source_root = PROJECT_ROOT.resolve()
    destination = destination.absolute()
    resolved_parent = destination.parent.resolve()
    projected = resolved_parent / destination.name
    if source_root == projected or source_root in projected.parents or projected in source_root.parents:
        raise RuntimeError("DESTINATION_MUST_BE_OUTSIDE_SOURCE_ROOT")
    if destination.exists() or destination.is_symlink():
        raise RuntimeError("DESTINATION_ALREADY_EXISTS")
    resolved_parent.mkdir(parents=True, exist_ok=True)

    snapshots: dict[str, tuple[bytes, int]] = {}
    for relative in source_paths():
        snapshots[relative] = read_source(relative)

    with tempfile.TemporaryDirectory(prefix=f".{destination.name}-building-", dir=resolved_parent) as temporary:
        staging = Path(temporary) / "candidate"
        staging.mkdir()
        rows: list[dict] = []
        for relative in source_paths():
            payload, mode = snapshots[relative]
            write_candidate_file(staging, relative, payload, mode)
            rows.append({
                "path": relative,
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "source_path": relative,
                "source_sha256": sha256_bytes(payload),
            })
        for candidate_path, source_path in MAPPED_FILES.items():
            payload, mode = snapshots[source_path]
            write_candidate_file(staging, candidate_path, payload, mode)
            rows.append({
                "path": candidate_path,
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "source_path": source_path,
                "source_sha256": sha256_bytes(payload),
            })

        rows.sort(key=lambda item: item["path"])
        digest = package_digest(rows)
        row_map = {row["path"]: row for row in rows}
        dependency_locks = {
            "root_python": row_map["requirements.lock"]["sha256"],
            "gemini_python": row_map["integrations/gemini/requirements.lock"]["sha256"],
            "frontend_npm": row_map["frontend/package-lock.json"]["sha256"],
        }
        release_status = PUBLISHED_SOURCE_STATUS if published_source else LOCAL_EXPORT_STATUS
        remaining_gates = PUBLISHED_REMAINING_GATES if published_source else LOCAL_REMAINING_GATES
        manifest = {
            "schema_version": "payguard.public_export.v2",
            "status": release_status,
            "publication_authorized": published_source,
            "public_artifact_id": f"payguard-public-source-{digest[:16]}",
            "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "package_digest_algorithm": PACKAGE_DIGEST_ALGORITHM,
            "package_digest_sha256": digest,
            "file_count": len(rows),
            "files": rows,
            "dependency_locks": dependency_locks,
            "owner_attestation": {
                "accepted": True,
                "scope": "RECORDED_OWNER_RIGHTS_AND_ENTRANT_ELIGIBILITY",
            },
            "raw_bounded_prompt_disclosure": {
                "intent": "INTENTIONAL_PUBLIC_EXECUTABLE_PRODUCT_SOURCE",
                "path": "backend/app/ai_brief.py",
                "sha256": row_map["backend/app/ai_brief.py"]["sha256"],
            },
            "remaining_gates": list(remaining_gates),
        }
        manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
        manifest_hash = sha256_bytes(manifest_bytes)
        write_candidate_file(staging, MANIFEST_NAME, manifest_bytes, 0o644)
        write_candidate_file(staging, DETACHED_NAME, f"{manifest_hash}  {MANIFEST_NAME}\n".encode("ascii"), 0o644)

        for relative, (payload, _mode) in snapshots.items():
            if read_source(relative)[0] != payload:
                raise RuntimeError(f"SOURCE_DRIFT:{relative}")

        result = validate_candidate(staging)
        staging.rename(destination)
        return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--published-source",
        action="store_true",
        help="record an already completed public-source publication transition",
    )
    parser.add_argument("destination", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = build_candidate(args.destination, published_source=args.published_source)
    except (OSError, RuntimeError, ValueError) as error:
        print(json.dumps({"status": "FAILED", "reason": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
