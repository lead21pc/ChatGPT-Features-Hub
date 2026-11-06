"""Network-blocked local suite, focused upstream specs, compilation and diff verification."""
import hashlib
import json
import py_compile
import socket
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
OUT = Path(__file__).resolve().parent


def run():
    record = dict(evidence_class='STATIC/SPEC', timestamp_utc=datetime.now(timezone.utc).isoformat())
    with (OUT / 'local_static.txt').open('w', encoding='utf-8') as log:
        with patch.object(socket.socket, 'connect', side_effect=AssertionError('Static tests forbid network')):
            result = unittest.TextTestRunner(stream=log, verbosity=2).run(
                unittest.defaultTestLoader.discover(str(ROOT / 'legacy/tests'), pattern='test_*.py'))
    record['local'] = dict(tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                           socket_connect='BLOCKED', passed=result.wasSuccessful())
    tests = ROOT / 'legacy/upstream/Central Hub/tests'
    sys.path.insert(0, str(tests))
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(name) for name in (
        'test_authoring_candidate', 'test_authoring_m1', 'test_authoring_m2',
        'test_authoring_m4', 'test_authoring_isolation'))
    with (OUT / 'focused_upstream.txt').open('w', encoding='utf-8') as log:
        with patch.object(socket.socket, 'connect', side_effect=AssertionError('Static specs forbid network')):
            result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    record['focused_upstream'] = dict(tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                                      passed=result.wasSuccessful())
    paths = [p for p in ROOT.rglob('*.py') if '.git' not in p.parts and '__pycache__' not in p.parts]
    for path in paths:
        py_compile.compile(str(path), doraise=True)
    record['compile'] = dict(files=len(paths), passed=True)
    diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
    record['diff_check'] = dict(passed=diff.returncode == 0, output=diff.stdout + diff.stderr)
    record['versions'] = dict(authoring='0.7', architecture='1.9', catalog='1.9', router='1.1', ci='1.1')
    record['source_hashes'] = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths + [ROOT / 'runtime/HUB_LOCAL_BINDINGS_v0.3.json',
                          ROOT / 'legacy/upstream/Central Hub/library_modules/HUB-CAP-AUTHORING_v0.7.md']}
    record['passed'] = all(record[k]['passed'] for k in ('local', 'focused_upstream', 'compile', 'diff_check'))
    (OUT / 'static_summary.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in record.items() if k != 'source_hashes'}, indent=2))
    raise SystemExit(not record['passed'])


if __name__ == '__main__':
    run()
