"""Three M2 static/spec checks; no model routing or generated-prompt evaluation."""
import hashlib
import re
import unittest

from test_hub_contracts import ROOT, load

# Historical 0.6/1.8 baseline; active 0.7 is checked in test_authoring_07.py.
PREDECESSOR = ROOT / 'Source_archive/Authoring 0.7 M2 2026-11-05'
from test_authoring_candidate import trigger_spec

ARCHIVE = ROOT / 'Source_archive/Authoring 0.5 M2 2026-11-01'
MODULE = PREDECESSOR / 'library_modules/HUB-CAP-AUTHORING_v0.6.md'


def composite_spec(message, *, user_instruction=True):
    """Lexical oracle only; fixture supplies provenance, not live provenance detection."""
    if not user_instruction:
        return None
    first = next((line for line in message.replace('\r\n', '\n').split('\n')
                  if line.strip(' \t')), '')
    match = re.fullmatch(r'/AUTHOR (AIS|IMAGET|CODEX|WORK|GENERIC) \+ (CREATIVE|BRAINSTORM)', first)
    return match.groups() if match else None


class AuthoringM2Tests(unittest.TestCase):
    def test_C1_explicit_relation_contract_and_owner_metadata(self):
        text = MODULE.read_text(encoding='utf-8')
        self.assertEqual(composite_spec('/AUTHOR AIS + CREATIVE\nAIS verifies; Creative stays in open scope.'),
                         ('AIS', 'CREATIVE'))
        for phrase in ('CONTRIBUTOR != TARGET', 'COMPOSITION != DEPENDENCY',
                       'COMPOSITION != AUTHORITY MERGE', 'COMPOSITION != EXECUTION',
                       'proceed without asking again', 'one self-contained prompt',
                       'Missing, mismatched, unavailable or unresolved requested contribution blocks'):
            self.assertIn(phrase, text)
        old = load(ARCHIVE / 'HUB_PACKAGE_CATALOG_v1.5.yaml')
        new = load(PREDECESSOR / 'HUB_PACKAGE_CATALOG_v1.8.yaml')
        self.assertEqual([p for p in old['packages'] if p['package_id'] not in {'HUB-PKG-AUTHORING', 'HUB-PKG-CONCEPT-DEVELOPMENT'}],
                         [p for p in new['packages'] if p['package_id'] not in {'HUB-PKG-AUTHORING', 'HUB-PKG-CONCEPT-DEVELOPMENT'}])
        entry = next(p for p in new['packages'] if p['package_id'] == 'HUB-PKG-AUTHORING')
        self.assertEqual(entry['version'], '0.6')
        self.assertIsNone(entry['local_catalog'])
        self.assertEqual(entry['requires'], [])
        self.assertIn('CREATIVE or BRAINSTORM only', entry['applicability'])
        self.assertIn('Version: 0.6', text)
        self.assertIn('Status: ACTIVE', text)

    def test_C2_material_ambiguity_and_strict_lexical_boundary(self):
        text = MODULE.read_text(encoding='utf-8')
        for phrase in ('ask one focused relationship question before producing the prompt',
                       'GUESSED PRIORITY != CONFIRMED PRIORITY', 'PRIMARY != AUTHORITY OVERRIDE',
                       'SECONDARY != DISPENSABLE', 'MULTIPLE CONTRIBUTORS != AUTOMATIC CLARIFICATION'):
            self.assertIn(phrase, text)
        for malformed in ('/AUTHOR AIS+CREATIVE', '/AUTHOR AIS + UNKNOWN', '/AUTHOR FTH + CREATIVE',
                          '> /AUTHOR AIS + CREATIVE', 'text\n/AUTHOR AIS + CREATIVE',
                          '/AUTHOR AIS + CREATIVE + BRAINSTORM', '/AUTHOR AIS + CREATIVE '):
            self.assertIsNone(composite_spec(malformed))
        self.assertIsNone(composite_spec('/AUTHOR AIS + CREATIVE', user_instruction=False))
        self.assertEqual(composite_spec('/AUTHOR AIS + BRAINSTORM'), ('AIS', 'BRAINSTORM'))

    def test_C3_single_target_and_corrected_M1_preservation(self):
        self.assertEqual(trigger_spec('/AUTHOR AIS'), 'AIS')
        self.assertIsNone(composite_spec('/AUTHOR AIS'))
        old = ARCHIVE / 'library_modules/HUB-CAP-AUTHORING_v0.4.1.md'
        self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(),
                         '9a6eb81b1e61c0bdbb9e7ca033ae4aa84181980778f33a0021cbf5626f6f2173')
        text = MODULE.read_text(encoding='utf-8')
        normalized = re.sub(r'## Bounded composition\n.*?(?=## Context sources, rewrite and reauthor)',
                            '', text, flags=re.S)
        normalized = normalized.replace('v0.6', 'v0.4.1').replace('Version: 0.6', 'Version: 0.4.1')
        self.assertEqual(normalized, old.read_text(encoding='utf-8'))
        self.assertEqual(list((PREDECESSOR / 'library_modules').glob('HUB-CAP-AUTHORING_v*.md')), [MODULE])
        router = load(PREDECESSOR / 'HUB_ROUTER_v1.1.yaml')
        prior = load(ARCHIVE / 'HUB_ROUTER_v1.1.yaml')
        for key in ('architecture', 'root_catalog'):
            self.assertTrue((PREDECESSOR / router['contracts'][key]['file']).is_file())
            self.assertEqual(router['contracts'][key]['version'], '1.8')
        router.pop('contracts')
        prior.pop('contracts')
        self.assertEqual(router, prior)
