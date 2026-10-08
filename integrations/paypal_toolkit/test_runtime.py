"""Stdlib profile boundaries; the launcher owns only the Python 3.12 profile."""
from copy import deepcopy
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_runtime as guard

PROFILE = Path(__file__).resolve().parent

class RuntimeProfileTests(unittest.TestCase):
    def setUp(self):
        self.pins = guard.validate_profile(PROFILE)
        self.inventory = [SimpleNamespace(metadata={'Name':name},version=version) for name,version in self.pins.items()]

    def rejected(self,code,callback):
        with self.assertRaises(guard.RuntimeRejected) as captured: callback()
        self.assertEqual(captured.exception.code,code)

    def test_mock_inventory_passes_and_capability_hook_receives_fixed_root(self):
        calls=[]
        result=guard.check(PROFILE,version=(3,12,14),distributions=self.inventory,capability_loader=calls.append)
        self.assertEqual(result['locked_distributions'],160)
        self.assertEqual(calls,[PROFILE.parent.parent])

    def test_python_313_rejected_before_inventory_or_imports(self):
        with patch.object(guard,'validate_profile',side_effect=AssertionError('must fail before reads')):
            self.rejected('PROFILE_PYTHON_312_REQUIRED',lambda:guard.check(PROFILE,version=(3,13,12)))

    def test_missing_distribution(self):
        self.rejected('PROFILE_INVENTORY_MISMATCH',lambda:guard.validate_inventory(self.pins,self.inventory[:-1]))

    def test_wrong_distribution_version(self):
        values=deepcopy(self.inventory);values[0].version='0.0.0'
        self.rejected('PROFILE_INVENTORY_MISMATCH',lambda:guard.validate_inventory(self.pins,values))

    def test_extra_distribution(self):
        self.rejected('PROFILE_INVENTORY_MISMATCH',lambda:guard.validate_inventory(self.pins,self.inventory+[SimpleNamespace(metadata={'Name':'unexpected'},version='1.0')]))

    def test_duplicate_normalized_distribution(self):
        self.rejected('PROFILE_INVENTORY_INVALID',lambda:guard.validate_inventory(self.pins,self.inventory+[SimpleNamespace(metadata={'Name':'OPENAI_AGENTS'},version='0.0.2')]))

    def test_manifest_direct_pin_and_python_and_count_parity(self):
        original=guard.tomllib.loads((PROFILE/'pyproject.toml').read_text())
        variants=[]
        changed=deepcopy(original);changed['project']['requires-python']='>=3.12';variants.append(changed)
        changed=deepcopy(original);changed['project']['dependencies'][0]='paypal-agent-toolkit==1.12.0';variants.append(changed)
        changed=deepcopy(original);changed['tool']['payguard-paypal-toolkit']['inventory-count']=True;variants.append(changed)
        for value in variants:
            with self.subTest(value=value),patch.object(guard.tomllib,'loads',return_value=value):
                self.rejected('PROFILE_MANIFEST_INVALID',lambda:guard.validate_profile(PROFILE))

    def test_manifest_lock_digest_mismatch(self):
        manifest=guard.tomllib.loads((PROFILE/'pyproject.toml').read_text());manifest['tool']['payguard-paypal-toolkit']['lock-sha256']='0'*64
        with patch.object(guard.tomllib,'loads',return_value=manifest):
            self.rejected('PROFILE_LOCK_HASH_INVALID',lambda:guard.validate_profile(PROFILE))

    def test_lock_bytes_tampered(self):
        raw=(PROFILE/'requirements.lock').read_bytes()+b'unknown==1.0 \\\n    --hash=sha256:'+b'0'*64+b'\n'
        with patch.object(Path,'read_bytes',return_value=raw):
            self.rejected('PROFILE_LOCK_HASH_INVALID',lambda:guard.validate_profile(PROFILE))

    def test_lock_direct_file_or_missing_hash_rejected(self):
        raw=(PROFILE/'requirements.lock').read_bytes()
        for changed in (raw.replace(b'paypal-agent-toolkit==1.11.0',b'paypal-agent-toolkit @ file:///untrusted.whl'),b'package==1.0 \\\n'):
            with self.subTest():self.rejected('PROFILE_LOCK_INVALID',lambda:guard.parse_lock(changed))

    def test_lock_toolkit_hash_preserved(self):
        raw=(PROFILE/'requirements.lock').read_bytes().replace(guard.TOOLKIT_WHEEL_SHA256.encode(),b'0'*64)
        self.rejected('PROFILE_TOOLKIT_HASH_INVALID',lambda:guard.parse_lock(raw))

    def test_project_marker_missing_rejected(self):
        with patch.object(Path,'read_bytes',side_effect=FileNotFoundError):
            self.rejected('PROFILE_PROJECT_MISMATCH',lambda:guard.validate_project(PROFILE))

    def test_project_marker_hash_mismatch_rejected(self):
        with patch.object(Path,'read_bytes',return_value=b'forged project'):
            self.rejected('PROFILE_PROJECT_MISMATCH',lambda:guard.validate_project(PROFILE))

    def marker_root(self, temporary):
        source_root=PROFILE.parent.parent
        root=Path(temporary)
        for relative in guard.PROJECT_MARKERS:
            target=root/relative;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source_root/relative,target)
        target=root/'tests/test_paypal_tools.py';target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text('"""Marker fixture."""\n')
        return root

    def test_stable_public_runner_marker_accepts_canonical_and_exported_layouts(self):
        with tempfile.TemporaryDirectory(prefix='paypal-toolkit-marker-') as temporary:
            root=self.marker_root(temporary)
            self.assertEqual(guard.validate_project_root(root),root)
            shutil.copyfile(root/'tools/public_run.sh',root/'tools/run.sh')
            self.assertEqual((root/'tools/public_run.sh').read_bytes(),(root/'tools/run.sh').read_bytes())
            self.assertEqual(guard.validate_project_root(root),root)

    def test_stable_public_runner_marker_rejects_missing_or_mismatch(self):
        for mutation in ('missing','mismatch'):
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory(prefix='paypal-toolkit-marker-') as temporary:
                root=self.marker_root(temporary);runner=root/'tools/public_run.sh'
                if mutation=='missing':runner.unlink()
                else:runner.write_bytes(runner.read_bytes()+b' ')
                self.rejected('PROFILE_PROJECT_MISMATCH',lambda:guard.validate_project_root(root))

    def test_manifest_and_guard_pin_same_public_runner(self):
        manifest=guard.tomllib.loads((PROFILE/'pyproject.toml').read_text())
        markers=manifest['tool']['payguard-paypal-toolkit']['project-markers']
        self.assertEqual(markers,guard.PROJECT_MARKERS)
        self.assertIn('tools/public_run.sh',markers)
        self.assertNotIn('tools/run.sh',markers)

    def test_guard_extra_arguments_before_import(self):
        with patch.object(guard,'check',side_effect=AssertionError('must not dispatch')):
            self.assertEqual(guard.main(['extra']),64)

    def launch(self,args,interpreter,extra=None):
        env={'PATH':'/usr/bin:/bin','PAYGUARD_PAYPAL_TOOLKIT_PYTHON_BIN':str(interpreter)}
        env.update(extra or {})
        return subprocess.run(['/bin/sh',str(PROFILE/'run.sh'),*args],env=env,text=True,capture_output=True,timeout=30)

    def test_launcher_missing_runtime_failclosed(self):
        result=self.launch(['check'],PROFILE/'MISSING_TEST_INTERPRETER')
        self.assertEqual(result.returncode,78);self.assertIn('PROFILE_RUNTIME_MISSING',result.stderr)

    def test_launcher_unknown_and_extra_before_interpreter(self):
        for args in (['unknown'],['api'],['api','extra'],['test','extra'],['help','extra']):
            result=self.launch(args,PROFILE/'MISSING_TEST_INTERPRETER')
            self.assertEqual(result.returncode,64)
            self.assertNotIn('RUNTIME_MISSING',result.stderr)

    def test_launcher_explicit_override_runs_only_profile_tests(self):
        # Test double covers shell selection only; real guard tested separately.
        with tempfile.TemporaryDirectory(prefix='.runtime-test-') as directory:
            fixture=Path(directory);calls=fixture/'calls';python=fixture/'python'
            python.write_text('#!/bin/sh\nprintf "%s\\n" "$*" "TRACE=$OPENAI_AGENTS_DISABLE_TRACING" >> "$PROFILE_TEST_CALLS"\nexit 0\n')
            python.chmod(0o755)
            result=self.launch(['test'],python,{'PROFILE_TEST_CALLS':str(calls)})
            self.assertEqual(result.returncode,0,result.stderr)
            observed=calls.read_text().splitlines()
            self.assertEqual(len(observed),4)
            self.assertIn('-I -B '+str(PROFILE/'check_runtime.py'),observed)
            self.assertIn('-I -B -m unittest discover -s '+str(PROFILE)+' -p test_runtime.py -v',observed)
            self.assertEqual(observed.count('TRACE=1'),2)
            joined='\n'.join(observed)
            self.assertNotIn('-m unittest discover -s tests -v',joined)
            self.assertNotIn('ROOT_PYTHON=',joined)
            self.assertNotIn('uvicorn',joined)

    def test_launcher_propagates_profile_test_failure(self):
        with tempfile.TemporaryDirectory(prefix='.runtime-test-') as directory:
            fixture=Path(directory);python=fixture/'python'
            python.write_text('#!/bin/sh\ncase "$*" in *"-m unittest discover"*) exit 23 ;; *) exit 0 ;; esac\n')
            python.chmod(0o755)
            result=self.launch(['test'],python)
            self.assertEqual(result.returncode,23)

if __name__=='__main__':
    unittest.main()
