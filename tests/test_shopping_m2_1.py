"""M2.1 REVIEWED_TEXT guards and bounded SPEC examples, never Markdown execution.

Reuse existing oracles only. Qualified facts/scopes are fixture premises;
passing here cannot reproduce or clear a failure in a model conversation.
See SHOPPING_M2_1_REGRESSIONS.md for owner decisions and untested boundaries.
"""
import copy
import hashlib
import unittest

from test_hub_contracts import ROOT, SHOPPING_PREDECESSOR, load
from test_shopping_candidate import MODULE, candidate_spec, offer_spec, offer_fixture
from test_ais_research_core import completion_oracle


class ShoppingM21Tests(unittest.TestCase):
    def test_candidate_unchanged_and_excluded_from_pre_promotion_catalog(self):
        self.assertEqual(hashlib.sha256(MODULE.read_bytes()).hexdigest(),
                         '10c176a41904aeae6238d943a3ac0b3edcef4da941e4ea876dbca8d1569a5431')
        catalog = load(SHOPPING_PREDECESSOR / 'HUB_PACKAGE_CATALOG_v1.9.yaml')
        self.assertNotIn('HUB-PKG-SHOPPING', {p['package_id'] for p in catalog['packages']})

    def test_reviewed_contract_already_has_scope_support_and_time_boundaries(self):
        text = MODULE.read_text(encoding='utf-8')
        for clause in ('protected/established Hub state',
                       'Preserve their claim-linked support/citations, applicability, uncertainty, conflicts',
                       'does not change established identity, resolve unknowns or widen the target set',
                       'An unavailable or stale offer cannot establish current availability',
                       'relevant time, availability and price conditions as applicable',
                       'Compare options using only the requested criteria and preserved constraints',
                       'Missing decisive support leaves dependent conclusions unresolved',
                       'recipe/flavor/model/variant'):
            with self.subTest(clause=clause):
                self.assertIn(clause, text)

    def test_R1_scoped_fit_facts_do_not_supply_B_fit(self):
        # Hub's correct per-model handoff is supplied, not inferred by this test.
        models = {
            'A': {'length_mm': dict(value=140, source='A dimensions'),
                  'case_fit': dict(value=False, source='A connector collision at obstruction')},
            'B': {'length_mm': dict(value=140, source='B dimensions'),
                  'connector_layout': dict(value='different', source='B geometry')},
            'C': {'length_mm': dict(value=160, source='C dimensions'),
                  'case_fit': dict(value=True, source='C installed in same case')},
        }
        before = copy.deepcopy(models)
        results = {model: candidate_spec({'case_fit': (True, 'hard')}, attributes,
                                        linked=True, identity_supported=True)
                   for model, attributes in models.items()}
        self.assertFalse(results['A']['purchase_suitable'])
        self.assertIsNone(results['B']['purchase_suitable'])
        self.assertIn('case_fit', results['B']['gaps_to_hub'])
        self.assertEqual(results['B']['hard_failures'], [])
        self.assertTrue(results['C']['purchase_suitable'])
        self.assertEqual(models, before)

    def test_R2_A_qualified_seller_update_keeps_page_as_claim_not_current_stock(self):
        # AIS/Hub qualification is a premise. No universal source ranking is added.
        page = dict(offer_fixture('SKU A'), time='t1', channel='retailer page',
                    available=True, current_supported=False,
                    qualification='t2 seller confirmation invalidates current-stock reliance')
        seller = dict(page, time='t2', channel='seller chat', available=False,
                      current_supported=True, qualification='same seller/SKU/location; direct confirmation')
        result = offer_spec([page, seller])
        self.assertEqual(result['current_available'], ())
        self.assertEqual(result['offers'], [page, seller])
        self.assertTrue(result['offers'][0]['available'])  # Retained historical page claim.
        self.assertEqual(result['discontinuation'], 'UNRESOLVED')

    def test_R2_B_conflicted_length_is_not_a_resolved_fit_advantage(self):
        readings = [('source A', 'AP-850G', 150), ('source B', 'AP-850G', 190)]
        gap = 'AP-850G length conflict 150/190 mm; fit depends on length'
        returned = completion_oracle({'resolved AP-850G length'}, set(), [gap], limit_reached=True)
        self.assertFalse(returned['sufficient'])
        self.assertIn(gap, returned['unresolved'])
        # No choosing 150 mm during qualification. An unresolved length cannot
        # be passed as a supported attribute to the domain oracle.
        domain = candidate_spec({'fit_length_mm': (150, 'hard')}, {}, linked=True)
        self.assertIsNone(domain['purchase_suitable'])
        self.assertNotIn('fit_length_mm', domain['matches'])
        self.assertIn('fit_length_mm', domain['gaps_to_hub'])
        self.assertEqual({length for _, _, length in readings}, {150, 190})

    def test_R2_C_missing_mandatory_protection_is_not_passed_by_low_price(self):
        criteria = {'protection': (True, 'hard')}
        a = candidate_spec(criteria, {'price': dict(value=100, source='offer A')}, linked=True)
        b = candidate_spec(criteria, {'price': dict(value=120, source='offer B'),
                                     'protection': dict(value=True, source='relevant supplied lab evidence')},
                           linked=True)
        self.assertIsNone(a['purchase_suitable'])
        self.assertIn('protection', a['gaps_to_hub'])
        self.assertTrue(b['purchase_suitable'])
        # There is no overall ranker in the existing oracle. Do not manufacture
        # one and call its output the candidate's actual recommendation.

    def test_R2_D_surrounding_dates_do_not_fill_requested_price_window(self):
        requested = 'price in requested window 2025-07-03'
        offers = [dict(offer_fixture('SKU white', 22.9), time='2025-04-01', current_supported=False),
                  dict(offer_fixture('SKU white', 24.0), time='2025-10-01', current_supported=False)]
        coverage = completion_oracle({requested}, {'2025-04-01 observation', '2025-10-01 observation'},
                                     [requested], limit_reached=True)
        self.assertFalse(coverage['sufficient'])
        self.assertIn(requested, coverage['unresolved'])
        result = offer_spec(offers)
        self.assertIsNone(result['mean'])
        self.assertEqual(result['offers'], offers)
        # No interpolation/trend inference or claimed model answer is generated.

    def test_R3_A_delegated_mismatch_stays_conflicted_without_selecting_referent(self):
        result = candidate_spec({'sku': ('Corsair RM850e 2025', 'hard')},
                                {'sku': dict(value='ASUS TUF Gaming 850W', source='resolved supplied URL object')},
                                linked=False)
        self.assertEqual(result['conflicts']['sku'], ('Corsair RM850e 2025', 'ASUS TUF Gaming 850W'))
        self.assertEqual(result['identity'], 'CANDIDATE')
        # Neither field is chosen as true. Whole-turn referent interpretation is
        # Hub-owned; this only covers an explicitly delegated attribute mismatch.
        hub = (ROOT / 'HUB_CI_v1.1.md').read_text(encoding='utf-8')
        self.assertIn('If plausible readings materially change what should be done', hub)
        self.assertIn('ask one focused question or branch', hub)

    def test_R3_B_exact_revision_not_established_by_V1_or_unknown_images(self):
        criteria = {'revision': ('V2', 'hard')}
        old = candidate_spec(criteria, {'revision': dict(value='V1', source='available image record')},
                             linked=True)
        unknown = candidate_spec(criteria, {}, linked=False)
        self.assertEqual(old['conflicts']['revision'], ('V2', 'V1'))
        self.assertFalse(old['purchase_suitable'])
        self.assertIsNone(unknown['purchase_suitable'])
        self.assertIn('revision', unknown['gaps_to_hub'])
        # No image retrieval/rendering is executed; primary-evidence selection
        # by a model is still untested.

    def test_long_context_has_current_scope_contract_but_no_fake_conversation_engine(self):
        router = load(ROOT / 'HUB_ROUTER_v1.1.yaml')
        scope = router['stages']['ROOT_PACKAGE_SELECTION']
        self.assertIn('Recompute selection from the current task portion', scope)
        self.assertIn('Neither prior package selection nor prior package non-selection', scope)
        self.assertFalse(router['persistence']['persistent_modes'])
        self.assertIn('Every turn and material scope change', router['persistence']['reassess'])
        # This is a contract assertion, not simulated evidence-need recognition.
        audit = (ROOT / 'tests/SHOPPING_M2_1_REGRESSIONS.md').read_text(encoding='utf-8')
        self.assertIn('| LC | NOT TESTABLE STATICALLY', audit)
        self.assertIn('LIVE SHOPPING / AIS COMPOSITION / LONG-CHAT CAUSALITY: NOT RUN', audit)


if __name__ == '__main__':
    unittest.main()
