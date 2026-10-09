"""Focused tests for the fail-closed and published-source export contracts."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

from tools import build_public_candidate as builder
from tools import validate_public_candidate as validator


class PublicExportBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="payguard-public-builder-tests-")
        cls.base = Path(cls.temporary.name) / "base-candidate"
        cls.result = builder.build_candidate(cls.base)
        cls.published = Path(cls.temporary.name) / "published-source"
        cls.published_result = builder.build_candidate(cls.published, published_source=True)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def copy_candidate(self, name, source=None):
        target = Path(self.temporary.name) / name
        shutil.copytree(source or self.base, target)
        target.chmod(target.stat().st_mode | 0o200)
        for path in target.rglob("*"):
            path.chmod(path.stat().st_mode | 0o200)
        return target

    def resign_manifest(self, root, manifest, *, rebuild_package=False):
        if rebuild_package:
            rows = {row["path"]: row for row in manifest["files"]}
            digest = validator.package_digest(rows)
            manifest["package_digest_sha256"] = digest
            manifest["public_artifact_id"] = f"payguard-public-source-{digest[:16]}"
        payload = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
        (root / validator.MANIFEST_NAME).write_bytes(payload)
        (root / validator.DETACHED_NAME).write_text(
            f"{validator.sha256_bytes(payload)}  {validator.MANIFEST_NAME}\n", encoding="ascii"
        )

    def test_fresh_candidate_passes_and_has_exact_public_boundary(self):
        result = validator.validate_candidate(self.base)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["release_status"], validator.LOCAL_EXPORT_STATUS)
        self.assertFalse(result["publication_authorized"])
        manifest = json.loads((self.base / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], validator.LOCAL_EXPORT_STATUS)
        self.assertFalse(manifest["publication_authorized"])
        self.assertEqual(manifest["remaining_gates"], list(validator.LOCAL_REMAINING_GATES))
        self.assertEqual((self.base / "tools/public_run.sh").read_bytes(), (self.base / "tools/run.sh").read_bytes())
        for relative in (
            "docs/submission/video_script.md",
            "frontend/src/operatorLabels.js",
            "THIRD_PARTY_NOTICES.md",
            "tests/frontend_operator_labels.mjs",
            "tests/frontend_recording_contract.mjs",
            "tests/test_public_export_builder.py",
        ):
            self.assertTrue((self.base / relative).is_file(), relative)
        for forbidden in (".venv", "__pycache__", "output", "logs", "archive", "rollback"):
            self.assertFalse(any(forbidden in path.parts for path in self.base.rglob("*")))

    def test_public_candidate_excludes_optional_sdk_profile_and_lock(self):
        manifest = json.loads((self.base / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
        self.assertFalse((self.base / "integrations/paypal_toolkit").exists())
        self.assertNotIn("paypal_toolkit_python", manifest["dependency_locks"])
        self.assertEqual(set(manifest["dependency_locks"]), {"root_python", "gemini_python", "frontend_npm"})
        with mock.patch.object(builder, "EXACT_FILES", builder.EXACT_FILES + ("integrations/paypal_toolkit/requirements.lock",)):
            with self.assertRaisesRegex(RuntimeError, "SOURCE_TOOLKIT_PROFILE_EXCLUDED"):
                builder.source_paths()

    def test_resigned_manifest_cannot_reintroduce_optional_sdk_profile(self):
        root = self.copy_candidate("reintroduced-toolkit")
        relative = "integrations/paypal_toolkit/requirements.lock"
        path = root / relative
        path.parent.mkdir(parents=True)
        payload = b"excluded-profile-test\n"
        path.write_bytes(payload)
        manifest = json.loads((root / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
        digest = validator.sha256_bytes(payload)
        manifest["files"].append({"path": relative, "bytes": len(payload), "sha256": digest,
                                  "source_path": relative, "source_sha256": digest})
        manifest["file_count"] += 1
        self.resign_manifest(root, manifest, rebuild_package=True)
        with self.assertRaisesRegex(validator.CandidateRejected, "PUBLIC_TOOLKIT_PROFILE_EXCLUDED"):
            validator.validate_candidate(root)

    def test_resigned_manifest_cannot_reintroduce_optional_sdk_lock_claim(self):
        root = self.copy_candidate("reintroduced-toolkit-lock-claim")
        manifest = json.loads((root / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
        manifest["dependency_locks"]["paypal_toolkit_python"] = "0" * 64
        self.resign_manifest(root, manifest)
        with self.assertRaisesRegex(validator.CandidateRejected, "DEPENDENCY_LOCK_HASH_MISMATCH"):
            validator.validate_candidate(root)

    def test_required_release_unit_allowlist_fails_closed(self):
        self.assertTrue(builder.REQUIRED_RELEASE_UNIT_FILES.issubset(set(builder.source_paths())))
        cases = (
            ("frontend/src/operatorLabels.js", "tree"),
            ("tests/frontend_operator_labels.mjs", "exact"),
            ("tests/frontend_recording_contract.mjs", "exact"),
        )
        for relative, source_group in cases:
            with self.subTest(relative=relative):
                if source_group == "tree":
                    tree_files = dict(builder.TREE_FILES)
                    tree_files["frontend/src"] = tuple(
                        name for name in tree_files["frontend/src"]
                        if f"frontend/src/{name}" != relative
                    )
                    patcher = mock.patch.object(builder, "TREE_FILES", tree_files)
                else:
                    exact_files = tuple(item for item in builder.EXACT_FILES if item != relative)
                    patcher = mock.patch.object(builder, "EXACT_FILES", exact_files)
                with patcher:
                    with self.assertRaises(RuntimeError) as captured:
                        builder.source_paths()
                self.assertEqual(
                    str(captured.exception),
                    f"SOURCE_RELEASE_UNIT_MISSING:{relative}",
                )

    def test_frontend_contract_entrypoints_are_public_and_documented(self):
        commands = (
            "node tests/frontend_ai_contract.mjs",
            "node tests/frontend_operator_labels.mjs",
            "node tests/frontend_recording_contract.mjs",
            "node tests/frontend_zip_contract.mjs",
            "node tests/frontend_zip_api_parity.mjs",
        )
        source_paths = set(builder.source_paths())
        for command in commands:
            self.assertIn(command.removeprefix("node "), source_paths)
        for relative in ("README.md", "docs/submission/quickstart.md"):
            with self.subTest(relative=relative):
                text = (self.published / relative).read_text(encoding="utf-8")
                for command in commands:
                    self.assertIn(command, text)

    def test_published_source_mode_has_exact_release_state_and_docs(self):
        result = validator.validate_candidate(self.published)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["release_status"], validator.PUBLISHED_SOURCE_STATUS)
        self.assertTrue(result["publication_authorized"])
        manifest = json.loads((self.published / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], validator.PUBLISHED_SOURCE_STATUS)
        self.assertTrue(manifest["publication_authorized"])
        self.assertEqual(manifest["remaining_gates"], list(validator.PUBLISHED_REMAINING_GATES))
        for relative in ("README.md", "docs/submission/quickstart.md"):
            text = (self.published / relative).read_text(encoding="utf-8").casefold()
            self.assertIn("complete repository run instructions", text)
            self.assertIn("hosted demo", text)
            self.assertIn("optional", text)
            self.assertIn("unperformed", text)
            self.assertNotIn("publication is not authorized", text)
            self.assertNotIn("publication remains closed", text)
            self.assertNotIn("public release remains closed", text)
        for relative, contradictions in validator.PUBLISHED_RELEASE_ASSETS.items():
            text = (self.published / relative).read_text(encoding="utf-8").casefold()
            for statement in validator.PUBLISHED_CURRENT_STATE:
                self.assertIn(statement, text)
            for contradiction in contradictions:
                self.assertNotIn(contradiction, text)

    def test_public_run_docs_keep_optional_profiles_and_attested_evidence_explicit(self):
        for relative in ("README.md", "docs/submission/quickstart.md"):
            with self.subTest(relative=relative):
                text = (self.published / relative).read_text(encoding="utf-8").casefold()
                self.assertIn("gemini profile is optional", text)
                self.assertIn("wsl 2", text)
                self.assertIn("operator-attested", text)
                self.assertNotIn("sandbox path proves", text)
        security = (self.published / "SECURITY.md").read_text(encoding="utf-8").casefold()
        self.assertIn("trust_env=false", security)
        video = (self.published / "docs/submission/video_script.md").read_text(encoding="utf-8").casefold()
        self.assertIn(
            "requires the separately authorized paypal sandbox and bounded ai paths "
            "to be available during recording",
            video,
        )
        self.assertIn(
            "do not replace live execution with a prior result or operator-attested text",
            video,
        )
        self.assertNotIn("sandbox path proves", video)

    def test_release_state_mismatches_fail_closed(self):
        cases = (
            (
                "local-with-published-status",
                self.base,
                validator.PUBLISHED_SOURCE_STATUS,
                False,
                validator.LOCAL_REMAINING_GATES,
            ),
            (
                "local-with-authorization",
                self.base,
                validator.LOCAL_EXPORT_STATUS,
                True,
                validator.LOCAL_REMAINING_GATES,
            ),
            (
                "local-with-published-gates",
                self.base,
                validator.LOCAL_EXPORT_STATUS,
                False,
                validator.PUBLISHED_REMAINING_GATES,
            ),
            (
                "published-with-local-status",
                self.published,
                validator.LOCAL_EXPORT_STATUS,
                True,
                validator.PUBLISHED_REMAINING_GATES,
            ),
            (
                "published-without-authorization",
                self.published,
                validator.PUBLISHED_SOURCE_STATUS,
                False,
                validator.PUBLISHED_REMAINING_GATES,
            ),
            (
                "published-with-local-gates",
                self.published,
                validator.PUBLISHED_SOURCE_STATUS,
                True,
                validator.LOCAL_REMAINING_GATES,
            ),
        )
        for name, source, status, authorized, gates in cases:
            with self.subTest(name=name):
                candidate = self.copy_candidate(name, source)
                manifest = json.loads((candidate / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
                manifest["status"] = status
                manifest["publication_authorized"] = authorized
                manifest["remaining_gates"] = list(gates)
                self.resign_manifest(candidate, manifest)
                with self.assertRaisesRegex(validator.CandidateRejected, "MANIFEST_RELEASE_STATE_INVALID"):
                    validator.validate_candidate(candidate)

    def test_published_source_docs_reject_closed_publication_claim(self):
        candidate = self.copy_candidate("published-doc-closed", self.published)
        path = candidate / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nPublication is not authorized.\n", encoding="utf-8")
        manifest = json.loads((candidate / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
        row = next(item for item in manifest["files"] if item["path"] == "README.md")
        payload = path.read_bytes()
        row["bytes"] = len(payload)
        row["sha256"] = validator.sha256_bytes(payload)
        row["source_sha256"] = row["sha256"]
        self.resign_manifest(candidate, manifest, rebuild_package=True)
        with self.assertRaisesRegex(validator.CandidateRejected, "PUBLISHED_RELEASE_DOC_INVALID"):
            validator.validate_candidate(candidate)

    def test_published_source_assets_reject_stale_current_state_claims(self):
        self.assertEqual(sum(len(items) for items in validator.PUBLISHED_RELEASE_ASSETS.values()), 11)
        for relative, contradictions in validator.PUBLISHED_RELEASE_ASSETS.items():
            for index, contradiction in enumerate(contradictions):
                with self.subTest(relative=relative, contradiction=contradiction):
                    candidate = self.copy_candidate(
                        f"published-stale-{Path(relative).stem}-{index}", self.published
                    )
                    path = candidate / relative
                    path.write_text(path.read_text(encoding="utf-8") + "\n" + contradiction + "\n", encoding="utf-8")
                    manifest = json.loads((candidate / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
                    row = next(item for item in manifest["files"] if item["path"] == relative)
                    payload = path.read_bytes()
                    row["bytes"] = len(payload)
                    row["sha256"] = validator.sha256_bytes(payload)
                    row["source_sha256"] = row["sha256"]
                    self.resign_manifest(candidate, manifest, rebuild_package=True)
                    with self.assertRaisesRegex(validator.CandidateRejected, "PUBLISHED_RELEASE_ASSET_INVALID"):
                        validator.validate_candidate(candidate)

    def test_manifest_and_unlisted_tamper_fail_closed(self):
        tampered = self.copy_candidate("tampered")
        (tampered / "README.md").write_bytes((tampered / "README.md").read_bytes() + b" ")
        with self.assertRaisesRegex(validator.CandidateRejected, "MANIFEST_FILE_HASH_MISMATCH"):
            validator.validate_candidate(tampered)
        unlisted = self.copy_candidate("unlisted")
        (unlisted / "unexpected.txt").write_text("unexpected", encoding="utf-8")
        with self.assertRaisesRegex(validator.CandidateRejected, "MANIFEST_UNLISTED_FILE"):
            validator.validate_candidate(unlisted)

    def test_symlink_and_broken_markdown_link_fail_closed(self):
        linked = self.copy_candidate("linked")
        (linked / "unexpected-link").symlink_to(linked / "README.md")
        with self.assertRaisesRegex(validator.CandidateRejected, "CANDIDATE_SYMLINK_REJECTED"):
            validator.validate_candidate(linked)
        with tempfile.TemporaryDirectory(prefix="payguard-link-test-") as temporary:
            root = Path(temporary)
            (root / "README.md").write_text("[missing](docs/missing.md)\n", encoding="utf-8")
            with self.assertRaisesRegex(validator.CandidateRejected, "MARKDOWN_LINK_MISSING"):
                validator.validate_links(root.resolve(), {"README.md": {}})

    def test_symlink_candidate_root_fails_before_resolution(self):
        linked_root = Path(self.temporary.name) / "candidate-root-link"
        linked_root.symlink_to(self.base, target_is_directory=True)
        with self.assertRaisesRegex(validator.CandidateRejected, "CANDIDATE_ROOT_INVALID"):
            validator.validate_candidate(linked_root)

    def test_manifest_source_identity_and_mapping_fail_closed(self):
        wrong_path = self.copy_candidate("wrong-source-path")
        manifest = json.loads((wrong_path / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
        readme = next(row for row in manifest["files"] if row["path"] == "README.md")
        readme["source_path"] = "docs/submission/quickstart.md"
        self.resign_manifest(wrong_path, manifest)
        with self.assertRaisesRegex(validator.CandidateRejected, "MANIFEST_SOURCE_PATH_MISMATCH"):
            validator.validate_candidate(wrong_path)

        wrong_hash = self.copy_candidate("wrong-source-hash")
        manifest = json.loads((wrong_hash / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
        readme = next(row for row in manifest["files"] if row["path"] == "README.md")
        readme["source_sha256"] = "0" * 64
        self.resign_manifest(wrong_hash, manifest)
        with self.assertRaisesRegex(validator.CandidateRejected, "MANIFEST_SOURCE_HASH_MISMATCH"):
            validator.validate_candidate(wrong_hash)

        mapped = self.copy_candidate("mapped-source-drift")
        mapped_path = mapped / "tools/run.sh"
        mapped_path.write_bytes(mapped_path.read_bytes() + b"\n")
        manifest = json.loads((mapped / validator.MANIFEST_NAME).read_text(encoding="utf-8"))
        mapped_row = next(row for row in manifest["files"] if row["path"] == "tools/run.sh")
        mapped_row["bytes"] = mapped_path.stat().st_size
        mapped_row["sha256"] = validator.sha256_bytes(mapped_path.read_bytes())
        mapped_row["source_sha256"] = mapped_row["sha256"]
        self.resign_manifest(mapped, manifest, rebuild_package=True)
        with self.assertRaisesRegex(validator.CandidateRejected, "MANIFEST_MAPPED_SOURCE_MISMATCH"):
            validator.validate_candidate(mapped)

    def test_detached_hash_package_digest_and_private_temp_fail_closed(self):
        detached = self.copy_candidate("detached")
        (detached / validator.DETACHED_NAME).write_text("0" * 64 + "  public_export_manifest.json\n", encoding="ascii")
        with self.assertRaisesRegex(validator.CandidateRejected, "DETACHED_MANIFEST_HASH_MISMATCH"):
            validator.validate_candidate(detached)
        package = self.copy_candidate("package")
        manifest_path = package / validator.MANIFEST_NAME
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["package_digest_sha256"] = "0" * 64
        payload = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
        manifest_path.write_bytes(payload)
        (package / validator.DETACHED_NAME).write_text(
            f"{validator.sha256_bytes(payload)}  {validator.MANIFEST_NAME}\n", encoding="ascii"
        )
        with self.assertRaisesRegex(validator.CandidateRejected, "PACKAGE_DIGEST_MISMATCH"):
            validator.validate_candidate(package)
        with tempfile.TemporaryDirectory(prefix="payguard-portable-test-") as temporary:
            root = Path(temporary)
            path = root / "sample.py"
            path.write_text('path = "' + "/private" + '/tmp/fixed"\n', encoding="utf-8")
            with self.assertRaisesRegex(validator.CandidateRejected, "PORTABLE_TEMP_PATH_VIOLATION"):
                validator.validate_public_text(root.resolve(), {"sample.py": {}})

    def test_case_insensitive_region_and_windows_private_paths_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix="payguard-public-text-test-") as temporary:
            root = Path(temporary)
            path = root / "sample.txt"
            for content, reason in (
                (("tai" + "wan").lower(), "US_SCOPE_RESIDUE"),
                (("TAI" + "PEI").upper(), "US_SCOPE_RESIDUE"),
                ("C:" + chr(92) + "Users" + chr(92) + "person" + chr(92) + "secret", "PRIVATE_ABSOLUTE_PATH_VIOLATION"),
                (chr(92) * 2 + "server" + chr(92) + "share" + chr(92) + "secret", "PRIVATE_ABSOLUTE_PATH_VIOLATION"),
            ):
                with self.subTest(reason=reason, content=content):
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaisesRegex(validator.CandidateRejected, reason):
                        validator.validate_public_text(root.resolve(), {"sample.txt": {}})

    def test_source_reader_rejects_symlink_ancestor_and_reads_regular_file(self):
        with tempfile.TemporaryDirectory(prefix="payguard-source-read-test-") as temporary:
            root = Path(temporary)
            real = root / "real"
            real.mkdir()
            source = real / "source.txt"
            source.write_bytes(b"bounded-source")
            linked = root / "linked"
            linked.symlink_to(real, target_is_directory=True)
            with mock.patch.object(builder, "PROJECT_ROOT", root):
                payload, mode = builder.read_source("real/source.txt")
                self.assertEqual(payload, b"bounded-source")
                self.assertEqual(mode, source.stat().st_mode & 0o777)
                with self.assertRaisesRegex(RuntimeError, "SOURCE_BOUNDARY_REJECTED"):
                    builder.read_source("linked/source.txt")

    def test_destination_inside_source_and_existing_destination_rejected(self):
        inside = builder.PROJECT_ROOT / "candidate-must-not-be-created"
        with self.assertRaisesRegex(RuntimeError, "DESTINATION_MUST_BE_OUTSIDE_SOURCE_ROOT"):
            builder.build_candidate(inside)
        with self.assertRaisesRegex(RuntimeError, "DESTINATION_ALREADY_EXISTS"):
            builder.build_candidate(self.base)
        self.assertFalse(inside.exists())


if __name__ == "__main__":
    unittest.main()
