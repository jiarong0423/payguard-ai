"""Fail-closed dependency and source guard for the Gemini Python 3.12 worker."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import sys
import tomllib


PINNED_DIRECT = {
    "google-auth": "2.60.0",
    "google-genai": "2.28.0",
    "pydantic": "2.13.5",
}
EXPECTED_LOCK_SHA256 = "36554331392d6102519a4ead5778704c4ff89e79da6bb9d6648b656f130724bb"
EXPECTED_INVENTORY_COUNT = 25
PROJECT_MARKERS = {
    'backend/app/ai_brief.py': '1e92524a14c2a722b603cca06bec0bacd0a1b80cc1cda5f85146cda97762dc92',
    'backend/app/main.py': 'dc24c4c91b15700d7f8aaf906438e01cdb0a17a003c9411e42269c8fba9d5f71',
    'backend/app/store.py': '1f2d4ba830b41ed443c2d22097825354224a9481a91768e1eb474d1d853fc91e',
    'integrations/gemini/run.sh': '6f276cb1cbe6905a5d04e8c107afb83487fd0898c2ab405da28fc8ee18979203',
    'integrations/gemini/worker.py': 'dcd627e0260bd61fc929cc930ede3ca32752e08148241d78ab4963773128f51e',
}
EXPECTED_PART_FIELDS = frozenset(
    {
        "audio_transcription",
        "code_execution_result",
        "executable_code",
        "file_data",
        "function_call",
        "function_response",
        "inline_data",
        "media_processing",
        "media_resolution",
        "part_metadata",
        "speech_metadata",
        "text",
        "thought",
        "thought_signature",
        "tool_call",
        "tool_response",
        "video_metadata",
    }
)


class RuntimeRejected(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def reject(code: str) -> None:
    raise RuntimeRejected(code)


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name.lower())


def parse_lock(raw: bytes) -> dict[str, str]:
    if type(raw) is not bytes or not 0 < len(raw) <= 2_000_000:
        reject("GEMINI_PROFILE_LOCK_INVALID")
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeError:
        reject("GEMINI_PROFILE_LOCK_INVALID")
    pins: dict[str, str] = {}
    hashes: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            reject("GEMINI_PROFILE_LOCK_INVALID")
        pin_line = line[:-2] if line.endswith(" \\") else ""
        pin = re.fullmatch(r"([a-z0-9][a-z0-9_.-]*)==([0-9][a-zA-Z0-9.!+_-]*)", pin_line)
        if pin:
            if current is not None and not hashes[current]:
                reject("GEMINI_PROFILE_LOCK_INVALID")
            current = normalize(pin[1])
            if current in pins:
                reject("GEMINI_PROFILE_LOCK_INVALID")
            pins[current] = pin[2]
            hashes[current] = []
            continue
        digest_line = line[:-2] if line.endswith(" \\") else line
        digest = re.fullmatch(r"    --hash=sha256:([a-f0-9]{64})", digest_line)
        if not digest or current is None or digest[1] in hashes[current]:
            reject("GEMINI_PROFILE_LOCK_INVALID")
        hashes[current].append(digest[1])
    if len(pins) != EXPECTED_INVENTORY_COUNT or any(not values for values in hashes.values()):
        reject("GEMINI_PROFILE_LOCK_INVALID")
    return pins


def validate_profile(profile: Path) -> dict[str, str]:
    try:
        raw = (profile / "requirements.lock").read_bytes()
        manifest = tomllib.loads((profile / "pyproject.toml").read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        reject("GEMINI_PROFILE_MANIFEST_INVALID")
    actual_hash = hashlib.sha256(raw).hexdigest()
    project = manifest.get("project", {})
    tool = manifest.get("tool", {}).get("payguard-gemini", {})
    if not isinstance(project, dict) or not isinstance(tool, dict):
        reject("GEMINI_PROFILE_MANIFEST_INVALID")
    if actual_hash != EXPECTED_LOCK_SHA256 or tool.get("lock-sha256") != actual_hash:
        reject("GEMINI_PROFILE_LOCK_HASH_INVALID")
    expected_dependencies = sorted(f"{name}=={version}" for name, version in PINNED_DIRECT.items())
    if project.get("requires-python") != "==3.12.*" or sorted(project.get("dependencies", [])) != expected_dependencies:
        reject("GEMINI_PROFILE_MANIFEST_INVALID")
    if tool.get("inventory-count") != EXPECTED_INVENTORY_COUNT:
        reject("GEMINI_PROFILE_MANIFEST_INVALID")
    if tool.get("api-version") != "v1" or tool.get("location") != "global":
        reject("GEMINI_PROFILE_MANIFEST_INVALID")
    if tool.get("model") != "gemini-3.8-flash" or tool.get("mode") != "fixed_synthetic_advisory_worker":
        reject("GEMINI_PROFILE_MANIFEST_INVALID")
    if tool.get("sdk-version") != PINNED_DIRECT["google-genai"]:
        reject("GEMINI_PROFILE_MANIFEST_INVALID")
    if tool.get("project-markers") != PROJECT_MARKERS:
        reject("GEMINI_PROFILE_MANIFEST_INVALID")
    pins = parse_lock(raw)
    if any(pins.get(name) != version for name, version in PINNED_DIRECT.items()):
        reject("GEMINI_PROFILE_MANIFEST_INVALID")
    return pins


def validate_inventory(pins: dict[str, str], distributions) -> None:
    installed: dict[str, str] = {}
    prefix = Path(sys.prefix).resolve()
    for distribution in distributions:
        name = distribution.metadata.get("Name")
        if not isinstance(name, str) or not name:
            reject("GEMINI_PROFILE_INVENTORY_INVALID")
        normalized = normalize(name)
        if normalized in installed:
            reject("GEMINI_PROFILE_INVENTORY_INVALID")
        try:
            location = Path(distribution.locate_file("")).resolve()
            location.relative_to(prefix)
        except (OSError, ValueError):
            reject("GEMINI_PROFILE_INVENTORY_INVALID")
        installed[normalized] = distribution.version
    if installed != pins:
        reject("GEMINI_PROFILE_INVENTORY_MISMATCH")


def validate_project(profile: Path) -> Path:
    root = profile.parent.parent
    try:
        for relative, digest in PROJECT_MARKERS.items():
            if hashlib.sha256((root / relative).read_bytes()).hexdigest() != digest:
                reject("GEMINI_PROFILE_PROJECT_MISMATCH")
    except OSError:
        reject("GEMINI_PROFILE_PROJECT_MISMATCH")
    return root


def validate_sdk_schema() -> None:
    try:
        from google.genai import types
        fields = frozenset(types.Part.model_fields)
    except Exception:
        reject("GEMINI_PROFILE_IMPORT_UNAVAILABLE")
    if fields != EXPECTED_PART_FIELDS:
        reject("GEMINI_PROFILE_SDK_SCHEMA_MISMATCH")


def check(profile: Path, *, version=None, distributions=None, schema_loader=None) -> dict[str, object]:
    version = sys.version_info if version is None else version
    if tuple(version[:2]) != (3, 12):
        reject("GEMINI_PROFILE_PYTHON_312_REQUIRED")
    pins = validate_profile(profile)
    validate_inventory(pins, importlib.metadata.distributions() if distributions is None else distributions)
    validate_project(profile)
    (validate_sdk_schema if schema_loader is None else schema_loader)()
    return {
        "api_version": "v1",
        "locked_distributions": EXPECTED_INVENTORY_COUNT,
        "location": "global",
        "model": "gemini-3.8-flash",
        "python": ".".join(str(item) for item in version[:3]),
        "sdk": "google-genai==2.28.0",
        "status": "GEMINI_PROFILE_READY",
    }


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        print("GEMINI_PROFILE_ARGUMENTS_REJECTED", file=sys.stderr)
        return 64
    try:
        result = check(Path(__file__).resolve().parent)
    except RuntimeRejected as failure:
        print(failure.code, file=sys.stderr)
        return 78
    except Exception:
        print("GEMINI_PROFILE_RUNTIME_UNAVAILABLE", file=sys.stderr)
        return 78
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
