"""STATIC guards and SPEC examples only; never execute the Markdown or an LLM.

Facts, source links, identity support and coverage are declared fixture premises.
These tiny oracles check their consequences, not actual evidence sufficiency.
No runtime Shopping implementation, natural-language interpreter or tool calls.
"""
import copy
import hashlib
import re
import unittest
from decimal import Decimal

from test_hub_contracts import ROOT, SHOPPING_PREDECESSOR, load, historical_source


CANDIDATE = ROOT / 'candidates/shopping_v0'
MODULE = CANDIDATE / 'HUB-DOM-SHOPPING_v0.1-candidate.md'
CASES = CANDIDATE / 'SHOPPING_TEST_CASES.md'
# Captured from clean main 28adb1a before M2; intentional candidate-only scope.
BASELINE = {
    'HUB_CI_v1.1.md': '7bb946874663627060d28e47674decb07ba99f51acbffb6550db98d65746157b',
    # Refreshed only for the authorized Library identity correction; Shopping remains inactive.
    'HUB_ROUTER_v1.1.yaml': 'b63baa9a9461b90f12c61b35dbe572270ac16826e38c66f8a95128ad32e705de',
    'HUB_ARCHITECTURE_v1.0.md': 'da62208fd10ed46d2a453fb72c55a0475185583d107edc2196b5b503eae738b5',
    # Refreshed for observed BRAINSTORM UI identity evidence; Shopping remains outside the active Catalog.
    'HUB_PACKAGE_CATALOG_v1.0.yaml': '4d841f8f0ca37220772cec1253d633004a38dfae330656f917554e7058a6d443',
    'tool_pipelines/AIS/AIS_PIPELINE_v1.1.md': '68763c5bc3a19dbfae17535daebcc5e95e6279368153583470285334d6e2ffd6',
    'tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml': 'c977b5adb74436e066192d240304e5e898b320d086cf3352ce5a59c542d03dbf',
}


def candidate_spec(clues, attributes, *, linked, identity_supported=False):
    """Already-classified clues and support; no identity/source-policy inference."""
    matches, conflicts, unknowns, hard_failures = {}, {}, [], []
    for name, (value, role) in clues.items():
        if name not in attributes:
            unknowns.append(name)
        elif attributes[name]['value'] == value:
            matches[name] = value
        else:
            conflicts[name] = (value, attributes[name]['value'])
            if role == 'hard':
                hard_failures.append(name)
    gaps = unknowns + ([] if linked else ['same-SKU link'])
    established = linked and identity_supported and not unknowns
    if not established:
        gaps.append('identity of remembered item')
    return dict(matches=matches, conflicts=conflicts, unknowns=unknowns,
                support=copy.deepcopy(attributes), hard_failures=hard_failures,
                purchase_suitable=False if hard_failures else
                None if any(clues[name][1] == 'hard' for name in unknowns) else True,
                identity='ESTABLISHED' if established else 'CANDIDATE',
                gaps_to_hub=gaps)


def catalog_spec(items, target, *, supported_complete_target=None):
    """Completeness support is supplied upstream, not evaluated by Shopping."""
    complete = target == supported_complete_target
    return dict(items=tuple(items), target=target, complete=complete,
                gaps_to_hub=[] if complete else [f'coverage of {target}'])


def offer_spec(offers, *, listing_found=True):
    """Defined-set arithmetic only; no market inference or source freshness engine."""
    # Every grouping component is a supplied condition; absent material context
    # prevents aggregation. Explicit normalization is outside these small fixtures.
    dimensions = ('retailer', 'currency', 'unit', 'basis', 'conditions', 'location', 'time')
    comparable = bool(offers) and all(
        all(o.get(k) is not None for k in (*dimensions, 'sku', 'price')) for o in offers)
    if comparable:
        comparable = len({tuple(o[k] for k in dimensions) for o in offers}) == 1
    return dict(offers=copy.deepcopy(offers),
                mean=sum((Decimal(str(o['price'])) for o in offers), Decimal(0)) / len(offers)
                if comparable else None,
                average_scope='DEFINED_RETAILER_SKU_SET' if comparable else None,
                current_available=tuple(o['sku'] for o in offers
                                        if o.get('current_supported') and o.get('available')),
                existence='LISTING_FOUND' if listing_found else 'UNRESOLVED',
                discontinuation='UNRESOLVED')


