"""Check runtime import isolation in a fresh Python process."""
import subprocess
import sys
import unittest
from pathlib import Path


class RuntimeImportTests(unittest.TestCase):
    def test_runtime_imports_do_not_load_app_or_streamlit(self):
        result = subprocess.run(
            [sys.executable, "-c", """
import sys
import runtime_host
import m1
import t8
import t9

assert m1.host is t8.host is t9.host is runtime_host
unexpected = [name for name in sys.modules
              if name == 'app' or name == 'streamlit' or name.startswith('streamlit.')]
assert not unexpected, unexpected
"""],
            cwd=Path(__file__).resolve().parents[2],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
