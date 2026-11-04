"""Focused context/prefix regressions through existing mocked M1 execution."""
import json
import unittest

import app
import t8
import t9
import test_m1
from test_t7 import leaf


def handoff(payload):
    return json.JSONDecoder().raw_decode(
        payload['instructions'].split('[T8 VERIFIED HANDOFF]\n', 1)[1])[0]


class M3Tests(unittest.TestCase):
    def setUp(self):
        self.harness = test_m1.M1Tests()
        self.harness.setUp()
        self.addCleanup(self.harness.doCleanups)

    def test_no_ais_keeps_root_selection_and_final_authoring_contribution(self):
        h = self.harness
        h.select(t8.AUTHORING, t8.TECHNICAL, t8.CONCEPT)
        h.admission.update(target='GENERIC', contributor='BRAINSTORM')
        h.owner.update(module_id='HUB-CAP-BRAINSTORM', runtime_role='CAPABILITY')
        h.local['selected_leaves'] = [leaf('HUB-CAP-BRAINSTORM')]
        answer, trace = h.run_runtime()
        for payload in h.payloads[1:]:
            data = handoff(payload)
            self.assertIsNone(data['ais_evidence'])
            self.assertEqual(data['selected_packages'], [
                {k: s[k] for k in app.ROUTE_PACKAGE_FIELDS} for s in h.route['selected_packages']])
            self.assertEqual(data['root_selected_package_ids'], trace['root_selected_package_ids'])
        concept = next(p for p in h.payloads if p.get('text', {}).get('format', {}).get('name') == 'hub_t8_concept')
        data = handoff(concept)
        self.assertEqual(data['contribution']['state'], 'GENERATED_CONTRIBUTION_NOT_ACCEPTED_STATE')
        self.assertEqual(data['contribution']['output'], 'MOCK Hub answer')
        final = handoff(h.payloads[-1])
        self.assertEqual(final['contribution'], data['contribution'])
        self.assertEqual(final['scoped_package_output'], 'MOCK Hub answer')
        self.assertEqual(answer, 'MOCK Hub answer')
        self.assertFalse(any('tools' in p for p in h.payloads))
        self.assertEqual(len(h.payloads), 7)
        self.assertFalse(trace['ais_selected'])
        self.assertEqual(trace['unresolved_blockers'], [])

    def test_concept_stable_prefix_across_different_handoffs_and_full_ais_final(self):
        h = self.harness
        h.select(t8.CONCEPT)
        h.local['selected_leaves'] = [leaf('HUB-CAP-BRAINSTORM')]
        _, first = h.run_runtime()
        payload1 = h.payloads[1]
        h.payloads.clear()
        h.select(t8.TECHNICAL, t8.CONCEPT, t9.AIS)
        _, second = h.run_runtime()
        payload2 = h.payloads[2]
        marker = '[T8 VERIFIED HANDOFF]\n'
        prefix = payload1['instructions'].split(marker, 1)[0]
        self.assertEqual(prefix, payload2['instructions'].split(marker, 1)[0])
        bindings = t8.load_bindings(t8.BINDINGS_PATH.read_text(encoding='utf-8'))
        for stable in [app.HUB_CI_PATH.read_text(encoding='utf-8'),
                       app.t7_concept_binding_view(bindings),
                       *[app.t7_retrieve(bindings[t8.CONCEPT][key]) for key in ('entrypoint', 'local_catalog')]]:
            self.assertIn(stable, prefix)
        self.assertIn('Select Concept leaves', payload2['instructions'].split(marker, 1)[1])
        self.assertNotEqual(handoff(payload1), handoff(payload2))
        final = handoff(h.payloads[-1])
        ais = final['ais_evidence']
        for key, value in second.items():
            if key != 'packages':
                self.assertEqual(ais[key], value)
        self.assertEqual(ais['root_route'], h.route)
        self.assertEqual(ais['ais_output_text'], 'MOCK AIS evidence')
        self.assertTrue(ais['ais_web_search_executed'])
        self.assertTrue(all(item['verified'] for item in ais['ais_local_retrieval_evidence']))
        self.assertEqual(second['packages']['root_selected_package_ids'], [t8.TECHNICAL, t8.CONCEPT])
        self.assertFalse(second['packages']['authoring_active'])
        self.assertEqual(first['unresolved_blockers'], second['unresolved_blockers'])
        self.assertEqual(len(h.payloads), 4)
        self.assertEqual(sum('tools' in p for p in h.payloads), 1)


if __name__ == '__main__':
    unittest.main()