def pate_fixture():
    clues = {name: (value, 'soft') for name, value in {
        'style': 'country-style pâté', 'jar': 'glass', 'lid': 'metal',
        'weight_g': 250, 'distributor': 'Ân Nam', 'retailer': 'Annam Gourmet',
    }.items()}
    attributes = {name: dict(value=value, source='linked fixture record')
                  for name, (value, _) in clues.items()}
    attributes['weight_g']['value'] = 180
    attributes['product_line'] = dict(value='Paté Royal', source='linked fixture record')
    return clues, attributes


def offer_fixture(sku='Paté Royal country 180 g', price=100000):
    return dict(sku=sku, retailer='X', price=price, currency='VND', unit='one 180 g jar',
                basis='normal', conditions='none', location='fixture location',
                time='fixture current observation', available=True, current_supported=True)


class ShoppingCandidateStaticTests(unittest.TestCase):
    def test_single_inactive_domain_and_no_internal_router_or_catalog(self):
        self.assertEqual({p.name for p in CANDIDATE.iterdir()}, {MODULE.name, CASES.name})
        text = MODULE.read_text(encoding='utf-8')
        for key, value in [('Module ID', 'HUB-DOM-SHOPPING'), ('Package ID', 'HUB-PKG-SHOPPING'),
                           ('Runtime role', 'DOMAIN_CONTROL'), ('Status', 'CANDIDATE'),
                           ('Version', '0.1-candidate')]:
            self.assertEqual(re.findall(rf'^{key}: (.+)$', text, re.M), [value])
        for key in ('Scope', 'Responsibility boundary'):
            self.assertEqual(len(re.findall(rf'^{key}: .+$', text, re.M)), 1)
        self.assertNotRegex(text, r'(?m)^(Refines|Complements|Requires):')
        self.assertIn('explicitly authorized isolated candidate test', text)
        self.assertIn('no runtime Library binding', text)

    def test_preserved_baseline_and_shopping_not_admitted(self):
        for path, expected in BASELINE.items():
            with self.subTest(path=path):
                data = historical_source(path).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected)
                self.assertNotIn(b'HUB-PKG-SHOPPING', data)
        catalog = load(SHOPPING_PREDECESSOR / 'HUB_PACKAGE_CATALOG_v1.9.yaml')
        self.assertEqual(len(catalog['packages']), 5)
        self.assertNotIn('HUB-PKG-SHOPPING', {p['package_id'] for p in catalog['packages']})

    def test_negative_escalation_guards_and_existing_owners(self):
        text = MODULE.read_text(encoding='utf-8')
        for guard in ('SOFT CLUE != HARD FILTER', 'CANDIDATE != CONFIRMED IDENTITY',
                      'SUPPORTED ATTRIBUTES != SUPPORTED SAME-SKU COMBINATION',
                      'DISCOVERED SET != CONFIRMED-COMPLETE SET',
                      'RETAILER CATALOG != MANUFACTURER CATALOG',
                      'RETAILER AVERAGE != MARKET AVERAGE',
                      'OFFER PRICE != UNIVERSAL PRODUCT PRICE',
                      'OUT OF STOCK != DISCONTINUED', 'NOT FOUND != NONEXISTENT',
                      'SHOPPING DOMAIN INTERPRETATION != EVIDENCE AUTHORITY',
                      'SHOPPING EVIDENCE GAP != AIS ACTIVATION',
                      'SHOPPING APPLICABILITY != ROUTING AUTHORITY'):
            with self.subTest(guard=guard):
                self.assertIn(guard, text)
        self.assertIn('Hub Router retains package selection/composition', text)
        self.assertIn('AIS retains research procedure, source policy, support and coverage checks', text)
        self.assertIn('AIS is not a hard dependency', text)

    def test_case_inventory_and_honest_evidence_labels(self):
        text = CASES.read_text(encoding='utf-8')
        ids = re.findall(r'^\| ([ABCDN]\d+) \|', text, re.M)
        self.assertEqual(ids, [f'{prefix}{i:02}' for prefix, n in
                              [('A', 4), ('B', 3), ('C', 5), ('D', 4), ('N', 10)]
                         for i in range(1, n + 1)])
        for label in ('REVIEWED_TEXT', 'STATIC VALIDATION', 'SPEC SIMULATION',
                      'LIVE CHATGPT / HUB ROUTING / LIBRARY / AIS-SHOPPING COMPOSITION: NOT RUN',
                      'REPRODUCED FAILURE is not claimed'):
            self.assertIn(label, text)


