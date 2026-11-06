"""V1-01..V1-14: STATIC guards and bounded declared SPEC fixtures only.

No Markdown/model execution, natural-language routing, Library retrieval or tools.
Selection, evidence qualification and source roles are supplied premises. The small
selection fixture is a read plan, not an executable Hub/Shopping resolver. Existing
M2/AIS oracles remain test-only and are never imported by runtime control artifacts.
LIVE SHOPPING / HUB ROUTING / AIS COMPOSITION: NOT RUN.
"""
import copy
import re
import unittest

from test_hub_contracts import ROOT, SHOPPING_PREDECESSOR, load
from test_shopping_candidate import candidate_spec
from test_ais_research_core import completion_oracle, execution_oracle


BASE = ROOT / 'candidates/shopping_v1'
CORE_ID = 'HUB-DOM-SHOPPING'
CAT_ID = 'HUB-CATALOG-SHOPPING'
SEARCH_ID = 'HUB-PROC-SHOPPING-SEARCH'
PACKAGE = 'HUB-PKG-SHOPPING'
VERSION = '1.0-candidate'
CORE = BASE / f'{CORE_ID}_v{VERSION}.md'
CATALOG = BASE / f'{CAT_ID}_v{VERSION}.yaml'
SEARCH = BASE / f'{SEARCH_ID}_v{VERSION}.md'
PROFILES = ('ELECTRONICS', 'HOME', 'FOOD', 'FASHION', 'PERSONAL', 'HOBBY')


def root_entry_fixture():
    """Uninstalled candidate interface view only; not an active Catalog edit."""
    location = {'class': 'LIBRARY', 'root': 'Central Hub Config',
                'locator': None, 'library_file_id': None, 'library_version_id': None,
                'resolution': 'UNRESOLVED', 'verification': 'NOT_PERFORMED'}
    return dict(package_id=PACKAGE, entrypoint_module_id=CORE_ID, runtime_role='DOMAIN_CONTROL',
                status='CANDIDATE', version=VERSION,
                applicability='Material Shopping-domain interpretation of the Hub-delegated portion.',
                binding_mode='LIBRARY_MODULE', location=location, requires=[],
                local_catalog=dict(module_id=CAT_ID, package_id=PACKAGE, runtime_role='PACKAGE_CATALOG',
                                   status='CANDIDATE', version=VERSION, location=copy.deepcopy(location)))


def selection_fixture(*, research_portion=False, hub_pipelines=(), missing=()):
    """Already-classified scope/availability; read plan only, no source resolution."""
    base = {CORE_ID, CAT_ID}
    missing = set(missing)
    if base & missing:
        return dict(read_plan=base - missing, blocked=base, hub_pipelines=tuple(hub_pipelines))
    selected = base | ({SEARCH_ID} if research_portion else set())
    return dict(read_plan=selected - missing, blocked=selected & missing,
                hub_pipelines=tuple(hub_pipelines))


