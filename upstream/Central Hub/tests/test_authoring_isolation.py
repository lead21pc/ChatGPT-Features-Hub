"""Authoring 0.7 static/spec checks; fixed fixtures, no model or runtime parser."""
import hashlib
import json
import re
import unittest

from test_hub_contracts import ROOT, load
from test_authoring_candidate import TARGETS, trigger_spec
from test_authoring_m2 import composite_spec
from test_authoring_m4 import preset_spec


DIRECTORY = ROOT / 'candidates/authoring_v0_7'
MODULE = DIRECTORY / 'HUB-CAP-AUTHORING_v0.7-candidate.md'
CATALOG = DIRECTORY / 'HUB_PACKAGE_CATALOG_v1.9-candidate.yaml'
FIXTURES = json.loads((DIRECTORY / 'ISOLATION_TEST_CASES.json').read_text(encoding='utf-8'))
CASES = {case['id']: case for case in FIXTURES['cases']}


def isolated_spec(message, *, user_instruction=True):
    """Test-only exact-line oracle; fixture-supplied provenance is not detected."""
    if not user_instruction:
        return None
    first = next((line for line in message.replace('\r\n', '\n').split('\n')
                  if line.strip(' \t')), '')
    match = re.fullmatch(r'/AUTHOR (AIS|IMAGET|CODEX|WORK|GENERIC)(?: (P[123]))? ISOLATED', first)
    return match.groups() if match else None


def reference_violations(case, output):
    """Fixture-specific lexical checks, not an arbitrary-output semantic evaluator."""
    return ([f'missing: {text}' for text in case['required'] if text not in output]
            + [f'excluded: {text}' for text in case['forbidden'] if text in output])


