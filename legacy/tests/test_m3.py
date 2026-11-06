"""Concept-only explicit caching: verify serialized SDK payloads without network."""
import copy
import json
import subprocess
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import app
import runtime_host
import m1
import t8
import t9
import test_m1
from test_t7 import leaf


def handoff(text):
    return json.JSONDecoder().raw_decode(text.split('[T8 VERIFIED HANDOFF]\n', 1)[1])[0]


class ExplicitConceptTests(unittest.TestCase):
    def harness(self, workload):
        h = test_m1.M1Tests()
        h.setUp()
        self.addCleanup(h.doCleanups)
        h.messages = [dict(role='user', content='earlier'), dict(role='assistant', content='prior'),
                      dict(role='user', content='current scope')]
        h.local['selected_leaves'] = [leaf('HUB-CAP-BRAINSTORM')]
        if workload == 1:
            h.select(t8.AUTHORING, t8.CONCEPT)
            h.admission.update(target='GENERIC', contributor='BRAINSTORM')
            h.owner.update(module_id='HUB-CAP-BRAINSTORM', runtime_role='CAPABILITY')
        else:
            h.select(t8.TECHNICAL, t8.CONCEPT, t9.AIS)
        return h

    def test_serialized_pair_and_unchanged_other_phases_against_head(self):
        baseline = types.ModuleType('baseline_t8')
        source = subprocess.check_output(['git', 'show',
            'dfd2d1d07bed7a5c4789796d77b57db00689f686:t8.py']).decode('utf-8')
        exec(compile(source, 'baseline_t8.py', 'exec'), baseline.__dict__)
        baseline.host = runtime_host  # Historical code uses the current primitive owner.
        prefixes = []
        for number, count in ((1, 7), (2, 4)):
            with self.subTest(workload=number):
                h = self.harness(number)
                before = copy.deepcopy(h.messages)
                with patch.object(runtime_host, 'OpenAI', h.client):
                    current_result = m1.call_runtime(h.config, h.messages)
                current = copy.deepcopy(h.payloads)
                h.payloads.clear()
                with patch.object(runtime_host, 'OpenAI', h.client), patch.object(t8, 'call_t8', baseline.call_t8):
                    baseline_result = m1.call_runtime(h.config, h.messages)
                self.assertEqual(h.messages, before)
                self.assertEqual(current_result, baseline_result)
                self.assertEqual(len(current), count)
                self.assertEqual(len(h.payloads), count)
                self.assertEqual(sum('tools' in p for p in current), number - 1)
                for new, old in zip(current, h.payloads):
                    if new.get('text', {}).get('format', {}).get('name') != 'hub_t8_concept':
                        self.assertEqual(new, old)
                        self.assertNotIn('prompt_cache_key', new)
                        self.assertNotIn('prompt_cache_options', new)
                        self.assertNotIn('prompt_cache_breakpoint', json.dumps(new))
                        continue
                    bindings = t8.load_bindings(t8.BINDINGS_PATH.read_text(encoding='utf-8'))
                    controls = [app.HUB_CI_PATH.read_text(encoding='utf-8'),
                        app.t7_concept_binding_view(bindings),
                        *[app.t7_retrieve(bindings[t8.CONCEPT][k]) for k in ('entrypoint', 'local_catalog')]]
                    self.assertEqual(new['instructions'], '\n\n'.join(controls))
                    self.assertNotIn('[T8 VERIFIED HANDOFF]', new['instructions'])
                    self.assertEqual(new['input'][0], {'role': 'developer', 'content': [{
                        'type': 'input_text',
                        'text': 'Concept cache boundary only; changes no authority or semantics.',
                        'prompt_cache_breakpoint': {'mode': 'explicit'}}]})
                    self.assertEqual(new['input'][1]['role'], 'developer')
                    dynamic = new['input'][1]['content'][0]
                    self.assertEqual(dynamic['type'], 'input_text')
                    self.assertEqual(handoff(dynamic['text']), handoff(old['instructions']))
                    data = handoff(dynamic['text'])
                    self.assertEqual(data['selected_packages'], handoff(old['instructions'])['selected_packages'])
                    self.assertTrue(data['verified_artifacts'])
                    if number == 1:
                        self.assertEqual(data['contribution']['output'], 'MOCK Hub answer')
                        self.assertEqual(data['contribution']['state'], 'GENERATED_CONTRIBUTION_NOT_ACCEPTED_STATE')
                        final = handoff(current[-1]['instructions'])
                        self.assertEqual(final['contribution'], data['contribution'])
                        self.assertEqual(final['scoped_package_output'], 'MOCK Hub answer')
                    else:
                        self.assertEqual(data['ais_evidence']['ais_output_text'], 'MOCK AIS evidence')
                        self.assertTrue(data['ais_evidence']['ais_web_search_executed'])
                        self.assertEqual(data['ais_evidence'], handoff(current[-1]['instructions'])['ais_evidence'])
                    phase = ('Select Concept leaves for current selected scopes only under exact core/Catalog. '
                             'Pending post-selection retrieval is not a blocker.')
                    # Exact legacy handoff, including its binding note, moves intact.
                    legacy_handoff = old['instructions'][len(controls[0]) + 2:].split(
                        '\n\n' + controls[1], 1)[0]
                    self.assertEqual(dynamic['text'], legacy_handoff + '\n\n' + phase)
                    self.assertEqual(new['input'][2:], old['input'])
                    self.assertEqual(new['text'], old['text'])
                    self.assertEqual(new['text']['format']['schema'], app.LEAF_SCHEMA)
                    self.assertEqual(new['prompt_cache_key'], 'central-hub:t8-concept:v1')
                    self.assertEqual(new['prompt_cache_options'], {'mode': 'explicit', 'ttl': '30m'})
                    self.assertNotIn('extra_body', new)
                    self.assertEqual(json.dumps(new).count('prompt_cache_breakpoint'), 1)
                    self.assertEqual(set(new) - set(old), {'prompt_cache_key', 'prompt_cache_options'})
                    for key in set(old) - {'instructions', 'input'}:
                        self.assertEqual(new[key], old[key])
                    prefixes.append((new['instructions'], new['input'][0], new['text'], new['prompt_cache_key']))
        self.assertEqual(prefixes[0], prefixes[1])

    def test_leaf_validation_matches_existing_validator(self):
        from test_t8 import T8Tests
        h = T8Tests()
        h.setUp()
        self.addCleanup(h.doCleanups)
        from test_t7 import package
        h.route['selected_packages'] = [package(t8.CONCEPT)]
        for record in ({}, {'selected_leaves': 'bad', 'unresolved_blockers': []},
                       {'selected_leaves': [dict(leaf('HUB-CAP-BRAINSTORM'), reason=7)], 'unresolved_blockers': []},
                       {'selected_leaves': [], 'unresolved_blockers': [False]}):
            with self.subTest(record=record):
                h.payloads.clear()
                h.raw_responses['hub_t8_concept'] = json.dumps(record)
                with self.assertRaises(ValueError):
                    h.run_t8()
                self.assertEqual(len(h.payloads), 2)
        h.raw_responses.clear()
        for failure in ('incomplete', 'refusal'):
            h.fail_phase, h.failure = 'hub_t8_concept', failure
            with self.subTest(failure=failure), self.assertRaises(ValueError):
                h.run_t8()


if __name__ == '__main__':
    unittest.main()
