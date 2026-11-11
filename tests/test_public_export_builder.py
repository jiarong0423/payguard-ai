"""Focused tests for the fail-closed and published-source export contracts."""

import ast
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
            "docs/submission/screens/real_send_trace.png",
            "docs/submission/screens/refusals_locked.png",
            "docs/submission/screens/ag_studio_trace.png",
            "docs/submission/screens/evidence_pages.png",
            "docs/submission/payguard_judge_overview.png",
            "docs/submission/payguard_judge_overview.svg",
            "docs/submission/video_script.md",
            "frontend/src/operatorLabels.js",
            "THIRD_PARTY_NOTICES.md",
            "tests/frontend_operator_labels.mjs",
            "tests/frontend_recording_contract.mjs",
            "tests/test_public_export_builder.py",
        ):
            self.assertTrue((self.base / relative).is_file(), relative)
        readme = (self.base / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("payguard_cover", readme)
        self.assertNotIn("payguard_zip_review_slide", readme)
        self.assertLess(
            readme.index("docs/submission/screens/real_send_trace.png"),
            readme.index("docs/submission/payguard_judge_overview.png"),
        )
        self.assertLess(
            readme.index("docs/submission/payguard_judge_overview.png"),
            readme.index("Screens from an earlier cut (2:50)"),
        )
        screens_order = [
            readme.index("docs/submission/screens/refusals_locked.png"),
            readme.index("docs/submission/screens/ag_studio_trace.png"),
            readme.index("docs/submission/screens/evidence_pages.png"),
        ]
        self.assertEqual(screens_order, sorted(screens_order))
        self.assertLess(readme.index("Screens from an earlier cut (2:50)"), screens_order[0])
        for removed in ("payguard_cover.png", "payguard_cover.svg", "payguard_zip_review_slide.png"):
            self.assertFalse((self.base / "docs/submission" / removed).exists(), removed)
        # the 2026-10 status map is retired: README embeds the current architecture overview instead
        self.assertFalse((self.base / "docs/decisions/2026Q4/payguard_us_architecture_status.svg").exists())
        self.assertNotIn("payguard_us_architecture_status", readme)
        self.assertIn("docs/submission/diagrams/architecture_overview.svg", readme)
        for retired in ("merchant defense buffer", "drawn before the country rules check"):
            self.assertNotIn(retired, readme.casefold())
        self.assertLess(
            readme.index("docs/submission/payguard_judge_overview.png"),
            readme.index("1. **Before a draft — AUP preflight:**"),
        )
        for forbidden in (".venv", "__pycache__", "output", "logs", "archive", "rollback"):
            self.assertFalse(any(forbidden in path.parts for path in self.base.rglob("*")))
        # an allowlist omission must not ship a package that cannot import itself: every local import in the candidate resolves to a shipped file
        for tree, package in (("backend/app", "backend.app"), ("src/payguard", "payguard")):
            for module in sorted((self.base / tree).glob("*.py")):
                for node in ast.walk(ast.parse(module.read_text(encoding="utf-8"))):
                    targets = []
                    if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                        targets.append(node.module.split(".")[0])
                    elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module and node.module.startswith(package + "."):
                        targets.append(node.module[len(package) + 1:].split(".")[0])
                    elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module == package:
                        targets.extend(alias.name for alias in node.names)
                    for target in targets:
                        self.assertTrue((self.base / tree / f"{target}.py").is_file() or (self.base / tree / target).is_dir(),
                                        f"{module.name} imports {target}, which is not in the public package")

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
        self.assertEqual(manifest["remaining_gates"], [])
        for relative in ("README.md", "docs/submission/quickstart.md"):
            text = (self.published / relative).read_text(encoding="utf-8").casefold()
            self.assertIn("complete repository run instructions", text)
            self.assertIn("hosted demo", text)
            self.assertIn("optional", text)
            self.assertIn("not performed", text)
            self.assertNotIn("publication is not authorized", text)
            self.assertNotIn("publication remains closed", text)
            self.assertNotIn("public release remains closed", text)
        for relative, contradictions in validator.PUBLISHED_RELEASE_ASSETS.items():
            text = (self.published / relative).read_text(encoding="utf-8").casefold()
            for statement in validator.PUBLISHED_CURRENT_STATE:
                self.assertIn(statement, text)
            for contradiction in contradictions:
                self.assertNotIn(contradiction, text)
        for relative in (
            "README.md",
            "SECURITY.md",
            "docs/submission/quickstart.md",
            "docs/decisions/2026Q4/architecture.md",
            "docs/decisions/2026Q4/us_mainline_contract.md",
        ):
            text = (self.published / relative).read_text(encoding="utf-8").casefold()
            self.assertIn("the devpost project is submitted", text)
            self.assertNotIn("devpost remains pending", text)
            self.assertNotIn("devpost submission remains", text)

    def test_public_run_docs_keep_optional_profiles_and_attested_evidence_explicit(self):
        for relative in ("README.md", "docs/submission/quickstart.md"):
            with self.subTest(relative=relative):
                text = (self.published / relative).read_text(encoding="utf-8").casefold()
                self.assertIn("the console starts without the gemini profile", text)
                self.assertIn("wsl 2", text)
                self.assertIn("2026-10-06", text)
                self.assertIn("inv2-...-w5uw", text)
                self.assertNotIn("inv2-2mta-prpq-4caj-w5uw", text)
                self.assertNotIn("sandbox path proves", text)
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
        self.assertEqual(sum(len(items) for items in validator.PUBLISHED_RELEASE_ASSETS.values()), 9)
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

    def test_only_the_country_rules_files_may_name_regions_and_the_time_zone_stays_forbidden(self):
        relative = "src/payguard/country_rules.py"
        self.assertIn(relative, validator.REGION_TEXT_FILES)
        with tempfile.TemporaryDirectory(prefix="payguard-region-text-test-") as temporary:
            root = Path(temporary)
            (root / relative).parent.mkdir(parents=True)
            (root / relative).write_text("Tai" + "wan " + chr(0x6CD5), encoding="utf-8")
            validator.validate_public_text(root.resolve(), {relative: {}})
            (root / relative).write_text("Asia/" + "Tai" + "pei", encoding="utf-8")
            with self.assertRaisesRegex(validator.CandidateRejected, "US_SCOPE_RESIDUE"):
                validator.validate_public_text(root.resolve(), {relative: {}})
            (root / "other.py").write_text(chr(0x6CD5), encoding="utf-8")
            with self.assertRaisesRegex(validator.CandidateRejected, "US_SCOPE_RESIDUE"):
                validator.validate_public_text(root.resolve(), {"other.py": {}})

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

class ImportIntegrityTests(unittest.TestCase):
    """The builder refuses a package in which an exported file imports a file that is not exported."""

    def current_payloads(self):
        return {relative: builder.read_source(relative)[0] for relative in builder.source_paths()}

    def test_current_allowlist_is_import_complete(self):
        self.assertEqual(builder.import_integrity_problems(self.current_payloads()), [])

    def test_every_import_form_must_resolve(self):
        source = {
            "backend/app/main.py": b"from .gone import x\nfrom .ok import y\nfrom payguard import missing_mod, CONSTANT\n",
            "backend/app/ok.py": b"",
            "src/payguard/__init__.py": b"CONSTANT = 1\n",
            "tests/test_x.py": b"import sys\nimport json\nimport helper_tool\nfrom app.absent import z\nfrom tools import shipped\n",
            "tools/shipped.py": b"",
            "frontend/src/main.jsx": (b"import App from './App.jsx';\nimport './gone.css';\n"
                                      b"const Lazy = lazy(() => import('./Lazy.jsx'));\n"
                                      b"export { thing } from './reexport.js';\n"
                                      b"const css = new URL('./theme.css', import.meta.url);\n"
                                      b"const quoted = \"import X from './only_in_a_string.js';\";\n"
                                      b"import {\n  a,\n  b,\n} from './multi';\n"),
            "frontend/src/App.jsx": b"import data from './data/table.json';\n",
            "frontend/index.html": b'<link rel="icon" href="/icons/icon.svg"><script type="module" src="/src/main.jsx"></script>'
                                   b'<a href="https://example.com/x">x</a><a href="//cdn.example/y">y</a>',
        }
        on_disk = set(source) | {"src/payguard/missing_mod.py", "tools/helper_tool.py"}
        problems = builder.import_integrity_problems(source, source_exists=lambda path: path in on_disk)
        self.assertEqual(problems, sorted([
            "backend/app/main.py -> .gone",
            "backend/app/main.py -> payguard import missing_mod",
            "frontend/index.html -> /icons/icon.svg",
            "frontend/src/App.jsx -> ./data/table.json",
            "frontend/src/main.jsx -> ./Lazy.jsx",
            "frontend/src/main.jsx -> ./gone.css",
            "frontend/src/main.jsx -> ./multi",
            "frontend/src/main.jsx -> ./reexport.js",
            "frontend/src/main.jsx -> ./theme.css",
            "tests/test_x.py -> app.absent",
            "tests/test_x.py -> helper_tool",
        ]))
        resolved = dict(source, **{name: b"" for name in (
            "backend/app/gone.py", "src/payguard/missing_mod.py", "tools/helper_tool.py", "backend/app/absent.py",
            "frontend/src/Lazy.jsx", "frontend/src/gone.css", "frontend/src/multi.js", "frontend/src/reexport.js",
            "frontend/src/theme.css", "frontend/src/data/table.json", "frontend/public/icons/icon.svg")})
        self.assertEqual(builder.import_integrity_problems(resolved, source_exists=lambda path: path in resolved), [])

    def test_unparseable_python_fails_closed(self):
        problems = builder.import_integrity_problems({"backend/app/main.py": b"def broken(:\n"}, source_exists=lambda _p: False)
        self.assertEqual(problems, ["backend/app/main.py -> <unparseable>"])

    def test_build_fails_when_an_imported_file_is_dropped(self):
        cases = (("backend/app", "guide_model.py", "backend/app/guide_routes.py -> .guide_model"),
                 ("frontend/src", "pwa.js", "frontend/src/main.jsx -> ./pwa.js"),
                 ("frontend/public", "icons/icon.svg", "frontend/index.html -> /icons/icon.svg"))
        for tree, name, expected in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory(prefix="payguard-import-integrity-") as temporary:
                tree_files = dict(builder.TREE_FILES)
                tree_files[tree] = tuple(item for item in tree_files[tree] if item != name)
                with mock.patch.object(builder, "TREE_FILES", tree_files):
                    with self.assertRaises(RuntimeError) as captured:
                        builder.build_candidate(Path(temporary) / "candidate")
                    self.assertTrue(str(captured.exception).startswith("SOURCE_IMPORT_UNRESOLVED:"))
                    self.assertIn(expected, str(captured.exception))
                    self.assertFalse((Path(temporary) / "candidate").exists())
                    with mock.patch("builtins.print") as printed:
                        self.assertEqual(builder.main([str(Path(temporary) / "candidate")]), 2)
                    self.assertEqual(json.loads(printed.call_args.args[0])["status"], "FAILED")


class ExportBoundaryInventoryTests(unittest.TestCase):
    """Every file in the audited source trees is exported or excluded with a written reason."""

    def source_files(self, tree):
        root = builder.PROJECT_ROOT / tree
        return {path.relative_to(builder.PROJECT_ROOT).as_posix() for path in root.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}}

    def test_audited_trees_are_fully_accounted_for(self):
        exported = set(builder.source_paths()) | set(builder.MAPPED_FILES)
        for tree in builder.AUDITED_TREES:
            with self.subTest(tree=tree):
                unaccounted = self.source_files(tree) - exported - set(builder.EXCLUDED_WITH_REASON)
                self.assertEqual(unaccounted, set(), "add each file to the allowlist or to EXCLUDED_WITH_REASON")

    def test_exclusions_are_disjoint_audited_and_explained(self):
        exported = set(builder.source_paths())
        self.assertEqual(exported & set(builder.EXCLUDED_WITH_REASON), set())
        # (r34 E2 P1-1) A built candidate, and the public clone made from it, hold no excluded file by design, so the
        # stale check runs only in the source tree. ".git" cannot tell them apart: the public clone has one too.
        source_tree = any((builder.PROJECT_ROOT / relative).is_file() for relative in builder.EXCLUDED_WITH_REASON)
        for relative, reason in builder.EXCLUDED_WITH_REASON.items():
            self.assertTrue(relative.startswith(tuple(f"{tree}/" for tree in builder.AUDITED_TREES)), relative)
            self.assertGreaterEqual(len(reason), 20, relative)
            if source_tree:
                self.assertTrue((builder.PROJECT_ROOT / relative).is_file(), f"stale exclusion: {relative}")

    def test_frontend_public_tree_ships_whole(self):
        self.assertEqual(self.source_files("frontend/public") - set(builder.source_paths()), set())

    def test_guided_gap_filling_ships_front_and_back(self):
        exported = set(builder.source_paths())
        for relative in ("backend/app/guide_routes.py", "backend/app/guide_model.py", "backend/app/demo_mode.py",
                         "backend/app/channel3.py", "src/payguard/evidence_guide.py", "src/payguard/controlled_fallback.py",
                         "frontend/src/GuideLive.jsx", "frontend/src/GuideLive.css", "frontend/src/GuideReplay.jsx",
                         "frontend/src/GuideReplay.css", "frontend/src/data/guide_replays_v1.json", "frontend/src/pwa.js",
                         "frontend/src/pwa.css", "tools/make_prompt_pack.py", "Dockerfile", ".dockerignore", "render.yaml",
                         # (review r25) the offline scorer ships with the records that cite it
                         "tools/score_replies.py", "docs/evidence/GUIDE_STRESS_TEST.md"):
            self.assertIn(relative, exported)
        for relative in ("tools/gemini_api_trial.py", "tools/vertex_trial.py", "tools/local_trial.py",
                         "tools/compare_runs.py", "tools/trial_evidence_guide.py"):
            self.assertNotIn(relative, exported)

    def test_unmasked_dispute_id_is_refused(self):
        # (r37) A Sandbox dispute id with its digits must not reach public text; masked and synthetic TST ids pass.
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "note.md").write_text("see PP-R-ABC-" + "12345678", encoding="utf-8")
            with self.assertRaises(validator.CandidateRejected) as caught:
                validator.validate_public_text(root, {"note.md": {}})
            self.assertEqual(str(caught.exception), "UNMASKED_DISPUTE_ID")
            (root / "note.md").write_text("see PP-R-OJX-... (masked) and PP-R-TST-00000001", encoding="utf-8")
            validator.validate_public_text(root, {"note.md": {}})


if __name__ == "__main__":
    unittest.main()
