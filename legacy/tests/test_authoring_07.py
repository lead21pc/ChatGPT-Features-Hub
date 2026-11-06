"""Active 0.7 contracts and test-only lexical oracle; no production trigger parsing."""
import hashlib
import json
import re
import unittest
from pathlib import Path

import runtime_host
import t8
import t9

HUB = Path(__file__).resolve().parents[1] / "upstream" / "Central Hub"
OLD = HUB / 'Source_archive/Authoring 0.7 M2 2026-11-05'
CANDIDATE = HUB / 'candidates/authoring_v0_7'


def isolated_spec(message):
    first = next((line for line in message.replace('\r\n', '\n').split('\n') if line.strip(' \t')), '')
    match = re.fullmatch(r'/AUTHOR (AIS|IMAGET|CODEX|WORK|GENERIC)(?: (P[123]))? ISOLATED', first)
    return match.groups() if match else None


class Authoring07Contracts(unittest.TestCase):
    def test_active_semantics_exactly_match_live_tested_candidate(self):
        active = (HUB / 'library_modules/HUB-CAP-AUTHORING_v0.7.md').read_text(encoding='utf-8')
        candidate = (CANDIDATE / 'HUB-CAP-AUTHORING_v0.7-candidate.md').read_text(encoding='utf-8')
        self.assertEqual(active.split('For the current turn only,')[1], candidate.split('For the current turn only,')[1])
        self.assertIn('Status: ACTIVE\nVersion: 0.7', active)
        self.assertEqual(list((HUB / 'library_modules').glob('HUB-CAP-AUTHORING_v*.md')),
                         [HUB / 'library_modules/HUB-CAP-AUTHORING_v0.7.md'])
        without_isolation = re.sub(r'## Optional explicit source isolation\n.*?(?=## Context sources, rewrite and reauthor)', '', active, flags=re.S)
        predecessor = (OLD / 'library_modules/HUB-CAP-AUTHORING_v0.6.md').read_text(encoding='utf-8')
        self.assertEqual(without_isolation.split('For the current turn only,')[1], predecessor.split('For the current turn only,')[1])

    def test_exact_activation_and_malformed_forms_spec_only(self):
        for target in ('AIS', 'IMAGET', 'CODEX', 'WORK', 'GENERIC'):
            for preset in (None, 'P1', 'P2', 'P3'):
                suffix = '' if preset is None else f' {preset}'
                text = f'/AUTHOR {target}{suffix} ISOLATED\nCreate a prompt.'
                self.assertEqual(isolated_spec(text), (target, preset))
                self.assertEqual(isolated_spec(' \t\r\n' + text), (target, preset))
            self.assertIsNone(isolated_spec(f'/AUTHOR {target}'))
        cases = json.loads((CANDIDATE / 'ISOLATION_TEST_CASES.json').read_text(encoding='utf-8'))['cases']
        for text in next(c for c in cases if c['id'] == 'I8')['invalid']:
            with self.subTest(text=text):
                self.assertIsNone(isolated_spec(text))
        self.assertIsNone(isolated_spec('/AUTHOR GENERIC\nISOLATED'))

    def test_minimum_catalog_router_delta_and_unchanged_other_packages(self):
        old = (OLD / 'HUB_PACKAGE_CATALOG_v1.8.yaml').read_text(encoding='utf-8')
        new = (HUB / "HUB_PACKAGE_CATALOG_v1.9.yaml").read_text(encoding='utf-8')
        def other(text):
            first, rest = text.split('- package_id: HUB-PKG-AUTHORING\n', 1)
            return first.split('packages:\n')[1], rest.split('- package_id: HUB-PKG-AIS\n')[1]
        self.assertEqual(other(old), other(new))
        identity = runtime_host.t7_catalog_identities(new, 'packages', 'package_id')[t8.AUTHORING]
        self.assertEqual((identity['version'], identity['status'], identity['runtime_role']), ('0.7', 'ACTIVE', 'CAPABILITY'))
        self.assertIn('ISOLATED last', new)
        self.assertIn('contributor + ISOLATED', new)
        self.assertEqual((HUB / "HUB_ROUTER_v1.1.yaml").read_text(encoding='utf-8'),
                         (OLD / 'HUB_ROUTER_v1.1.yaml').read_text(encoding='utf-8').replace('1.8', '1.9'))

    def test_archive_receipt_and_runtime_bindings(self):
        receipt = json.loads((OLD / 'ARCHIVE_RECEIPT.json').read_text(encoding='utf-8'))
        for path, digest in receipt.items():
            self.assertEqual(hashlib.sha256((OLD / path).read_bytes()).hexdigest(), digest)
        runtime = Path('runtime/packages/authoring/HUB-CAP-AUTHORING_v0.7.md')
        self.assertEqual(runtime.read_bytes(), (HUB / 'library_modules' / runtime.name).read_bytes())
        for path in (t8.BINDINGS_PATH, t9.BINDINGS_PATH):
            manifest = json.loads(path.read_text(encoding='utf-8'))
            entry = manifest['packages'][t8.AUTHORING]['entrypoint']
            self.assertEqual(entry['version'], '0.7')
            self.assertEqual(entry['sha256'], hashlib.sha256(runtime.read_bytes()).hexdigest())
        t9.load_bindings(t9.BINDINGS_PATH.read_text(encoding='utf-8'))
        archived_runtime = runtime.parent / 'source_archive/HUB-CAP-AUTHORING_v0.6.md'
        self.assertEqual(hashlib.sha256(archived_runtime.read_bytes()).hexdigest(),
                         receipt['library_modules/HUB-CAP-AUTHORING_v0.6.md'])


if __name__ == '__main__':
    unittest.main()