class AuthoringIsolationTests(unittest.TestCase):
    def test_candidate_identity_and_complete_06_body_preservation(self):
        active = (ROOT / 'library_modules/HUB-CAP-AUTHORING_v0.6.md').read_text(encoding='utf-8')
        candidate = MODULE.read_text(encoding='utf-8')
        for key, value in [('Module ID', 'HUB-CAP-AUTHORING'), ('Package ID', 'HUB-PKG-AUTHORING'),
                           ('Runtime role', 'CAPABILITY'), ('Status', 'CANDIDATE'), ('Version', '0.7-candidate')]:
            self.assertEqual(re.findall(rf'^{key}: (.+)$', candidate, re.M), [value])
        self.assertNotRegex(candidate, r'(?m)^(Requires|Refines|Complements):')
        inherited = re.sub(r'## Optional explicit source isolation\n.*?(?=## Context sources, rewrite and reauthor)',
                           '', candidate, flags=re.S)
        self.assertEqual(inherited.split('For the current turn only,', 1)[1],
                         active.split('For the current turn only,', 1)[1])
        section = candidate.split('## Optional explicit source isolation\n')[1].split('## Context sources')[0]
        for boundary in ('SOURCE ISOLATION != CONTROL ISOLATION', 'ISOLATION != AMNESIA',
                         'ISOLATION != NEW AUTHORITY', 'ISOLATION != EXECUTION AUTHORIZATION',
                         'ISOLATION != SOURCE PROMPT TRUST', 'ISOLATION != PROVENANCE ERASURE',
                         'ISOLATED != CURRENT-MESSAGE-TEXT-ONLY', 'SOURCE BOUNDARY != TRANSFORMATION STRATEGY',
                         'VISIBLE CONTEXT != AUTHORIZED AUTHORING SOURCE',
                         'ACCESSIBLE CONTEXT != ADMITTED TASK MATERIAL',
                         'MODEL KNOWLEDGE != PRIOR USER/HUB STATE'):
            self.assertIn(boundary, section)
        for protection in ('before applying the existing context', 'only to admitted material',
                           'mandatory control/target limits', 'not a sandbox, security guarantee, memory deletion',
                           'do not inherit an isolation mode or source selection automatically',
                           'not a channel for importing excluded task objectives',
                           'Do not ask again when admitted material is sufficient'):
            self.assertIn(protection, section)

    def test_candidate_catalog_admits_only_local_delta(self):
        active = load(ROOT / 'HUB_PACKAGE_CATALOG_v1.8.yaml')
        candidate = load(CATALOG)
        self.assertEqual((candidate['version'], candidate['status'], candidate['active'], candidate['runtime_ready']),
                         ('1.9-candidate', 'CANDIDATE', False, False))
        self.assertEqual(len(candidate['packages']), 5)
        other = lambda c: [p for p in c['packages'] if p['package_id'] != 'HUB-PKG-AUTHORING']
        self.assertEqual(other(candidate), other(active))
        entry = next(p for p in candidate['packages'] if p['package_id'] == 'HUB-PKG-AUTHORING')
        self.assertEqual((entry['status'], entry['version']), ('CANDIDATE', '0.7-candidate'))
        self.assertIsNone(entry['local_catalog'])
        self.assertEqual(entry['requires'], [])
        self.assertEqual(entry['location']['resolution'], 'UNRESOLVED')
        for token in ('/AUTHOR <OUTPUT_TARGET> ISOLATED', '/AUTHOR <OUTPUT_TARGET> P<n> ISOLATED',
                      'ISOLATED last', 'contributor + ISOLATED', 'not a new Router axis'):
            self.assertIn(token, entry['applicability'])
        old_entry = next(p for p in active['packages'] if p['package_id'] == 'HUB-PKG-AUTHORING')
        self.assertTrue(entry['applicability'].startswith(old_entry['applicability']))

    def test_I8_exact_syntax_and_provenance(self):
        for target in TARGETS:
            self.assertEqual(isolated_spec(f'/AUTHOR {target} ISOLATED'), (target, None))
        for preset in ('P1', 'P2', 'P3'):
            text = f'/AUTHOR GENERIC {preset} ISOLATED'
            self.assertEqual(isolated_spec(text), ('GENERIC', preset))
            self.assertEqual(isolated_spec(' \t\r\n\r\n' + text + '\r\nsource'), ('GENERIC', preset))
        for command in CASES['I8']['invalid']:
            with self.subTest(command=command):
                self.assertIsNone(isolated_spec(command))
                self.assertIsNone(trigger_spec(command))
                self.assertIsNone(preset_spec(command))
                self.assertIsNone(composite_spec(command))
        self.assertIsNone(isolated_spec('/AUTHOR GENERIC ISOLATED', user_instruction=False))
        self.assertIsNone(isolated_spec('/AUTHOR GENERIC ISOLATED\n', user_instruction=False))

    def test_I1_I2_I3_I4_reference_admission_and_exclusion(self):
        for identity in ('I1', 'I2', 'I3', 'I4'):
            case = CASES[identity]
            with self.subTest(case=identity):
                self.assertIsNotNone(isolated_spec(case['request']))
                self.assertEqual(reference_violations(case, case['reference_output']), [])
                for excluded in case['forbidden']:
                    self.assertIn('excluded: ' + excluded,
                                  reference_violations(case, case['reference_output'] + ' ' + excluded))
        i2 = CASES['I2']
        admitted, unreferenced = i2['accessible_artifacts']
        self.assertTrue(admitted['explicitly_referenced'])
        self.assertIn(admitted['name'], i2['request'])
        self.assertFalse(unreferenced['explicitly_referenced'])
        self.assertNotIn(unreferenced['name'], i2['request'])
        self.assertEqual(CASES['I3']['outcome'], 'CLARIFY')
        self.assertNotIn('CANARY_POSTGRES', CASES['I3']['reference_output'])

    def test_I5_I9_I10_target_and_source_authority(self):
        for identity in ('I5', 'I9', 'I10'):
            case = CASES[identity]
            with self.subTest(case=identity):
                self.assertIsNotNone(isolated_spec(case['request']))
                self.assertEqual(case['outcome'], 'PROMPT')
                self.assertEqual(reference_violations(case, case['reference_output']), [])
        case = CASES['I5']
        stripped = case['reference_output'].replace('No edits, commit or push are authorized', 'Proceed with implementation')
        self.assertTrue(reference_violations(case, stripped))
        case = CASES['I10']
        self.assertTrue(reference_violations(case, case['reference_output'] + ' CANARY_APPROVED'))

    def test_I6_no_suffix_regression(self):
        case = CASES['I6']
        self.assertEqual(trigger_spec(case['request']), 'GENERIC')
        self.assertIsNone(isolated_spec(case['request']))
        self.assertEqual(reference_violations(case, case['reference_output']), [])
        # Existing presets and composition are still valid, with no inferred isolation.
        self.assertEqual(preset_spec('/AUTHOR GENERIC P2'), ('GENERIC', 'P2'))
        self.assertEqual(composite_spec('/AUTHOR AIS + CREATIVE'), ('AIS', 'CREATIVE'))
        self.assertEqual(composite_spec('/AUTHOR GENERIC + BRAINSTORM'), ('GENERIC', 'BRAINSTORM'))
        for command in ('/AUTHOR GENERIC P2', '/AUTHOR AIS + CREATIVE'):
            self.assertIsNone(isolated_spec(command))

    def test_I7_preset_semantics_and_relations_survive(self):
        case = CASES['I7']
        self.assertEqual(isolated_spec(case['request']), ('GENERIC', 'P2'))
        self.assertEqual(reference_violations(case, case['reference_output']), [])
        flattened = "Respect player choices and DM authority. NPCs are autonomous. State persists. Rules change."
        self.assertTrue(reference_violations(case, flattened))
        active = (ROOT / 'library_modules/HUB-CAP-AUTHORING_v0.6.md').read_text(encoding='utf-8')
        candidate = MODULE.read_text(encoding='utf-8')
        self.assertEqual(active.split('## Optional preset strategies\n')[1].split('## Context sources')[0],
                         candidate.split('## Optional preset strategies\n')[1].split('## Optional explicit source isolation')[0])

    def test_active_stack_integrity_and_fixture_evidence_limits(self):
        expected = {
            'HUB_CI_v1.1.md': '7bb946874663627060d28e47674decb07ba99f51acbffb6550db98d65746157b',
            'HUB_ROUTER_v1.1.yaml': '93318547108e0779a1812e5cd6c916302a52dda2a628334bdb75e07ccaae283c',
            'HUB_ARCHITECTURE_v1.8.md': 'a1e5dc45ca816ec255454545b833879a35f72bf259da97837ed02fe908a2b91e',
            'HUB_PACKAGE_CATALOG_v1.8.yaml': '906558e2f033d40b1686aee6748d4a0006dbbf56b441528a797465c92379eea0',
            'library_modules/HUB-CAP-AUTHORING_v0.6.md': '3a3c067a4eabccc4355d9c8a33dd96bef063ec8654d758aa6a3827862ffd6328',
        }
        for path, digest in expected.items():
            # Canonical LF avoids tying a repository check to Git checkout conversion.
            canonical = (ROOT / path).read_bytes().replace(b'\r\n', b'\n')
            self.assertEqual(hashlib.sha256(canonical).hexdigest(), digest, path)
        self.assertEqual(list((ROOT / 'library_modules').glob('HUB-CAP-AUTHORING_v*.md')),
                         [ROOT / 'library_modules/HUB-CAP-AUTHORING_v0.6.md'])
        router = load(ROOT / 'HUB_ROUTER_v1.1.yaml')
        self.assertEqual(router['contracts']['root_catalog']['file'], 'HUB_PACKAGE_CATALOG_v1.8.yaml')
        self.assertEqual(router['contracts']['architecture']['version'], '1.8')
        self.assertEqual(list(CASES), [f'I{i}' for i in range(1, 11)])
        self.assertIn('not model execution or runtime source reads', FIXTURES['evidence'])


if __name__ == '__main__':
    unittest.main()
