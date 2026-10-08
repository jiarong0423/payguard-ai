"""Synthetic, isolation-only metadata runtime and boundary tests."""

from copy import deepcopy
from dataclasses import FrozenInstanceError
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

from payguard import reference_policy as runtime


ROOT = Path(__file__).absolute().parents[1]
PACKAGE = "US/paypal_aup_reference_v1"
def context():
    result = {
        "policy_domain": "AUP", "provider_account_region": "US", "merchant_legal_region": "US",
        "buyer_destination_region": None, "issuer_region_signal": None, "ip_country_signal": None,
        "event_time": "2026-10-05T18:00:00+08:00", "evaluated_at": "2026-10-06T01:00:00+08:00",
        "policy_as_of": "2026-10-05T18:00:00+08:00",
    }
    result["authority"] = {field: {"authority_class": "USER_CLAIMED", "provenance": "SYNTHETIC_TEST"} for field in result}
    result["authority"]["provider_account_region"]["authority_class"] = "PROVIDER_VERIFIED"
    result["authority"]["merchant_legal_region"]["authority_class"] = "MERCHANT_VERIFIED"
    for field in runtime._OPTIONAL_REGIONS:
        result["authority"][field] = {"authority_class": "UNKNOWN", "provenance": "NOT_PROVIDED"}
    return result


class ReferenceRuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary_parent = Path(tempfile.gettempdir()).resolve()
        self.temp = tempfile.TemporaryDirectory(prefix="payguard-reference-policy-", dir=temporary_parent)
        self.root = Path(self.temp.name)
        for relative in runtime._PINS:
            target = self.root / "policies" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / "policies" / relative, target)
        self.patcher = patch.object(runtime, "_PROJECT_ROOT", self.root)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temp.cleanup()

    def assert_safe(self, result, outcome=None, code=None):
        if outcome is not None:
            self.assertEqual(result["outcome"], outcome)
        if code is not None:
            self.assertEqual(result["reason_code"], code)
        self.assertEqual(result["evaluation_mode"], "REFERENCE_METADATA_ONLY")
        self.assertEqual(result["compliance_decision"], "NOT_MADE")
        self.assertEqual(result["current_policy_applicability"], "NOT_ESTABLISHED")
        for field in ("workflow_transition_authorized", "external_action_authorized", "rules_loaded", "rules_evaluated"):
            self.assertIs(result[field], False)
        self.assertIn("ordinary PayPal flow", result["limitations"][0])
        self.assertNotIn(str(self.root), json.dumps(result))

    def file(self, relative):
        return self.root / "policies" / relative

    def test_normal_us_metadata_and_effective_interval_absent(self):
        input_context = context()
        result = runtime.resolve_reference_context(input_context)
        self.assert_safe(result, "EVALUATE", "REFERENCE_METADATA_RESOLVED")
        self.assertEqual(result["context"], input_context)
        self.assertEqual(result["diagnostics"], [])
        metadata = result["reference_metadata"]
        self.assertEqual(metadata["package_id"], runtime._PACKAGE_ID)
        self.assertEqual(metadata["execution_tier"], "REFERENCE_ONLY")
        self.assertIsNone(metadata["effective_from"])
        self.assertIsNone(metadata["effective_to"])
        self.assertEqual(metadata["effective_status"], "NOT_VERIFIED")
        self.assertEqual(metadata["current_policy_applicability"], "NOT_ESTABLISHED")
        self.assertEqual(metadata["source_ids"], [runtime._SOURCE_ID])
        self.assertEqual(metadata["sources"][0]["visible_updated_date"], "2022-10-29")
        self.assertEqual(metadata["metadata_sha256"], dict(runtime._PINS))
        self.assertEqual(metadata["integrity_scope"], "PINNED_METADATA_ONLY")
        self.assertIs(metadata["rules_integrity_verified"], False)
        self.assertNotIn("rules_sha256", metadata)
        self.assertEqual(metadata["compliance_decision"], "NOT_MADE")
        self.assertEqual(metadata["evaluation_mode"], "REFERENCE_METADATA_ONLY")
        self.assertIs(metadata["workflow_transition_authorized"], False)
        self.assertIs(metadata["external_action_authorized"], False)
        self.assertIn("ordinary PayPal flow", " ".join(metadata["limitations"]))

    def test_unknown_provider_and_merchant_authority_unsupported(self):
        for field in ("provider_account_region", "merchant_legal_region"):
            for missing in (None, "UNKNOWN"):
                data = context()
                data[field] = missing
                data["authority"][field]["authority_class"] = "UNKNOWN"
                self.assert_safe(runtime.resolve_reference_context(data), "UNSUPPORTED", "AUTHORITATIVE_REGION_REQUIRED")
            for label in ("USER_CLAIMED", "DERIVED_SIGNAL"):
                data = context()
                data["authority"][field]["authority_class"] = label
                self.assert_safe(runtime.resolve_reference_context(data), "UNSUPPORTED", "AUTHORITATIVE_REGION_REQUIRED")

    def test_primary_conflict_preserves_dimensions_without_fallback(self):
        data = context()
        data["merchant_legal_region"] = "UK"
        with patch.object(runtime, "load_reference_package", side_effect=AssertionError("unexpected read")):
            result = runtime.resolve_reference_context(data)
        self.assert_safe(result, "CONTEXT_CONFLICT", "AUTHORITATIVE_REGION_CONFLICT")
        self.assertEqual(result["context"], data)
        self.assertIsNone(result["reference_metadata"])

    def test_auxiliary_geo_conflict_is_diagnostic_only(self):
        data = context()
        for field in runtime._OPTIONAL_REGIONS:
            data[field] = "CA"
            data["authority"][field] = {"authority_class": "USER_CLAIMED" if field == "buyer_destination_region" else "DERIVED_SIGNAL", "provenance": "SIGNAL_SUMMARY"}
        result = runtime.resolve_reference_context(data)
        self.assert_safe(result, "EVALUATE")
        self.assertEqual(result["context"], data)
        self.assertEqual([item["dimension"] for item in result["diagnostics"]], list(runtime._OPTIONAL_REGIONS))
        self.assertTrue(all(item["code"] == "GEO_SIGNAL_CONFLICT" and item["routing_effect"] == "NONE_REFERENCE_ONLY_AUP" for item in result["diagnostics"]))
        self.assertEqual(result["reference_metadata"]["jurisdiction"], "US")

    def test_matching_auxiliary_signals_no_conflict(self):
        data = context()
        for field in runtime._OPTIONAL_REGIONS:
            data[field] = "US"
            data["authority"][field]["authority_class"] = "DERIVED_SIGNAL"
        result = runtime.resolve_reference_context(data)
        self.assert_safe(result, "EVALUATE")
        self.assertEqual(result["diagnostics"], [])

    def test_unsupported_domain_and_foreign_regions_fail_before_package_load(self):
        cases = [("policy_domain", "AML", "UNSUPPORTED", "DOMAIN_UNSUPPORTED")]
        cases.extend(("provider_account_region", region, "UNSUPPORTED", "REGION_UNSUPPORTED") for region in ("CA", "GB"))
        cases.append(("provider_account_region", "GLOBAL", "INVALID_INPUT", "CONTEXT_SCHEMA_INVALID"))
        for field, value, outcome, code in cases:
            data = context()
            data[field] = value
            if field == "provider_account_region":
                data["merchant_legal_region"] = value
            with patch.object(runtime, "load_reference_package", side_effect=AssertionError("unsupported request must not load package")) as loader:
                result = runtime.resolve_reference_context(data)
            self.assert_safe(result, outcome, code)
            self.assertIsNone(result["reference_metadata"])
            loader.assert_not_called()

    def test_canonical_outcome_precedence_for_combined_failures(self):
        registry = self.file("registry.json")
        registry.write_bytes(registry.read_bytes() + b" ")
        data = context()
        data["policy_domain"] = "AML"
        self.assert_safe(runtime.resolve_reference_context(data), "UNSUPPORTED", "DOMAIN_UNSUPPORTED")
        data["merchant_legal_region"] = "UK"
        self.assert_safe(runtime.resolve_reference_context(data), "CONTEXT_CONFLICT", "AUTHORITATIVE_REGION_CONFLICT")
        data["event_time"] = "invalid"
        self.assert_safe(runtime.resolve_reference_context(data), "INVALID_INPUT", "DATE_INVALID")
        for field in ("provider_account_region", "merchant_legal_region"):
            data = context()
            data[field] = "UNKNOWN"
            data["authority"][field]["authority_class"] = "UNKNOWN"
            self.assert_safe(runtime.resolve_reference_context(data), "UNSUPPORTED", "AUTHORITATIVE_REGION_REQUIRED")
        self.assert_safe(runtime.resolve_reference_context(context()), "PACKAGE_INTEGRITY_FAILURE", "HASH_MISMATCH")
        registry.unlink()
        data = context()
        data["policy_domain"] = "AML"
        self.assert_safe(runtime.resolve_reference_context(data), "UNSUPPORTED", "DOMAIN_UNSUPPORTED")
        self.assert_safe(runtime.resolve_reference_context(context()), "PACKAGE_UNAVAILABLE", "METADATA_UNAVAILABLE")
        manifest = self.file(PACKAGE + "/manifest.json")
        manifest.write_bytes(manifest.read_bytes() + b" ")
        self.assert_safe(runtime.resolve_reference_context(data), "UNSUPPORTED", "DOMAIN_UNSUPPORTED")
        self.assert_safe(runtime.resolve_reference_context(context()), "PACKAGE_INTEGRITY_FAILURE", "HASH_MISMATCH")

    def test_insufficient_authority_does_not_claim_primary_conflict(self):
        data = context()
        data["provider_account_region"] = "CA"
        data["authority"]["provider_account_region"]["authority_class"] = "USER_CLAIMED"
        self.assert_safe(runtime.resolve_reference_context(data), "UNSUPPORTED", "AUTHORITATIVE_REGION_REQUIRED")

    def test_context_unknown_fields_path_traversal_and_raw_text_rejected(self):
        for field, value in (("path", "../../rules.json"), ("registry_path", "/tmp/registry.json"), ("package_id", runtime._PACKAGE_ID), ("rules", {"operator": "eval"}), ("raw_ip", "192.0.2.1"), ("description", "synthetic raw text")):
            data = context()
            data[field] = value
            with patch.object(runtime, "load_reference_package", side_effect=AssertionError("unexpected read")):
                result = runtime.resolve_reference_context(data)
            self.assert_safe(result, "INVALID_INPUT", "CONTEXT_SCHEMA_INVALID")
            self.assertIsNone(result["context"])
            self.assertNotIn(value if isinstance(value, str) else "operator", json.dumps(result))

    def test_context_types_regions_and_missing_fields_rejected(self):
        cases = []
        for field, value in (("provider_account_region", "us"), ("merchant_legal_region", "../../US"), ("policy_domain", []), ("issuer_region_signal", True), ("ip_country_signal", "USA")):
            data = context()
            data[field] = value
            cases.append(data)
        data = context()
        del data["buyer_destination_region"]
        cases.extend((data, None, [], "AUP"))
        for data in cases:
            self.assert_safe(runtime.resolve_reference_context(data), "INVALID_INPUT")

    def test_invalid_authority_and_provenance_are_sanitized(self):
        for descriptor in ({"authority_class": "ROOT", "provenance": "SYNTHETIC_TEST"}, {"authority_class": "PROVIDER_VERIFIED", "provenance": "raw private note"}, {"authority_class": "PROVIDER_VERIFIED"}, []):
            data = context()
            data["authority"]["provider_account_region"] = descriptor
            self.assert_safe(runtime.resolve_reference_context(data), "INVALID_INPUT", "CONTEXT_AUTHORITY_INVALID")
        data = context()
        data["issuer_region_signal"] = "CA"
        data["authority"]["issuer_region_signal"]["authority_class"] = "PROVIDER_VERIFIED"
        self.assert_safe(runtime.resolve_reference_context(data), "INVALID_INPUT", "SIGNAL_AUTHORITY_INVALID")
        data = context()
        data["provider_account_region"] = "UNKNOWN"
        self.assert_safe(runtime.resolve_reference_context(data), "INVALID_INPUT", "CONTEXT_AUTHORITY_INVALID")

    def test_dates_invalid_naive_offsets_and_time_order(self):
        for value in ("2026-10-05", "2026-10-05T18:00:00", "2026-02-30T00:00:00Z", "2026-10-05T18:00:00+99:00", None, 5):
            data = context()
            data["event_time"] = value
            self.assert_safe(runtime.resolve_reference_context(data), "INVALID_INPUT", "DATE_INVALID")
        for field in ("event_time", "policy_as_of"):
            data = context()
            data[field] = "2026-10-07T00:00:00Z"
            self.assert_safe(runtime.resolve_reference_context(data), "INVALID_INPUT", "TIME_ORDER_INVALID")
        data = context()
        data["evaluated_at"] = "2026-10-05T17:00:00Z"
        self.assert_safe(runtime.resolve_reference_context(data), "EVALUATE")

    def test_offset_component_overflow_all_context_fields_before_metadata_io(self):
        offsets = ("+00:60", "+01:99", "-00:60", "-01:99", "+24:00", "-24:00", "+25:00", "-25:00", "+99:59", "-99:59")
        for state in ("valid", "unavailable", "tampered"):
            target = self.file("registry.json")
            original = (ROOT / "policies/registry.json").read_bytes()
            if state == "unavailable":
                target.unlink()
            elif state == "tampered":
                target.write_bytes(original + b" ")
            for field in ("event_time", "evaluated_at", "policy_as_of"):
                for offset in offsets:
                    with self.subTest(state=state, field=field, offset=offset):
                        data = context()
                        data[field] = "2026-10-05T09:00:00" + offset
                        with patch.object(runtime, "_read_pinned", side_effect=AssertionError("invalid timestamp metadata I/O")) as reader:
                            self.assert_safe(runtime.resolve_reference_context(data), "INVALID_INPUT", "DATE_INVALID")
                            reader.assert_not_called()
            target.write_bytes(original)

    def test_bad_offset_metadata_timestamp_keeps_integrity_outcome(self):
        offsets = ("+00:60", "+01:99", "-00:60", "-01:99", "+24:00", "-24:00", "+25:00", "-25:00", "+99:59", "-99:59")
        source = runtime._parse(self.file(PACKAGE + "/source_index.json").read_bytes())
        for offset in offsets:
            value = "2026-10-05T09:00:00" + offset
            with self.subTest(offset=offset):
                with self.assertRaises(runtime.ReferencePolicyError) as caught:
                    runtime._instant(value)
                self.assertEqual(caught.exception.outcome, "PACKAGE_INTEGRITY_FAILURE")
                self.assertEqual(caught.exception.code, "DATE_INVALID")
                data = deepcopy(source)
                data["sources"][0]["observed_at"] = value
                with self.assertRaises(runtime.ReferencePolicyError) as caught:
                    runtime._validate_sources(data)
                self.assertEqual(caught.exception.outcome, "PACKAGE_INTEGRITY_FAILURE")

    def test_valid_offset_boundaries_z_fractions_and_context_fields(self):
        suffixes = ("+00:59", "-00:59", "+23:59", "-23:59", "Z", "+00:00", "-00:00")
        for suffix in suffixes:
            for fraction in ("", ".1", ".123456"):
                value = "2026-10-05T09:00:00" + fraction + suffix
                with self.subTest(value=value):
                    instant = runtime._instant(value)
                    self.assertEqual(instant.utcoffset().total_seconds(), 0)
                    data = context()
                    for field in ("event_time", "evaluated_at", "policy_as_of"):
                        data[field] = value
                    result = runtime.resolve_reference_context(data)
                    self.assert_safe(result, "EVALUATE")
                    self.assertEqual(result["context"], data)

    def test_offset_utc_equivalence_and_time_order_are_not_coerced(self):
        equivalent = ("2026-10-05T09:00:00Z", "2026-10-05T09:59:00+00:59", "2026-10-05T08:01:00-00:59", "2026-10-06T08:59:00+23:59", "2026-10-04T09:01:00-23:59")
        expected = runtime._instant(equivalent[0])
        for value in equivalent:
            self.assertEqual(runtime._instant(value), expected)
            for field in ("event_time", "evaluated_at", "policy_as_of"):
                data = context()
                for timestamp in ("event_time", "evaluated_at", "policy_as_of"):
                    data[timestamp] = equivalent[0]
                data[field] = value
                result = runtime.resolve_reference_context(data)
                self.assert_safe(result, "EVALUATE")
                self.assertEqual(result["context"][field], value)
        for field in ("event_time", "policy_as_of"):
            data = context()
            data["event_time"] = equivalent[1]
            data["policy_as_of"] = equivalent[2]
            data["evaluated_at"] = equivalent[0]
            data[field] = "2026-10-05T09:59:00.000001+00:59"
            with patch.object(runtime, "_read_pinned", side_effect=AssertionError("time order metadata I/O")) as reader:
                self.assert_safe(runtime.resolve_reference_context(data), "INVALID_INPUT", "TIME_ORDER_INVALID")
                reader.assert_not_called()

    def test_all_metadata_raw_hash_tamper_fails_without_exposure(self):
        for relative in runtime._PINS:
            target = self.file(relative)
            before = target.read_bytes()
            target.write_bytes(before + b" ")
            self.assert_safe(runtime.resolve_reference_context(context()), "PACKAGE_INTEGRITY_FAILURE", "HASH_MISMATCH")
            target.write_bytes(before)

    def test_missing_metadata_fails_without_exposure(self):
        for relative in runtime._PINS:
            target = self.file(relative)
            raw = target.read_bytes()
            target.unlink()
            result = runtime.resolve_reference_context(context())
            self.assert_safe(result, "PACKAGE_UNAVAILABLE", "METADATA_UNAVAILABLE")
            self.assertIsNone(result["reference_metadata"])
            target.write_bytes(raw)

    def test_no_rules_open_read_or_stat_even_poisoned_or_missing(self):
        rules = self.file(PACKAGE + "/rules.json")
        rules.symlink_to("/does/not/exist")
        real_open, real_stat = os.open, os.stat
        opened = []
        def guard_open(path, *args, **kwargs):
            self.assertNotIn("rules.json", str(path))
            opened.append(str(path))
            return real_open(path, *args, **kwargs)
        def guard_stat(path, *args, **kwargs):
            self.assertNotIn("rules.json", str(path))
            return real_stat(path, *args, **kwargs)
        with patch.object(os, "open", guard_open), patch.object(os, "stat", guard_stat), patch.object(os, "supports_dir_fd", set(os.supports_dir_fd) | {guard_open}):
            self.assert_safe(runtime.resolve_reference_context(context()), "EVALUATE")
        self.assertEqual([item for item in opened if item.endswith(".json")], ["registry.json", "manifest.json", "source_index.json"])
        rules.unlink()
        self.assert_safe(runtime.resolve_reference_context(context()), "EVALUATE")

    def test_symlink_file_and_ancestor_refused(self):
        target = self.file("registry.json")
        target.unlink()
        target.symlink_to(ROOT / "policies/registry.json")
        self.assert_safe(runtime.resolve_reference_context(context()), "PACKAGE_INTEGRITY_FAILURE", "PATH_BOUNDARY_VIOLATION")
        alias = self.root / "alias"
        alias.symlink_to(ROOT, target_is_directory=True)
        with patch.object(runtime, "_PROJECT_ROOT", alias):
            self.assert_safe(runtime.resolve_reference_context(context()), "PACKAGE_INTEGRITY_FAILURE", "PATH_BOUNDARY_VIOLATION")

    def test_module_root_alias_loads_while_descendant_alias_stays_untrusted(self):
        with tempfile.TemporaryDirectory(prefix="payguard-reference-alias-") as temporary:
            alias = Path(temporary) / "project-alias"
            alias.symlink_to(ROOT, target_is_directory=True)
            module_path = alias / "src/payguard/reference_policy.py"
            self.assertNotEqual(module_path.absolute(), module_path.resolve(strict=True))
            with (
                patch.object(runtime, "_PROJECT_ROOT", runtime._MODULE_PROJECT_ROOT),
                patch.object(runtime, "__file__", str(module_path)),
            ):
                package = runtime.load_reference_package()
            self.assertEqual(package.metadata()["metadata_sha256"], dict(runtime._PINS))

            descendant = self.root / "policies" / "US"
            actual = self.root / "actual-us"
            descendant.rename(actual)
            descendant.symlink_to(actual, target_is_directory=True)
            self.assert_safe(
                runtime.resolve_reference_context(context()),
                "PACKAGE_INTEGRITY_FAILURE",
                "PATH_BOUNDARY_VIOLATION",
            )

    def test_missing_module_derived_root_fails_closed(self):
        missing_module = self.root / "missing/src/payguard/reference_policy.py"
        with (
            patch.object(runtime, "_PROJECT_ROOT", runtime._MODULE_PROJECT_ROOT),
            patch.object(runtime, "__file__", str(missing_module)),
        ):
            self.assert_safe(
                runtime.resolve_reference_context(context()),
                "PACKAGE_UNAVAILABLE",
                "METADATA_UNAVAILABLE",
            )

    def test_fifo_directory_and_oversize_rejected_without_blocking(self):
        target = self.file("registry.json")
        target.unlink()
        os.mkfifo(target)
        self.assert_safe(runtime.resolve_reference_context(context()), "PACKAGE_INTEGRITY_FAILURE", "FILE_TYPE_INVALID")
        target.unlink()
        target.mkdir()
        self.assert_safe(runtime.resolve_reference_context(context()), "PACKAGE_INTEGRITY_FAILURE", "FILE_TYPE_INVALID")
        target.rmdir()
        target.write_bytes(b"x" * (runtime._MAX_BYTES + 1))
        self.assert_safe(runtime.resolve_reference_context(context()), "PACKAGE_INTEGRITY_FAILURE", "FILE_SIZE_INVALID")

    def test_path_allowlist_and_public_api_have_no_path_pin_parameters(self):
        for path in ("../../rules.json", "/tmp/registry.json", PACKAGE + "/rules.json", "US/../registry.json"):
            with self.assertRaises(runtime.ReferencePolicyError) as caught:
                runtime._read_pinned(path)
            self.assertEqual(caught.exception.code, "PATH_NOT_ALLOWLISTED")
        with self.assertRaises(TypeError):
            runtime.load_reference_package(self.root)
        with self.assertRaises(TypeError):
            runtime.resolve_reference_context(context(), path=self.root)

    def test_parser_duplicate_keys_nonfinite_encoding_and_bounds(self):
        cases = [(b'{"x":1,"x":2}', "DUPLICATE_JSON_KEY"), (b'{"nested":{"x":1,"x":2}}', "DUPLICATE_JSON_KEY"), (b'{"x":NaN}', "JSON_INVALID"), (b'\xff', "JSON_INVALID"), (b'[]' * 40000, "FILE_SIZE_INVALID"), (b'', "FILE_SIZE_INVALID"), (b'[' * 12 + b'0' + b']' * 12, "JSON_LIMIT_EXCEEDED")]
        for raw, code in cases:
            with self.assertRaises(runtime.ReferencePolicyError) as caught:
                runtime._parse(raw)
            self.assertEqual(caught.exception.code, code)

    def test_exact_schema_unknown_wrongtype_identity_and_tier_rejected(self):
        validators = (("registry.json", runtime._validate_registry), (PACKAGE + "/manifest.json", runtime._validate_manifest), (PACKAGE + "/source_index.json", runtime._validate_sources))
        for relative, validator in validators:
            original = runtime._parse(self.file(relative).read_bytes())
            for mutation in ({**original, "unknown": "value"}, {**original, "schema_version": 1}, {key: value for key, value in original.items() if key != "schema_version"}):
                with self.assertRaises(runtime.ReferencePolicyError):
                    validator(mutation)
        registry = runtime._parse(self.file("registry.json").read_bytes())
        for key, value in (("relative_path", "../../US"), ("package_id", "CA_AUP"), ("canonical_runtime_active", 0), ("active_tier", "SHADOW")):
            data = deepcopy(registry)
            data["packages"][0][key] = value
            with self.assertRaises(runtime.ReferencePolicyError):
                runtime._validate_registry(data)
        manifest = runtime._parse(self.file(PACKAGE + "/manifest.json").read_bytes())
        for key, value in (("effective_from", "2022-11-02"), ("effective_to", "2027-01-01"), ("current_policy_applicability", "ESTABLISHED"), ("execution_tier", "SHADOW"), ("workflow_transition_authorized", True), ("retroactive", 0)):
            data = {**manifest, key: value}
            with self.assertRaises(runtime.ReferencePolicyError):
                runtime._validate_manifest(data)
        source = runtime._parse(self.file(PACKAGE + "/source_index.json").read_bytes())
        for key, value in (("source_id", "other"), ("url", "https://example.org"), ("effective_from", "2022-11-02"), ("unknown", None)):
            data = deepcopy(source)
            data["sources"][0][key] = value
            with self.assertRaises(runtime.ReferencePolicyError):
                runtime._validate_sources(data)
        data = deepcopy(source)
        data["limitations"][0] = []
        with self.assertRaises(runtime.ReferencePolicyError):
            runtime._validate_sources(data)

    def test_snapshot_immutable_detached_and_constructor_rejected(self):
        package = runtime.load_reference_package()
        with self.assertRaises(FrozenInstanceError):
            package._metadata_bytes = b'{}'
        with self.assertRaises(runtime.ReferencePolicyError):
            runtime.ReferencePackage(b'{}')
        first = package.metadata()
        first["source_ids"].clear()
        first["sources"][0]["title"] = "changed"
        self.assertEqual(package.metadata()["source_ids"], [runtime._SOURCE_ID])
        data = context()
        result = runtime.resolve_reference_context(data)
        result["context"]["authority"].clear()
        self.assertEqual(data, context())

    def test_second_identical_resolution_has_zero_write_delta(self):
        def inventory():
            return {relative: (hashlib.sha256(self.file(relative).read_bytes()).hexdigest(), self.file(relative).stat().st_mtime_ns, self.file(relative).stat().st_size) for relative in runtime._PINS}
        before = inventory()
        first = runtime.resolve_reference_context(context())
        middle = inventory()
        second = runtime.resolve_reference_context(context())
        self.assertEqual(first, second)
        self.assertEqual(before, middle)
        self.assertEqual(before, inventory())
        self.assertEqual(set(p.relative_to(self.root).as_posix() for p in self.root.rglob("*") if p.is_file()), {"policies/" + relative for relative in runtime._PINS})

    def test_import_performs_no_io(self):
        source = ROOT / "src/payguard/reference_policy.py"
        code = compile(source.read_bytes(), str(source), "exec")
        spec = importlib.util.spec_from_loader("payguard_reference_import_probe", loader=None, origin=str(source))
        module = importlib.util.module_from_spec(spec)
        module.__file__ = str(source)
        sys.modules[spec.name] = module
        try:
            with patch.object(os, "open", side_effect=AssertionError("import I/O")), patch.object(Path, "open", side_effect=AssertionError("import I/O")), patch.object(Path, "stat", side_effect=AssertionError("import I/O")):
                exec(code, module.__dict__)
        finally:
            del sys.modules[spec.name]


if __name__ == "__main__":
    unittest.main()
