"""Repository contracts and declared read plans for Shopping 1.0."""
import hashlib
import json
import re
import unittest

from test_hub_contracts import ROOT, SHOPPING_PREDECESSOR, load
from test_shopping_v1_candidate import (
    CATALOG, CORE, SEARCH, CAT_ID, CORE_ID, PACKAGE, PROFILES, SEARCH_ID, selection_fixture,
)


class ShoppingPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        modules = ROOT / 'library_modules'
        cls.core = (modules / f'{CORE_ID}_v1.0.md').read_text(encoding='utf-8')
        cls.search = (modules / f'{SEARCH_ID}_v1.0.md').read_text(encoding='utf-8')
        cls.local = load(modules / f'{CAT_ID}_v1.0.yaml')
        cls.catalog = load(ROOT / 'HUB_PACKAGE_CATALOG_v1.10.yaml')
        cls.router = load(ROOT / 'HUB_ROUTER_v1.1.yaml')
        cls.entry = next(row for row in cls.catalog['packages'] if row['package_id'] == PACKAGE)

    def test_active_identities(self):
        for body, identity, role in ((self.core, CORE_ID, 'DOMAIN_CONTROL'),
                                     (self.search, SEARCH_ID, 'DOMAIN_PROCEDURE')):
            for key, value in [('Module ID', identity), ('Package ID', PACKAGE),
                               ('Runtime role', role), ('Status', 'ACTIVE'), ('Version', '1.0')]:
                self.assertEqual(re.findall(rf'^{key}: (.+)$', body, re.M), [value])
        for row, identity, role, key in (
            (self.entry, CORE_ID, 'DOMAIN_CONTROL', 'entrypoint_module_id'),
            (self.entry['local_catalog'], CAT_ID, 'PACKAGE_CATALOG', 'module_id'),
            (self.local, CAT_ID, 'PACKAGE_CATALOG', 'module_id'),
            (self.local['entries'][0], SEARCH_ID, 'DOMAIN_PROCEDURE', 'module_id'),
        ):
            self.assertEqual((row[key], row['package_id'], row['runtime_role'], row['status'], row['version']),
                             (identity, PACKAGE, role, 'ACTIVE', '1.0'))

    def test_six_root_packages_and_interface_boundary(self):
        self.assertEqual(len(self.catalog['packages']), 6)
        self.assertEqual(set(self.entry), set(self.router['package_interface']['root_metadata']))
        self.assertEqual(set(self.entry['local_catalog']),
                         {'module_id', 'package_id', 'runtime_role', 'status', 'version', 'location'})
        self.assertEqual(self.entry['binding_mode'], 'LIBRARY_MODULE')
        for forbidden in (SEARCH_ID, *PROFILES):
            self.assertNotIn(forbidden, str(self.entry))
        self.assertIn('A product mention alone does not establish Shopping scope', self.entry['applicability'])

    def test_library_binding_remains_unresolved(self):
        for row in (self.entry, self.entry['local_catalog'], self.local['entries'][0]):
            location = row['location']
            self.assertEqual((location['class'], location['root']), ('LIBRARY', 'Central Hub Config'))
            self.assertEqual((location['resolution'], location['verification']), ('UNRESOLVED', 'NOT_PERFORMED'))
            for field in ('locator', 'library_file_id', 'library_version_id'):
                self.assertIsNone(location[field])
            self.assertIn('FULL_FILE', location['retrieval_mechanism'])

    def test_local_search_and_no_hard_dependencies(self):
        self.assertEqual([row['module_id'] for row in self.local['entries']], [SEARCH_ID])
        self.assertIn('INDEPENDENT HUB COMPOSITION', self.search)
        for row in (self.entry, self.entry['local_catalog'], self.local, self.local['entries'][0]):
            self.assertEqual(row.get('requires', []), [])
        for text in (self.core, self.search):
            self.assertNotRegex(text, r'(?m)^Requires:')

    def test_fixed_evidence_read_plan(self):
        self.assertIn('selects no Search leaf and no AIS through Shopping', self.core)
        self.assertIn('does not select this leaf', self.local['entries'][0]['applicability'])
        result = selection_fixture()
        self.assertEqual(result['read_plan'], {CORE_ID, CAT_ID})
        self.assertEqual(result['hub_pipelines'], ())

    def test_research_read_plan_and_separate_hub_selection(self):
        applicability = self.local['entries'][0]['applicability']
        self.assertIn('external discovery/current product, price or stock', applicability)
        self.assertIn('Hub independently owns external-evidence need and AIS selection', applicability)
        for pipelines in ((), ('HUB-PIPE-AIS',)):
            with self.subTest(pipelines=pipelines):
                result = selection_fixture(research_portion=True, hub_pipelines=pipelines)
                self.assertEqual(result['read_plan'], {CORE_ID, CAT_ID, SEARCH_ID})
                self.assertEqual(result['hub_pipelines'], pipelines)

    def test_candidate_behavior_preserved(self):
        for path, active, section in (
            (CORE, self.core, 'Sufficient supplied evidence for identification'),
            (SEARCH, self.search, 'INDEPENDENT HUB COMPOSITION'),
        ):
            candidate = path.read_text(encoding='utf-8')
            self.assertEqual(active.split(section, 1)[1],
                             candidate.split(section, 1)[1].replace('outside this candidate.', 'outside this package.'))
        self.assertEqual(self.local['entries'][0]['applicability'], load(CATALOG)['entries'][0]['applicability'])

    def test_shared_stack_regression(self):
        previous = load(SHOPPING_PREDECESSOR / 'HUB_PACKAGE_CATALOG_v1.9.yaml')
        self.assertEqual([row for row in self.catalog['packages'] if row['package_id'] != PACKAGE],
                         previous['packages'])
        self.assertEqual(self.catalog['identity_binding'],
                         'EXACT_INSTALLED_V1_1_CI_ROUTER_WITH_V1_10_ARCHITECTURE_CATALOG_CONTRACT')

    def test_history_integrity(self):
        receipt = json.loads((SHOPPING_PREDECESSOR / 'ARCHIVE_RECEIPT.json').read_text(encoding='utf-8'))
        self.assertEqual(set(receipt), {'HUB_ARCHITECTURE_v1.9.md', 'HUB_PACKAGE_CATALOG_v1.9.yaml',
                                       'HUB_ROUTER_v1.1.yaml'})
        for path, digest in receipt.items():
            self.assertEqual(hashlib.sha256((SHOPPING_PREDECESSOR / path).read_bytes()).hexdigest(), digest)
        previous = load(SHOPPING_PREDECESSOR / 'HUB_PACKAGE_CATALOG_v1.9.yaml')
        self.assertEqual((previous['version'], len(previous['packages'])), ('1.9', 5))

    def test_router_only_changes_exact_pins(self):
        old = (SHOPPING_PREDECESSOR / 'HUB_ROUTER_v1.1.yaml').read_bytes()
        self.assertEqual((ROOT / 'HUB_ROUTER_v1.1.yaml').read_bytes(), old.replace(b'1.9', b'1.10'))
        self.assertEqual(self.router['router_version'], '1.1')
        for key, path in [('architecture', 'HUB_ARCHITECTURE_v1.10.md'),
                          ('root_catalog', 'HUB_PACKAGE_CATALOG_v1.10.yaml')]:
            self.assertEqual(self.router['contracts'][key]['file'], path)
            self.assertEqual(self.router['contracts'][key]['version'], '1.10')
            self.assertTrue((ROOT / path).is_file())
