"""Native Hub active 0.7 contracts; static checks only, no local API host."""
import copy
import hashlib
import json
import re
import unittest

from test_hub_contracts import ROOT, SHOPPING_PREDECESSOR, load
from test_authoring_isolation import isolated_spec, CASES

OLD = ROOT / 'Source_archive/Authoring 0.7 M2 2026-11-05'
ACTIVE = ROOT / 'library_modules/HUB-CAP-AUTHORING_v0.7.md'
CANDIDATE = ROOT / 'candidates/authoring_v0_7/HUB-CAP-AUTHORING_v0.7-candidate.md'


class Authoring07PromotionTests(unittest.TestCase):
    def test_active_identity_live_candidate_and_no_suffix_preservation(self):
        text = ACTIVE.read_text(encoding='utf-8')
        self.assertIn('Status: ACTIVE\nVersion: 0.7', text)
        self.assertEqual(list((ROOT / 'library_modules').glob('HUB-CAP-AUTHORING_v*.md')), [ACTIVE])
        body = text.split('For the current turn only,', 1)[1]
        self.assertEqual(body, CANDIDATE.read_text(encoding='utf-8').split('For the current turn only,', 1)[1])
        inherited = re.sub(r'## Optional explicit source isolation\n.*?(?=## Context sources, rewrite and reauthor)', '', text, flags=re.S)
        previous = (OLD / 'library_modules/HUB-CAP-AUTHORING_v0.6.md').read_text(encoding='utf-8')
        self.assertEqual(inherited.split('For the current turn only,', 1)[1], previous.split('For the current turn only,', 1)[1])

    def test_catalog_exact_binding_and_unchanged_other_packages(self):
        catalog = load(SHOPPING_PREDECESSOR / 'HUB_PACKAGE_CATALOG_v1.9.yaml')
        old = load(OLD / 'HUB_PACKAGE_CATALOG_v1.8.yaml')
        self.assertEqual((catalog['version'], catalog['status'], catalog['active']), ('1.9', 'ACTIVE', True))
        self.assertEqual(catalog['identity_binding'], 'EXACT_INSTALLED_V1_1_CI_ROUTER_WITH_V1_9_ARCHITECTURE_CATALOG_CONTRACT')
        other = lambda data: [p for p in data['packages'] if p['package_id'] != 'HUB-PKG-AUTHORING']
        self.assertEqual(other(catalog), other(old))
        author = next(p for p in catalog['packages'] if p['package_id'] == 'HUB-PKG-AUTHORING')
        self.assertEqual((author['version'], author['status'], author['runtime_role']), ('0.7', 'ACTIVE', 'CAPABILITY'))
        self.assertEqual(author['location']['class'], 'LIBRARY')
        self.assertEqual(author['location']['resolution'], 'UNRESOLVED')
        self.assertEqual(author['requires'], [])
        self.assertIsNone(author['local_catalog'])
        self.assertIn('ISOLATED last', author['applicability'])
        self.assertIn('contributor + ISOLATED', author['applicability'])

    def test_exact_stack_pins_without_router_algorithm_change(self):
        router = load(SHOPPING_PREDECESSOR / 'HUB_ROUTER_v1.1.yaml')
        previous = load(OLD / 'HUB_ROUTER_v1.1.yaml')
        expected = copy.deepcopy(previous)
        for key, filename in [('architecture', 'HUB_ARCHITECTURE_v1.9.md'), ('root_catalog', 'HUB_PACKAGE_CATALOG_v1.9.yaml')]:
            expected['contracts'][key].update(file=filename, version='1.9')
            self.assertTrue((SHOPPING_PREDECESSOR / filename).is_file())
        expected['contracts']['binding_scope'] = expected['contracts']['binding_scope'].replace('1.8', '1.9')
        self.assertEqual(router, expected)
        architecture = (SHOPPING_PREDECESSOR / 'HUB_ARCHITECTURE_v1.9.md').read_text(encoding='utf-8')
        self.assertIn('Version: 1.9', architecture)
        self.assertIn('CAPABILITY/0.7', architecture)
        self.assertIn('exact installed Architecture/Catalog 1.9 pins', architecture)
        self.assertFalse((ROOT / 'HUB_ARCHITECTURE_v1.8.md').exists())
        self.assertFalse((ROOT / 'HUB_PACKAGE_CATALOG_v1.8.yaml').exists())

    def test_isolation_exact_forms_and_rejected_combinations_spec_only(self):
        for target in ('AIS', 'IMAGET', 'CODEX', 'WORK', 'GENERIC'):
            for preset in (None, 'P1', 'P2', 'P3'):
                suffix = '' if preset is None else ' ' + preset
                self.assertEqual(isolated_spec(f'/AUTHOR {target}{suffix} ISOLATED\nTask'), (target, preset))
            self.assertIsNone(isolated_spec('/AUTHOR ' + target))
            self.assertIsNone(isolated_spec('/AUTHOR ' + target + ' + CREATIVE ISOLATED'))
        for line in CASES['I8']['invalid']:
            with self.subTest(line=line):
                self.assertIsNone(isolated_spec(line))

    def test_predecessor_archive_receipt(self):
        receipt = json.loads((OLD / 'ARCHIVE_RECEIPT.json').read_text(encoding='utf-8'))
        self.assertEqual(set(receipt), {'library_modules/HUB-CAP-AUTHORING_v0.6.md', 'HUB_ARCHITECTURE_v1.8.md', 'HUB_PACKAGE_CATALOG_v1.8.yaml', 'HUB_ROUTER_v1.1.yaml', 'AUTHORING_PROMOTION.md'})
        for name, digest in receipt.items():
            self.assertEqual(hashlib.sha256((OLD / name).read_bytes()).hexdigest(), digest, name)


if __name__ == '__main__':
    unittest.main()