class ShoppingV1CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = CORE.read_text(encoding='utf-8')
        cls.search = SEARCH.read_text(encoding='utf-8')
        cls.catalog = load(CATALOG)

    def test_V1_01_candidate_identities_and_no_active_admission(self):
        self.assertEqual({p.name for p in BASE.iterdir()}, {CORE.name, CATALOG.name, SEARCH.name})
        for path, module, role in [(CORE, CORE_ID, 'DOMAIN_CONTROL'),
                                   (SEARCH, SEARCH_ID, 'DOMAIN_PROCEDURE')]:
            text = path.read_text(encoding='utf-8')
            for key, value in [('Module ID', module), ('Package ID', PACKAGE), ('Runtime role', role),
                               ('Status', 'CANDIDATE'), ('Version', VERSION)]:
                self.assertEqual(re.findall(rf'^{key}: (.+)$', text, re.M), [value])
            self.assertNotRegex(text, r'(?m)^(Requires|Refines|Complements):')
        for key, value in dict(module_id=CAT_ID, package_id=PACKAGE, runtime_role='PACKAGE_CATALOG',
                               status='CANDIDATE', version=VERSION).items():
            self.assertEqual(self.catalog[key], value)
        for entry in (root_entry_fixture(), self.catalog, self.catalog['entries'][0]):
            self.assertNotEqual(entry['status'], 'ACTIVE')
        previous = load(SHOPPING_PREDECESSOR / 'HUB_PACKAGE_CATALOG_v1.9.yaml')
        self.assertEqual(len(previous['packages']), 5)
        self.assertNotIn(PACKAGE, {p['package_id'] for p in previous['packages']})

    def test_V1_02_root_view_is_only_package_interface(self):
        entry = root_entry_fixture()
        expected = load(ROOT / 'HUB_ROUTER_v1.1.yaml')['package_interface']['root_metadata']
        self.assertEqual(set(entry), set(expected))
        for level in (entry, entry['local_catalog']):
            self.assertEqual(level['location']['root'], 'Central Hub Config')
            for key in ('locator', 'library_file_id', 'library_version_id'):
                self.assertIsNone(level['location'][key])
        self.assertEqual(entry['local_catalog']['module_id'], CAT_ID)
        for forbidden in (SEARCH_ID, *PROFILES, 'retailer_data', 'entries', 'repository_path'):
            self.assertNotIn(forbidden, str(entry))

    def test_V1_03_local_catalog_has_one_applicable_search_procedure(self):
        self.assertEqual(len(self.catalog['entries']), 1)
        leaf = self.catalog['entries'][0]
        for key, value in dict(module_id=SEARCH_ID, package_id=PACKAGE,
                               runtime_role='DOMAIN_PROCEDURE', status='CANDIDATE', version=VERSION).items():
            self.assertEqual(leaf[key], value)
        self.assertTrue(leaf['scope'])
        self.assertIn('research-oriented Shopping portion', leaf['applicability'])
        self.assertIn('Fixed supplied evidence sufficient', leaf['applicability'])
        self.assertIn('does not select this leaf', leaf['applicability'])
        self.assertEqual(leaf['location']['class'], 'LIBRARY')
        self.assertEqual(leaf['location']['root'], 'Central Hub Config')
        for key in ('locator', 'library_file_id', 'library_version_id'):
            self.assertIsNone(leaf['location'][key])
        self.assertEqual(leaf['location']['verification'], 'NOT_PERFORMED')
        self.assertNotIn('repository_path', leaf['location'])
        for relation in ('requires', 'refines', 'complements'):
            self.assertFalse(leaf.get(relation))

    def test_V1_04_no_research_closure_for_sufficient_supplied_evidence(self):
        for operation in ('fixed Offer comparison', 'identity', 'constraint reevaluation', 'Category interpretation'):
            with self.subTest(operation=operation):
                result = selection_fixture()
                self.assertEqual(result['read_plan'], {CORE_ID, CAT_ID})
                self.assertEqual(result['hub_pipelines'], ())
                self.assertFalse(result['blocked'])
        self.assertIn('baseline closure is core + local Catalog', self.core)
        self.assertIn('selects no Search leaf and no AIS through Shopping', self.core)
        unrelated = selection_fixture(hub_pipelines=('HUB-PIPE-AIS',))
        self.assertEqual(unrelated['read_plan'], {CORE_ID, CAT_ID})
        self.assertEqual(unrelated['hub_pipelines'], ('HUB-PIPE-AIS',))

    def test_V1_05_research_closure_and_independently_selected_AIS(self):
        for operation in ('external discovery', 'current price', 'current stock'):
            with self.subTest(operation=operation):
                result = selection_fixture(research_portion=True, hub_pipelines=('HUB-PIPE-AIS',))
                self.assertEqual(result['read_plan'], {CORE_ID, CAT_ID, SEARCH_ID})
                self.assertEqual(result['hub_pipelines'], ('HUB-PIPE-AIS',))
        unselected = selection_fixture(research_portion=True)
        self.assertEqual(unselected['hub_pipelines'], ())
        self.assertIn('INDEPENDENT HUB COMPOSITION', self.search)
        self.assertIn('no hard Requires AIS edge', self.search)
        self.assertIn('preserve the evidence need/incomplete research state', self.search)

    def test_V1_06_priority_order_changes_neither_roles_nor_hard_eligibility(self):
        conditions = {'weight_g': (250, 'soft'), 'protection': (True, 'hard')}
        evidence = {'weight_g': dict(value=180, source='identity record')}
        before = copy.deepcopy(conditions)
        for order in [('weight_g', 'protection'), ('protection', 'weight_g')]:
            ordered = {field: conditions[field] for field in order}
            result = candidate_spec(ordered, evidence, linked=True)
            self.assertIsNone(result['purchase_suitable'])
            self.assertEqual(result['hard_failures'], [])
            self.assertEqual(result['conflicts']['weight_g'], (250, 180))
        self.assertEqual(conditions, before)
        self.assertIn('Changing priority_order does not change HARD/SOFT roles', self.core)
        self.assertIn('preserve user-declared ties rather than inventing an order', self.core)
        self.assertIn('lower-priority HARD criterion still blocks', self.core)

    def test_V1_07_category_fields_are_suggestions_not_required_conditions(self):
        rows = re.findall(r'^\| (' + '|'.join(PROFILES) + r') \| (.+) \| (.+) \|$', self.core, re.M)
        self.assertEqual([row[0] for row in rows], list(PROFILES))
        self.assertIn('expiry', next(row for row in rows if row[0] == 'FOOD')[2])
        # Already-classified material requirement; no expiry condition was requested.
        conditions = {'packaging': ('jar', 'hard')}
        result = candidate_spec(conditions, {'packaging': dict(value='jar', source='supplied label')}, linked=True)
        self.assertTrue(result['purchase_suitable'])
        self.assertNotIn('expiry', result['gaps_to_hub'])
        for clause in ('PROFILE FIELD != USER REQUIREMENT', 'does not require researching every field',
                       'fields from multiple profiles', 'general Shopping path when sufficient'):
            self.assertIn(clause, self.core)

    def test_V1_08_same_seller_different_channels_remain_distinct_offers(self):
        offers = [dict(sku='variant A', seller='seller X', channel='own website', price=120, stock='in stock'),
                  dict(sku='variant A', seller='seller X', channel='marketplace store', price=100, stock='unknown')]
        observation_keys = {(o['sku'], o['seller'], o['channel']) for o in offers}
        self.assertEqual(len(observation_keys), 2)
        self.assertEqual([o['price'] for o in offers], [120, 100])
        self.assertIn('SAME SELLER != SAME OFFER', self.core)
        self.assertIn('do not deduplicate by seller or product name alone', self.core)

    def test_V1_09_conditional_price_does_not_become_unconditional_total(self):
        offers = [dict(basis='list', price=120, member_required=False, shipping=None),
                  dict(basis='sale', price=100, member_required=False, shipping=None),
                  dict(basis='sale+voucher', price=80, member_required=True,
                       eligibility=None, payment='specific card', shipping=None)]
        unconditional = [o['price'] for o in offers if not o['member_required']]
        self.assertEqual(min(unconditional), 100)
        self.assertEqual(min(o['price'] for o in offers), 80)
        self.assertTrue(all(o['shipping'] is None for o in offers))
        self.assertEqual([o['basis'] for o in offers], ['list', 'sale', 'sale+voucher'])
        self.assertIsNone(offers[2]['eligibility'])
        self.assertNotIn('effective_total', offers[2])
        for clause in ('LOWEST CONDITIONAL PRICE != LOWEST UNCONDITIONAL PRICE',
                       'Never invent shipping = 0', 'payment, shipping, bundle and warranty conditions',
                       'prevents an unconditional effective-total claim'):
            self.assertIn(clause, self.core)

    def test_V1_10_hard_unknown_does_not_qualify_cheapest_as_overall_winner(self):
        requirements = {'protection': (True, 'hard')}
        candidates = {'cheap': candidate_spec(requirements, {}, linked=True),
                      'verified': candidate_spec(requirements,
                                                 {'protection': dict(value=True, source='supplied lab')}, linked=True)}
        eligible = [name for name, value in candidates.items() if value['purchase_suitable'] is True]
        self.assertEqual(eligible, ['verified'])
        self.assertIsNone(candidates['cheap']['purchase_suitable'])
        self.assertIn('Do not force one winner', self.core)
        self.assertIn('does not prohibit every useful response', self.core)
        self.assertIn('winner dependent on an unresolved mandatory field', self.core)

    def test_V1_11_AIS_action_status_and_basis_are_preserved(self):
        for traces, expected in [([('DIRECT_EXECUTION_TRACE', 'search', 1)], 'EXECUTED'),
                                 ([('PRE_SUBMISSION_BLOCK', 'search', 1)], 'NOT_EXECUTED'),
                                 ([], 'UNKNOWN'),
                                 ([('DIRECT_EXECUTION_TRACE', 'search', 1),
                                   ('DIRECT_NON_EXECUTION_TRACE', 'search', 1)], 'CONFLICTED')]:
            # Existing AIS oracle takes (action, attempt, trace-kind).
            converted = [(action, attempt, kind) for kind, action, attempt in traces]
            status = execution_oracle(converted, retrospective='I searched')
            self.assertEqual(status, expected)
            packet = dict(actual_execution_status=status, execution_evidence_basis=converted,
                          source_reads=[], claim_support=[])
            carried = copy.deepcopy(packet)
            self.assertEqual(carried, packet)
            self.assertFalse(carried['source_reads'])
        for guard in ('PLANNED SEARCH != EXECUTED SEARCH', 'EXECUTED SEARCH != SOURCE READ',
                      'SOURCE READ != CLAIM SUPPORT', 'SOURCE READ != VALID OFFER',
                      'VALID OFFER != SHOPPING-SCOPE COMPLETION'):
            self.assertIn(guard, self.search)
        self.assertIn('model self-report as proof', self.search)

    def test_V1_12_partial_channels_do_not_establish_market_completion(self):
        branches = {'major': 'covered', 'specialists': 'covered',
                    'small independents': 'partial', 'marketplaces': 'not executed'}
        supported = {name for name, status in branches.items() if status == 'covered'}
        result = completion_oracle(set(branches), supported, limit_reached=True)
        self.assertTrue(result['return_to_hub'])
        self.assertFalse(result['sufficient'])
        self.assertEqual(result['unresolved'], {'small independents', 'marketplaces'})
        self.assertIn('do not report the whole market searched', self.search)
        self.assertIn('not fixed tiers, named store rankings, a registry or a quota', self.search)

    def test_V1_13_predecessor_semantics_preserved_without_copying_fixture_code(self):
        for guard in ('SOFT CLUE != HARD FILTER', 'CANDIDATE != CONFIRMED IDENTITY',
                      'SUPPORTED ATTRIBUTES != SUPPORTED SAME-SKU COMBINATION',
                      'DISCOVERED SET != CONFIRMED-COMPLETE SET',
                      'RETAILER CATALOG != MANUFACTURER CATALOG',
                      'RETAILER AVERAGE != MARKET AVERAGE', 'OFFER PRICE != UNIVERSAL PRODUCT PRICE',
                      'OUT OF STOCK != DISCONTINUED', 'NOT FOUND != NONEXISTENT',
                      'PURCHASE SUITABILITY != HISTORICAL PRODUCT IDENTITY'):
            self.assertIn(guard, self.core)
        self.assertIn("A retailer's internal SKU code is optional", self.core)
        self.assertIn('model-specific fit finding must not become a dimension-wide constraint', self.core)
        self.assertNotIn('Paté Royal', self.core)  # Historical example is not a universal rule.
        for text in (self.core, self.search):
            self.assertNotIn('def candidate_spec', text)
            self.assertNotIn('from test_', text)

    def test_V1_14_missing_search_blocks_only_dependent_work(self):
        needed = selection_fixture(research_portion=True, missing={SEARCH_ID})
        self.assertEqual(needed['read_plan'], {CORE_ID, CAT_ID})
        self.assertEqual(needed['blocked'], {SEARCH_ID})
        independent = selection_fixture(missing={SEARCH_ID})
        self.assertEqual(independent['read_plan'], {CORE_ID, CAT_ID})
        self.assertFalse(independent['blocked'])
        for missing in (CORE_ID, CAT_ID):
            broken = selection_fixture(research_portion=True, missing={missing})
            self.assertEqual(broken['blocked'], {CORE_ID, CAT_ID})
            self.assertNotIn(SEARCH_ID, broken['read_plan'])
        self.assertIn('Missing Search blocks Search-dependent work only', self.core)
        self.assertIn('Do not substitute v0.1', self.core)


if __name__ == '__main__':
    unittest.main()
