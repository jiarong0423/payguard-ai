"""The hosted demo image ships src/, backend/, data/ and policies/ only; the app must import without tools/."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class HostedImageLayoutTests(unittest.TestCase):
    def test_app_imports_and_answers_health_without_tools_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("src", "backend", "data", "policies"):
                shutil.copytree(ROOT / name, Path(tmp) / name, ignore=shutil.ignore_patterns("__pycache__"))
            script = (
                "from fastapi.testclient import TestClient\n"
                "from app.main import create_app\n"
                "client = TestClient(create_app(), base_url='https://payguard-demo.onrender.com',"
                " client=('127.0.0.1', 1))\n"
                "print(client.get('/api/v1/health').status_code)\n"
            )
            env = {key: value for key, value in os.environ.items() if not key.startswith("PAYGUARD_")}
            env.update(PYTHONPATH=f"{tmp}/src:{tmp}/backend", PYTHONDONTWRITEBYTECODE="1",
                       PAYGUARD_DEMO_MODE="public", PAYGUARD_PUBLIC_HOST="payguard-demo.onrender.com",
                       PAYGUARD_STATIC_DIR=str(Path(tmp) / "no-build"))
            result = subprocess.run([sys.executable, "-c", script], cwd=tmp, env=env,
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr[-800:])
            self.assertIn(result.stdout.strip().splitlines()[-1], {"200", "403"})
            self.assertFalse((Path(tmp) / "tools").exists())


    def test_every_dockerfile_copy_source_survives_dockerignore(self):
        # .dockerignore is default-deny; a COPY source missing from its allow list fails the image build.
        allowed = [line[1:].rstrip("/") for line in (ROOT / ".dockerignore").read_text().splitlines() if line.startswith("!")]
        sources = []
        for line in (ROOT / "Dockerfile").read_text().splitlines():
            parts = line.split()
            if parts[:1] == ["COPY"] and not any(part.startswith("--from") for part in parts):
                sources += parts[1:-1]
        self.assertTrue(sources)
        for source in sources:
            self.assertTrue(any(source == item or source.startswith(item + "/") for item in allowed),
                            f"{source} is copied by the Dockerfile but excluded by .dockerignore")


if __name__ == "__main__":
    unittest.main()