class ShoppingCandidateSpecTests(unittest.TestCase):
    def test_A01_A02_soft_memory_vs_hard_purchase_constraint(self):
        clues, attributes = pate_fixture()
        soft = candidate_spec(clues, attributes, linked=True)
        self.assertEqual(soft['conflicts'], {'weight_g': (250, 180)})
        self.assertEqual(len(soft['matches']), 5)
        self.assertTrue(soft['purchase_suitable'])
        self.assertEqual(soft['identity'], 'CANDIDATE')
        self.assertEqual(soft['support'], attributes)
        clues['weight_g'] = (250, 'hard')
        hard = candidate_spec(clues, attributes, linked=True)
        self.assertFalse(hard['purchase_suitable'])
        self.assertEqual(hard['hard_failures'], ['weight_g'])
        self.assertEqual(hard['conflicts'], soft['conflicts'])
        self.assertEqual(hard['identity'], 'CANDIDATE')

    def test_A03_A04_matching_fields_need_identity_support(self):
        clues, attributes = pate_fixture()
        clues['weight_g'] = (180, 'soft')
        self.assertEqual(candidate_spec(clues, attributes, linked=True)['identity'], 'CANDIDATE')
        established = candidate_spec(clues, attributes, linked=True, identity_supported=True)
        self.assertEqual(established['identity'], 'ESTABLISHED')
        self.assertEqual(established['gaps_to_hub'], [])

    def test_unknown_attribute_remains_a_named_gap(self):
        clues, attributes = pate_fixture()
        del attributes['lid']
        result = candidate_spec(clues, attributes, linked=True)
        self.assertEqual(result['unknowns'], ['lid'])
        self.assertIn('lid', result['gaps_to_hub'])
        clues['lid'] = ('metal', 'hard')
        self.assertIsNone(candidate_spec(clues, attributes, linked=True)['purchase_suitable'])

    def test_B01_B02_B03_coverage_must_match_target(self):
        items = tuple(f'Paté Royal fixture variant {i}' for i in range(10))
        retailer = 'all Paté Royal listings at X under fixture conditions'
        manufacturer = 'manufacturer global catalog'
        complete = catalog_spec(items, retailer, supported_complete_target=retailer)
        unsupported = catalog_spec(items, manufacturer, supported_complete_target=retailer)
        discovered = catalog_spec(items, retailer)
        self.assertTrue(complete['complete'])
        self.assertEqual(complete['target'], retailer)
        for result in (unsupported, discovered):
            self.assertFalse(result['complete'])
            self.assertEqual(result['items'], items)
            self.assertEqual(result['gaps_to_hub'], [f"coverage of {result['target']}"])

    def test_C01_retailer_mean_retains_offer_context(self):
        offers = [offer_fixture(), offer_fixture('Paté Royal pepper 180 g', 120000)]
        result = offer_spec(offers)
        self.assertEqual(result['mean'], Decimal(110000))
        self.assertEqual(result['average_scope'], 'DEFINED_RETAILER_SKU_SET')
        self.assertEqual(result['offers'], offers)
        self.assertNotEqual(result['average_scope'], 'MARKET')

    def test_C02_sale_and_normal_prices_are_separate(self):
        normal = offer_fixture()
        sale = dict(normal, price=80000, basis='sale', conditions='members only')
        result = offer_spec([normal, sale])
        self.assertIsNone(result['mean'])
        self.assertEqual(result['offers'][1]['conditions'], 'members only')
        self.assertEqual(offer_spec([sale])['mean'], Decimal(80000))

    def test_C03_C04_stale_unavailable_and_not_found_do_not_escalate(self):
        offers = [dict(offer_fixture(), available=False),
                  dict(offer_fixture('Paté Royal pepper 180 g'), current_supported=False)]
        result = offer_spec(offers)
        self.assertEqual(result['current_available'], ())
        self.assertEqual(result['discontinuation'], 'UNRESOLVED')
        self.assertEqual(result['offers'], offers)
        absent = offer_spec([], listing_found=False)
        self.assertEqual(absent['existence'], 'UNRESOLVED')
        self.assertIsNone(absent['mean'])

    def test_C05_incompatible_or_missing_offer_context_prevents_pooling(self):
        first = offer_fixture()
        for field, value in [('currency', 'USD'), ('unit', 'two jars'), ('location', 'elsewhere'),
                             ('time', 'old observation'), ('retailer', 'Y'), ('price', None)]:
            with self.subTest(field=field):
                self.assertIsNone(offer_spec([first, dict(first, **{field: value})])['mean'])

    def test_D01_D02_D03_supplied_evidence_or_gap_to_hub_never_runs_AIS(self):
        clues = {'brand': ('Paté Royal', 'soft'), 'weight_g': (180, 'soft')}
        evidence = {'brand': dict(value='Paté Royal', source='A'),
                    'weight_g': dict(value=180, source='B')}
        # No AIS input is required. Its support/link judgments, when supplied,
        # arrive as premises through Hub; this oracle never resolves sources.
        ready = candidate_spec(clues, evidence, linked=True, identity_supported=True)
        self.assertEqual(ready['gaps_to_hub'], [])
        gap = candidate_spec(clues, evidence, linked=False, identity_supported=True)
        self.assertEqual(gap['identity'], 'CANDIDATE')
        self.assertIn('same-SKU link', gap['gaps_to_hub'])
        self.assertEqual(gap['support']['brand']['source'], 'A')
        self.assertEqual(gap['support']['weight_g']['source'], 'B')
        self.assertNotIn('selected_pipeline', gap)
        self.assertNotIn('tool_calls', gap)

    def test_D04_operation_sequence_preserves_supplied_product_state(self):
        clues, attributes = pate_fixture()
        clues['weight_g'] = (180, 'soft')
        state = dict(sku='Paté Royal country 180 g', clues=clues, attributes=attributes,
                     linked=True, identity_supported=True)
        before = copy.deepcopy(state)
        identity = candidate_spec(state['clues'], state['attributes'], linked=state['linked'],
                                  identity_supported=state['identity_supported'])
        other_sku = 'Paté Royal pepper 180 g'
        variants = catalog_spec([state['sku'], other_sku], 'retailer X')
        prices = offer_spec([offer_fixture(state['sku']), offer_fixture(other_sku, 120000)])
        # Comparison is scoped arithmetic on supplied offers, no state engine.
        comparison = min(prices['offers'], key=lambda o: o['price'])['sku']
        self.assertEqual(identity['identity'], 'ESTABLISHED')
        self.assertEqual(variants['items'], (state['sku'], other_sku))
        self.assertEqual(prices['offers'][0]['sku'], state['sku'])
        self.assertEqual(comparison, state['sku'])
        self.assertEqual(state, before)


if __name__ == '__main__':
    unittest.main()
