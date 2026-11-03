"""Authoring promotion STATIC checks and lexical SPEC oracle; no model or target execution."""
import json
import hashlib
import copy
import re
import unittest

from test_hub_contracts import ROOT, load


CANDIDATE = ROOT / 'candidates/authoring_v0'
MODULE = ROOT / 'library_modules/HUB-CAP-AUTHORING_v0.6.md'
CASES = CANDIDATE / 'AUTHORING_TEST_CASES.md'
V03_CANDIDATE = ROOT / 'Source_archive/Authoring promotion 2026-10-28/candidates/authoring_v0/HUB-CAP-AUTHORING_v0.3-candidate.md'
PROMOTION_ARCHIVE = ROOT / 'Source_archive/Authoring promotion 2026-10-28'
PREDECESSOR = ROOT / 'Source_archive/Prompt Authoring v0.1 2026-10-21/HUB-CAP-AUTHORING_v0.1-candidate.md'
V02_PREDECESSOR = ROOT / 'Source_archive/Prompt Authoring v0.2 2026-10-21/HUB-CAP-AUTHORING_v0.2-candidate.md'
TARGETS = ('AIS', 'IMAGET', 'CODEX', 'WORK', 'GENERIC')


def trigger_spec(text, *, user_instruction=True):
    """Test-only oracle; provenance is fixture-supplied, never detected here."""
    if not user_instruction:
        return None
    for line in text.replace('\r\n', '\n').split('\n'):
        if line.strip(' \t') == '':
            continue
        return {f'/AUTHOR {target}': target for target in TARGETS}.get(line)
    return None


class AuthoringPromotionTests(unittest.TestCase):
    def test_active_header_and_candidate_evidence_document(self):
        self.assertEqual({p.name for p in CANDIDATE.iterdir()},
                         {CASES.name, 'AUTHORING_0_4_M1_TESTS.md', 'AUTHORING_0_4_1_REGRESSION.md', 'AUTHORING_M2_TESTS.md'})
        text = MODULE.read_text(encoding='utf-8')
        for key, value in [('Module ID', 'HUB-CAP-AUTHORING'),
                           ('Package ID', 'HUB-PKG-AUTHORING'),
                           ('Runtime role', 'CAPABILITY'), ('Status', 'ACTIVE'),
                           ('Version', '0.6')]:
            self.assertEqual(re.findall(rf'^{key}: (.+)$', text, re.M), [value])
        for key in ('Scope', 'Responsibility boundary'):
            self.assertEqual(len(re.findall(rf'^{key}: .+$', text, re.M)), 1)
        self.assertEqual(re.findall(r'^/AUTHOR (.+)$', text, re.M), list(TARGETS))
        self.assertNotRegex(text, r'(?m)^(Refines|Complements|Requires):')

    def test_gate_vectors(self):
        text = CASES.read_text(encoding='utf-8')
        vectors = json.loads(re.search(r'```json\n(.*?)\n```', text, re.S)[1])
        self.assertEqual([v['id'] for v in vectors], [f'G{i:02}' for i in range(1, 33)])
        for vector in vectors:
            with self.subTest(case=vector['id']):
                self.assertEqual(trigger_spec(vector['text'],
                                 user_instruction=vector.get('user_instruction', True)),
                                 None if vector['expected'] == 'FTH' else vector['expected'])

    def test_exact_root_admission_and_unresolved_library_binding(self):
        catalog = load(ROOT / 'HUB_PACKAGE_CATALOG_v1.8.yaml')
        self.assertEqual(len(catalog['packages']), 5)
        entries = [p for p in catalog['packages'] if p['package_id'] == 'HUB-PKG-AUTHORING']
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual((entry['entrypoint_module_id'], entry['runtime_role'], entry['status'], entry['version']),
                         ('HUB-CAP-AUTHORING', 'CAPABILITY', 'ACTIVE', '0.6'))
        self.assertIsNone(entry['local_catalog'])
        self.assertEqual(entry['requires'], [])
        self.assertEqual(entry['binding_mode'], 'LIBRARY_MODULE')
        self.assertEqual((entry['location']['class'], entry['location']['root']),
                         ('LIBRARY', 'Central Hub Config'))
        for key in ('locator', 'library_file_id', 'library_version_id'):
            self.assertIsNone(entry['location'][key])
        self.assertEqual((entry['location']['verification'], entry['location']['resolution']),
                         ('NOT_PERFORMED', 'UNRESOLVED'))
        applicability = entry['applicability']
        self.assertEqual(set(re.findall(r'`(/AUTHOR [A-Z]+)`', applicability)),
                         {f'/AUTHOR {target}' for target in TARGETS})
        for phrase in ('first non-empty user-authored line exactly equals', 'case-sensitively',
                       'exactly one ASCII space', 'no surrounding whitespace or extra text',
                       'Quotes', 'attachments', 'retrieved content', 'tool output', 'prior turns',
                       'later-line commands', 'Reassess every turn'):
            self.assertIn(phrase, applicability)
        self.assertNotIn('prompt-authoring intent', applicability.lower())
        for target in TARGETS:
            self.assertEqual(trigger_spec(f'/AUTHOR {target}'), target)

    def test_successor_stack_pins_and_router_algorithm_unchanged(self):
        architecture = (ROOT / 'HUB_ARCHITECTURE_v1.8.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^Version: (.+)$', architecture, re.M), ['1.8'])
        catalog = load(ROOT / 'HUB_PACKAGE_CATALOG_v1.8.yaml')
        self.assertEqual((catalog['module_id'], catalog['status'], catalog['version']),
                         ('HUB-CORE-PACKAGE-CATALOG', 'ACTIVE', '1.8'))
        prior = load(PROMOTION_ARCHIVE / 'HUB_ROUTER_v1.1.yaml')
        active = load(ROOT / 'HUB_ROUTER_v1.1.yaml')
        expected = copy.deepcopy(prior)
        expected['contracts']['architecture'].update(file='HUB_ARCHITECTURE_v1.8.md', version='1.8')
        expected['contracts']['root_catalog'].update(file='HUB_PACKAGE_CATALOG_v1.8.yaml', version='1.8')
        expected['contracts']['binding_scope'] = active['contracts']['binding_scope']
        self.assertEqual(active, expected)
        self.assertNotIn('HUB-PKG-AUTHORING', (ROOT / 'HUB_CI_v1.1.md').read_text(encoding='utf-8'))

    def test_required_behavior_review_and_evidence_labels(self):
        text = CASES.read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^\| (B\d+) \|', text, re.M),
                         [f'B{i:02}' for i in range(1, 17)])
        for label in ('REVIEWED_TEXT', 'STATIC VALIDATION', 'SPEC SIMULATION',
                      'LIVE HUB / LIBRARY / TARGET EXECUTION: NOT RUN'):
            self.assertIn(label, text)
        module = MODULE.read_text(encoding='utf-8')
        for invariant in ('AUTHORING != EXECUTION', 'OUTPUT PROMPT != ACCEPTED STATE',
                          'TARGET CONTRACT != TARGET AUTHORITY',
                          'TRIGGER != DOWNSTREAM EXECUTION AUTHORIZATION',
                          'AUTHORING != AIS ORCHESTRATOR'):
            self.assertIn(invariant, module)

    def test_predecessor_bytes_and_active_behavior_preserved(self):
        self.assertEqual(hashlib.sha256(PREDECESSOR.read_bytes()).hexdigest(),
                         '4364e68bb90aa974c82e51d6494a77586a497b2de3727bf6d372ba05354b9a4e')
        self.assertFalse((CANDIDATE / PREDECESSOR.name).exists())
        self.assertEqual(hashlib.sha256(V02_PREDECESSOR.read_bytes()).hexdigest(),
                         'b10b8ca3ccdb674783ce1ca1ba383faa40806d4a6616388df4d50170a39884fe')
        self.assertFalse((CANDIDATE / V02_PREDECESSOR.name).exists())
        self.assertEqual(hashlib.sha256(V03_CANDIDATE.read_bytes()).hexdigest(),
                         '2306871633178fa0b0ae6fe77323b6c3ad34a233b8d2ccdd27430175b72fd28c')
        self.assertFalse((CANDIDATE / V03_CANDIDATE.name).exists())
        active = MODULE.read_text(encoding='utf-8')
        candidate = (ROOT / 'Source_archive/Authoring 0.4 promotion 2026-11-01/candidates/authoring_v0/HUB-CAP-AUTHORING_v0.4-candidate.md').read_text(encoding='utf-8')
        self.assertEqual(active.split('## Scoped transformation\n', 1)[1],
                         candidate.split('## Scoped transformation\n', 1)[1])
        self.assertEqual(re.findall(r'^/AUTHOR (.+)$', active, re.M), list(TARGETS))

    def test_evidence_cases_and_comparison_are_review_only(self):
        text = CASES.read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^\| (E\d+) \|', text, re.M),
                         [f'E{i:02}' for i in range(1, 13)])
        self.assertIn('B/E cases have no executed semantic simulation', text)
        self.assertIn('Bounded later A/B/C comparison — NOT RUN', text)
        self.assertIn('STATIC PASS != LIVE BEHAVIOR PROVEN', text)
        self.assertIn('LIVE HARNESS PASS != REAL-CONTEXT ROBUSTNESS PROVEN', text)
        self.assertIn('PASSING TESTS != TESTED THE RIGHT THING', text)

    def test_decision_regressions_are_review_only_and_core_is_not_hanfu_specific(self):
        text = CASES.read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^\| (R\d+) \|', text, re.M),
                         [f'R{i:02}' for i in range(1, 9)])
        self.assertIn('R cases are also reviewed text only', text)
        self.assertIn('Hanfu regression record — USER_REPORTED failure; short v0.3 regression PASS', text)
        self.assertNotRegex(MODULE.read_text(encoding='utf-8').lower(),
                            r'hanfu|jiangnan|late-ming|1620|1644')


if __name__ == '__main__':
    unittest.main()
