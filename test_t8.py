import copy
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from openai import OpenAI
from streamlit.testing.v1 import AppTest

import app
import t8
import test_app
from test_t7 import package, leaf


class T8Tests(unittest.TestCase):
    def setUp(self):
        self.config = dict(openai_api_key='mock-only', model='mock-model')
        self.messages = [dict(role='user', content='/AUTHOR GENERIC\nprior'),
                         dict(role='assistant', content='prior prompt'),
                         dict(role='user', content='current turn, interpreted only by model')]
        self.route = dict(task_scope='current', selected_packages=[package(t8.AUTHORING)], unresolved_blockers=[])
        self.admission = dict(active=True, isolated=False, target='GENERIC', preset='NONE', contributor='NONE',
                              application_scope='current request', reason='mock admission', unresolved_blockers=[])
        self.owner = dict(module_id='HUB-DOM-CREATIVE', runtime_role='DOMAIN_CONTROL',
                          application_scope='scoped contribution only', protected_constraints=['locked premise', 'unknown stays open'],
                          provenance='current user supplied premise; generated content is proposed',
                          reason='mock Concept owner resolution', unresolved_blockers=[])
        self.payloads = []
        self.reads = []
        self.original_read = Path.read_bytes
        self.overrides = {}
        self.raw_responses = {}
        self.fail_phase = None
        self.failure = None
        self.manifest = json.loads(t8.BINDINGS_PATH.read_text(encoding='utf-8'))
        self.author_path = t8.BINDINGS_PATH.parent / 'packages/authoring/HUB-CAP-AUTHORING_v0.7.md'
        self.controls = [app.HUB_CI_PATH, app.HUB_ROUTER_PATH, app.HUB_ARCHITECTURE_PATH,
                         app.HUB_CATALOG_PATH, t8.BINDINGS_PATH]

    def client(self, **kwargs):
        self.assertEqual(kwargs['max_retries'], 0)
        self.assertEqual(kwargs['base_url'], 'https://api.openai.com/v1')
        def respond(request):
            payload = json.loads(request.content)
            self.payloads.append(payload)
            name = payload.get('text', {}).get('format', {}).get('name')
            records = {'hub_t8_root': self.route, 'hub_t8_admission': self.admission,
                       'hub_t8_contributor': self.owner,
                       'hub_t8_concept': dict(selected_leaves=[], unresolved_blockers=[])}
            text = self.raw_responses.get(name, json.dumps(records[name]) if name else
                ('scoped generated contribution' if self.admission.get('contributor') != 'NONE'
                 and len([p for p in self.payloads if 'text' not in p]) == 1 else 'final answer'))
            result = dict(id='resp_mock', object='response', created_at=0,
                status='completed', model='mock-model', output=[dict(id='msg_mock', type='message',
                role='assistant', status='completed', content=[dict(type='output_text', text=text, annotations=[])])])
            if name == self.fail_phase and self.failure:
                if self.failure == 'incomplete':
                    result['status'] = 'incomplete'
                elif self.failure == 'empty':
                    result['output'][0]['content'][0]['text'] = ''
                else:
                    result['output'][0]['content'] = [dict(type='refusal', refusal='mock refusal')]
            return httpx.Response(200, json=result)
        return OpenAI(**kwargs, http_client=httpx.Client(transport=httpx.MockTransport(respond)))

    def read(self, path):
        self.reads.append(path)
        value = self.overrides.get(path)
        if isinstance(value, Exception):
            raise value
        return value if value is not None else self.original_read(path)

    def run_t8(self):
        before = copy.deepcopy(self.messages)
        with patch.object(Path, 'read_bytes', lambda path: self.read(path)), patch.object(app, 'OpenAI', self.client):
            result = t8.call_t8(self.config, self.messages)
        self.assertEqual(self.messages, before)
        for payload in self.payloads:
            if payload.get("text", {}).get("format", {}).get("name") == "hub_t8_concept":
                self.assertEqual(payload["input"][2:], self.messages)
                self.assertEqual([m["role"] for m in payload["input"][:2]], ["developer", "developer"])
            else:
                self.assertEqual(payload['input'], self.messages)
            self.assertFalse(payload['store'])
            if 'text' in payload:
                self.assertTrue(payload['text']['format']['strict'])
        return result

    def contributor(self, name):
        self.admission['contributor'] = name
        module = 'HUB-DOM-CREATIVE' if name == 'CREATIVE' else 'HUB-CAP-BRAINSTORM'
        self.owner.update(module_id=module, runtime_role=leaf(module)['runtime_role'])

    def final(self):
        return self.payloads[-1]['instructions']

    def test_binding_inventory_exact_copy_and_t7_inventory(self):
        bindings = t8.load_bindings(t8.BINDINGS_PATH.read_text(encoding='utf-8'))
        old = app.t7_load_bindings(app.T7_BINDINGS_PATH.read_text(encoding='utf-8'))
        self.assertEqual(set(bindings), {t8.TECHNICAL, t8.CONCEPT, t8.AUTHORING})
        self.assertEqual({k: v for k, v in bindings.items() if k != t8.AUTHORING}, old)
        artifact = bindings[t8.AUTHORING]['entrypoint']
        self.assertTrue(self.author_path.resolve().is_relative_to(t8.BINDINGS_PATH.parent))
        self.assertEqual(self.author_path.read_bytes(),
                         app.HUB_CI_PATH.parent.joinpath('library_modules', self.author_path.name).read_bytes())
        self.assertEqual(hashlib.sha256(self.author_path.read_bytes()).hexdigest(), artifact['sha256'])

    def test_root_has_exact_controls_no_manifest_no_leaf_inventory(self):
        self.run_t8()
        instructions = self.payloads[0]['instructions']
        for path in self.controls[:-1]:
            self.assertIn(self.original_read(path).decode('utf-8'), instructions)
        self.assertNotIn('HUB-DOM-CREATIVE', instructions)
        self.assertNotIn('HUB-CAP-BRAINSTORM', instructions)
        self.assertNotIn('HUB-CAP-DEBATE', instructions)
        self.assertNotIn('"packages"', instructions)
        self.assertNotIn('sha256', instructions)
        self.assertEqual(self.reads, self.controls + [self.author_path])

    def test_all_targets_and_presets_exact_body_no_target_execution(self):
        for target in ('AIS', 'IMAGET', 'CODEX', 'WORK', 'GENERIC'):
            for preset in ('NONE', 'P1', 'P2', 'P3'):
                with self.subTest(target=target, preset=preset):
                    self.payloads.clear(); self.reads.clear()
                    self.admission.update(target=target, preset=preset)
                    _, trace = self.run_t8()
                    self.assertEqual(trace['authoring_target'], target)
                    self.assertEqual(trace['authoring_preset'], preset)
                    self.assertTrue(trace['authoring_active'])
                    self.assertTrue(trace['authoring_retrieved'])
                    self.assertEqual(trace['unresolved_blockers'], [])
                    self.assertIn(self.original_read(self.author_path).decode('utf-8'), self.final())
                    self.assertTrue(self.final().startswith(self.original_read(app.HUB_CI_PATH).decode('utf-8')))
                    self.assertEqual(self.reads, self.controls + [self.author_path])
                    self.assertEqual(len(self.payloads), 3)

    def test_impossible_and_malformed_admission_stops_no_retry(self):
        base = self.admission.copy()
        invalid = [dict(base, active=False), dict(base, active=False, target='NONE', preset='P1'),
                   dict(base, active=False, target='NONE', contributor='CREATIVE'), dict(base, active=True, target='NONE'),
                   dict(base, preset='P1', contributor='CREATIVE'), dict(base, target='FTH'),
                   dict(base, contributor='DEBATE'), dict(base, preset='P4'), dict(base, active=1),
                   dict(base, unresolved_blockers=[1]), dict(base, extra='x'), {}, [],
                   {k: v for k, v in base.items() if k != 'reason'}]
        for record in invalid:
            with self.subTest(record=record):
                self.admission = record
                self.payloads.clear()
                with self.assertRaises(ValueError):
                    self.run_t8()
                self.assertEqual(len(self.payloads), 2)

    def test_inactive_is_baseline_only_despite_prior_authoring(self):
        self.admission.update(active=False, target='NONE')
        self.route['selected_packages'].append(package(t8.TECHNICAL))
        _, trace = self.run_t8()
        self.assertFalse(trace['authoring_active'])
        self.assertNotIn(self.original_read(self.author_path).decode('utf-8'), self.final())
        self.assertNotIn(app.TECHNICAL_PATH, self.reads)
        self.assertIn('inactive', self.final())
        self.assertEqual(len(self.payloads), 3)

    def test_reread_and_recompute_every_turn_no_activation_carryover(self):
        self.run_t8()
        self.admission.update(active=False, target='NONE')
        # A clarification or reauthor-like history cannot activate the host itself.
        self.messages[-1]['content'] = 'clarification / reauthor answer without fresh trigger'
        self.payloads.clear(); self.reads.clear()
        self.overrides[app.HUB_ROUTER_PATH] = self.original_read(app.HUB_ROUTER_PATH) + b'\n# current reread\n'
        _, trace = self.run_t8()
        self.assertFalse(trace['authoring_active'])
        self.assertEqual(self.reads, self.controls + [self.author_path])
        self.assertIn('# current reread', self.payloads[0]['instructions'])
        self.route['selected_packages'] = []
        self.payloads.clear(); self.reads.clear()
        self.run_t8()
        self.assertEqual(self.reads, self.controls)
        self.assertEqual(len(self.payloads), 2)
        self.assertNotIn(self.original_read(self.author_path).decode('utf-8'), self.final())
        self.overrides[t8.BINDINGS_PATH] = b'{}'
        with patch.object(Path, 'read_bytes', lambda path: self.read(path)), patch.object(app, 'OpenAI') as client:
            with self.assertRaises(ValueError):
                t8.call_t8(self.config, self.messages)
            client.assert_not_called()

    def test_both_contributor_paths_scoped_artifact_no_other_leaf_or_target(self):
        for name, path in (('CREATIVE', app.CREATIVE_PATH), ('BRAINSTORM', app.BRAINSTORM_PATH)):
            for target in ('AIS', 'IMAGET', 'CODEX', 'WORK', 'GENERIC'):
                with self.subTest(name=name, target=target):
                    self.contributor(name)
                    self.admission['target'] = target
                    self.payloads.clear(); self.reads.clear()
                    _, trace = self.run_t8()
                    self.assertEqual(self.reads, self.controls + [self.author_path, app.CONCEPT_CORE_PATH,
                                                                app.CONCEPT_CATALOG_PATH, path])
                    self.assertEqual(trace['contributor_retrieved_module_ids'], [self.owner['module_id']])
                    self.assertEqual(trace['locally_retrieved_package_ids'], [t8.AUTHORING, t8.CONCEPT])
                    self.assertEqual(trace['unresolved_blockers'], [])
                    self.assertEqual(len(self.payloads), 5)
                    owner_phase = self.payloads[2]['instructions']
                    self.assertIn('[T8 CONCEPT OWNER LOCAL BINDING AVAILABILITY]', owner_phase)
                    self.assertIn('Expected pending post-selection body retrieval is not an unresolved blocker', owner_phase)
                    self.assertNotIn(self.original_read(path).decode('utf-8'), owner_phase)
                    self.assertIn('scoped generated contribution', self.final())
                    self.assertIn('GENERATED_CONTRIBUTION_NOT_ACCEPTED_STATE', self.final())
                    for constraint in self.owner['protected_constraints']:
                        self.assertIn(constraint, self.final())
                    self.assertIn(self.owner['provenance'], self.final())
                    for control in (app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH, path):
                        self.assertNotIn(self.original_read(control).decode('utf-8'), self.final())
                    self.assertIn(self.original_read(path).decode('utf-8'), self.payloads[-2]['instructions'])

    def test_contributor_identity_mismatch_debate_unknown_and_role_block(self):
        self.contributor('CREATIVE')
        base = self.owner.copy()
        for bad in (dict(base, module_id='HUB-CAP-BRAINSTORM', runtime_role='CAPABILITY'),
                    dict(base, module_id='HUB-CAP-DEBATE', runtime_role='CAPABILITY'),
                    dict(base, module_id='UNKNOWN'), dict(base, runtime_role='CAPABILITY')):
            with self.subTest(bad=bad):
                self.owner = bad
                self.payloads.clear(); self.reads.clear()
                _, trace = self.run_t8()
                self.assertTrue(trace['unresolved_blockers'])
                self.assertEqual(trace['contributor_retrieved_module_ids'], [])
                self.assertEqual(len(self.payloads), 4)
                self.assertNotIn(app.CREATIVE_PATH, self.reads)
                self.assertNotIn(self.original_read(self.author_path).decode('utf-8'), self.final())
                self.assertIn('single-target-equivalent', self.final())

    def test_interface_leaf_and_authoring_failures_block_without_fallback(self):
        self.contributor('CREATIVE')
        for path in (self.author_path, app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH, app.CREATIVE_PATH):
            for failure in (FileNotFoundError(), PermissionError(), OSError(), b'tampered', b'\xff'):
                with self.subTest(path=path, failure=failure):
                    self.overrides = {path: failure}
                    self.payloads.clear(); self.reads.clear()
                    _, trace = self.run_t8()
                    self.assertTrue(trace['unresolved_blockers'])
                    self.assertEqual(trace['contributor_retrieved_module_ids'], [])
                    self.assertNotIn(self.original_read(self.author_path).decode('utf-8'), self.final())
                    self.assertTrue(set(self.reads).issubset(set(self.controls + [self.author_path,
                        app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH, app.CREATIVE_PATH])))

    def test_utf8_failure_after_valid_hash_and_path_escape(self):
        manifest = copy.deepcopy(self.manifest)
        manifest['packages'][t8.AUTHORING]['entrypoint']['sha256'] = hashlib.sha256(b'\xff').hexdigest()
        self.overrides = {t8.BINDINGS_PATH: json.dumps(manifest).encode(), self.author_path: b'\xff'}
        _, trace = self.run_t8()
        self.assertFalse(trace['authoring_retrieved'])
        self.assertTrue(trace['unresolved_blockers'])
        self.contributor('CREATIVE')
        for path in ('../upstream/body.md', 'upstream/body.md', 'C:/outside/body.md', 'runtime/../../body.md'):
            manifest = copy.deepcopy(self.manifest)
            manifest['packages'][t8.CONCEPT]['leaves'][0]['path'] = path
            self.overrides = {t8.BINDINGS_PATH: json.dumps(manifest).encode()}
            self.payloads.clear(); self.reads.clear()
            _, trace = self.run_t8()
            self.assertTrue(trace['unresolved_blockers'])
            self.assertEqual(self.reads, self.controls + [self.author_path, app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH])

    def test_owner_blockers_preserved_no_execution(self):
        self.contributor('CREATIVE')
        self.owner['unresolved_blockers'] = ['material relationship unresolved']
        _, trace = self.run_t8()
        self.assertIn('material relationship unresolved', trace['unresolved_blockers'])
        self.assertNotIn(app.CREATIVE_PATH, self.reads)
        self.assertNotIn(self.original_read(self.author_path).decode('utf-8'), self.final())

    def test_admission_blockers_preserved_no_authoring_execution(self):
        self.admission['unresolved_blockers'] = ['missing decisive source']
        _, trace = self.run_t8()
        self.assertIn('missing decisive source', trace['unresolved_blockers'])
        self.assertNotIn(self.original_read(self.author_path).decode('utf-8'), self.final())

    def test_admission_pending_contributor_is_next_stage_not_blocker(self):
        self.contributor('BRAINSTORM')
        _, trace = self.run_t8()
        admission = self.payloads[1]['instructions']
        self.assertIn('Contributor resolution is intentionally pending until after admission.', admission)
        self.assertIn('Pending contributor resolution is normal next-stage state, not an unresolved blocker.', admission)
        self.assertIn('Report genuine admission blockers unchanged.', admission)
        self.assertEqual(trace['unresolved_blockers'], [])
        self.assertEqual(trace['contributor_retrieved_module_ids'], ['HUB-CAP-BRAINSTORM'])

    def test_contributor_exact_catalog_role_contract(self):
        for name in ('CREATIVE', 'BRAINSTORM'):
            with self.subTest(name=name):
                self.contributor(name)
                self.payloads.clear()
                self.run_t8()
                owner = self.payloads[2]
                self.assertEqual(owner['text']['format']['schema']['properties']['runtime_role'],
                                 dict(type='string', enum=['DOMAIN_CONTROL', 'CAPABILITY']))
                self.assertIn('runtime_role must be the exact Catalog identifier; never translate it.',
                              owner['instructions'])

    def test_translated_contributor_role_rejected_without_retry(self):
        self.contributor('BRAINSTORM')
        for role in ('NĂNG LỰC', 'NANG LUC', 'capability', 'UNKNOWN'):
            with self.subTest(role=role):
                self.owner['runtime_role'] = role
                self.payloads.clear(); self.reads.clear()
                with self.assertRaisesRegex(ValueError, 'structured'):
                    self.run_t8()
                self.assertEqual(len(self.payloads), 3)
                self.assertNotIn(app.BRAINSTORM_PATH, self.reads)

    def test_controls_and_manifest_failure_before_client(self):
        for path in self.controls:
            for failure in (FileNotFoundError(), PermissionError(), OSError(), b'\xff', b'', b'\x00'):
                self.overrides = {path: failure}
                with self.subTest(path=path, failure=failure), patch.object(Path, 'read_bytes', lambda path: self.read(path)), patch.object(app, 'OpenAI') as client:
                    with self.assertRaises(ValueError):
                        t8.call_t8(self.config, self.messages)
                    client.assert_not_called()

    def test_invalid_manifest_inventory_identity_duplicate_and_shape(self):
        invalid = ['{}', '[]', '{', '{"binding_version":"0.2","binding_version":"0.2"}']
        for key, value in (('binding_version', '0.1'), ('retrieval_authority', 'LIBRARY_MODULE'), ('status', 'INACTIVE')):
            manifest = copy.deepcopy(self.manifest); manifest[key] = value
            invalid.append(json.dumps(manifest))
        for key, value in (('module_id', 'FAKE'), ('runtime_role', 'DOMAIN_CONTROL'), ('version', '0.6'),
                           ('path', 'upstream/body.md'), ('sha256', 'invalid')):
            manifest = copy.deepcopy(self.manifest); manifest['packages'][t8.AUTHORING]['entrypoint'][key] = value
            invalid.append(json.dumps(manifest))
        for package_id in (t8.AUTHORING, t8.TECHNICAL, t8.CONCEPT):
            manifest = copy.deepcopy(self.manifest); del manifest['packages'][package_id]
            invalid.append(json.dumps(manifest))
        manifest = copy.deepcopy(self.manifest); manifest['packages']['HUB-PKG-AIS'] = {}
        invalid.append(json.dumps(manifest))
        for text in invalid:
            self.overrides = {t8.BINDINGS_PATH: text.encode()}
            with self.subTest(text=text), patch.object(Path, 'read_bytes', lambda path: self.read(path)), patch.object(app, 'OpenAI') as client:
                with self.assertRaises(ValueError):
                    t8.call_t8(self.config, self.messages)
                client.assert_not_called()

    def test_invalid_root_and_contributor_shape_no_retry(self):
        for phase in ('hub_t8_root', 'hub_t8_admission', 'hub_t8_contributor'):
            self.contributor('CREATIVE')
            for text in ('[]', '{}', '{', 'null'):
                self.raw_responses = {phase: text}; self.payloads.clear()
                with self.subTest(phase=phase, text=text), self.assertRaises(ValueError):
                    self.run_t8()
                self.assertEqual(len(self.payloads), {'hub_t8_root': 1, 'hub_t8_admission': 2, 'hub_t8_contributor': 3}[phase])

    def test_unbound_root_targets_block_but_authoring_target_is_independent(self):
        self.route['selected_packages'] += [package('HUB-PKG-AIS'), package('HUB-PKG-IMAGET')]
        self.admission['target'] = 'AIS'
        _, trace = self.run_t8()
        self.assertEqual(len(trace['unresolved_blockers']), 2)
        self.assertTrue(trace['authoring_active'])
        self.assertIn(self.original_read(self.author_path).decode('utf-8'), self.final())
        self.assertEqual(self.reads, self.controls + [self.author_path])

    def test_non_authoring_root_technical_and_concept_use_verified_interfaces(self):
        self.route['selected_packages'] = [package(t8.TECHNICAL), package(t8.CONCEPT)]
        _, trace = self.run_t8()
        self.assertFalse(trace['authoring_retrieved'])
        self.assertEqual(trace['locally_retrieved_package_ids'], [t8.TECHNICAL, t8.CONCEPT])
        self.assertEqual(trace['unresolved_blockers'], [])
        self.assertNotIn(self.author_path, self.reads)
        self.assertIn(self.original_read(app.TECHNICAL_PATH).decode('utf-8'), self.final())

    def test_response_failure_each_phase_stops_without_retry_or_history_mutation(self):
        self.contributor('CREATIVE')
        for phase, count in (('hub_t8_root', 1), ('hub_t8_admission', 2), ('hub_t8_contributor', 3), (None, 4)):
            for failure in ('incomplete', 'empty', 'refusal'):
                self.fail_phase = phase; self.failure = failure; self.payloads.clear()
                before = copy.deepcopy(self.messages)
                with self.subTest(phase=phase, failure=failure), self.assertRaises(ValueError):
                    self.run_t8()
                self.assertEqual(len(self.payloads), count)
                self.assertEqual(self.messages, before)
        self.admission['contributor'] = 'NONE'
        for failure in ('incomplete', 'empty', 'refusal'):
            self.fail_phase = None; self.failure = failure; self.payloads.clear()
            with self.subTest(final=failure), self.assertRaises(ValueError):
                self.run_t8()
            self.assertEqual(len(self.payloads), 3)

    def test_invalid_root_identity_and_duplicate_fail_current_request(self):
        good = package(t8.AUTHORING)
        for records in ([dict(good, package_id='UNKNOWN')], [dict(good, runtime_role='TOOL_PIPELINE')], [good, good]):
            self.route['selected_packages'] = records
            self.payloads.clear()
            with self.subTest(records=records), self.assertRaises(ValueError):
                self.run_t8()
            self.assertEqual(len(self.payloads), 1)

    def test_owner_malformed_fields_fail_instead_of_guessing(self):
        self.contributor('CREATIVE')
        base = self.owner.copy()
        for bad in (dict(base, protected_constraints='not an array'), dict(base, protected_constraints=[1]),
                    dict(base, provenance=None), dict(base, unresolved_blockers=[False]), dict(base, extra='x')):
            self.owner = bad; self.payloads.clear()
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.run_t8()
            self.assertEqual(len(self.payloads), 3)

    def test_invalid_ordinary_concept_selection_fails_request(self):
        self.route['selected_packages'] = [package(t8.CONCEPT)]
        self.raw_responses['hub_t8_concept'] = '{}'
        with self.assertRaises(ValueError):
            self.run_t8()
        self.assertEqual(len(self.payloads), 2)

    def test_binding_catalog_version_and_interface_mismatch_block(self):
        self.contributor('CREATIVE')
        for path, old, new in (
            (app.HUB_CATALOG_PATH, b"version: '0.7'", b"version: '9.0'"),
            (app.HUB_CATALOG_PATH, b'    module_id: HUB-CATALOG-CONCEPT-DEVELOPMENT', b'    module_id: FAKE'),
            (app.CONCEPT_CATALOG_PATH, b'- module_id: HUB-DOM-CREATIVE', b'- module_id: FAKE')):
            changed = self.original_read(path).replace(old, new, 1)
            self.assertNotEqual(changed, self.original_read(path))
            self.overrides = {path: changed}
            if path == app.CONCEPT_CATALOG_PATH:
                manifest = copy.deepcopy(self.manifest)
                manifest['packages'][t8.CONCEPT]['local_catalog']['sha256'] = hashlib.sha256(changed).hexdigest()
                self.overrides[t8.BINDINGS_PATH] = json.dumps(manifest).encode()
            self.payloads.clear(); self.reads.clear()
            _, trace = self.run_t8()
            self.assertTrue(trace['unresolved_blockers'])
            self.assertNotIn(app.CREATIVE_PATH, self.reads)
            self.assertNotIn(self.original_read(self.author_path).decode('utf-8'), self.final())

    def test_ui_t8_history_t3_isolation_and_failure_preserves_state(self):
        with test_app.Stage2Tests.ui_context(self), patch.object(app, 'OpenAI', self.client):
            ui = AppTest.from_file('app.py').run()
            ui.radio[0].set_value(app.MODES[8]).run()
            ui.text_area[0].set_value('current')
            ui.button[0].click().run()
            self.assertFalse(ui.exception)
            self.assertFalse(ui.error)
            self.assertEqual(ui.chat_message[-1].caption[0].value, app.MODES[8])
            history = list(ui.session_state.messages)
            labels = dict(ui.session_state.response_modes)
            import test_t3
            routing = test_t3.T3Tests(); routing.setUp()
            with patch('openai.OpenAI', routing.client):
                ui.radio[0].set_value(app.MODES[3]).run()
                ui.text_area[0].set_value('T3 isolated')
                ui.button[0].click().run()
            self.assertEqual(routing.payloads[-1]['input'], [dict(role='user', content='T3 isolated')])
            self.assertEqual(ui.session_state.messages, history)
            routes = list(ui.session_state.route_records)
            ui.radio[0].set_value(app.MODES[8]).run()
            with patch.object(Path, 'read_bytes', side_effect=FileNotFoundError()):
                ui.text_area[0].set_value('keep current')
                ui.button[0].click().run()
            self.assertTrue(ui.error)
            self.assertEqual(ui.session_state.messages, history)
            self.assertEqual(ui.session_state.response_modes, labels)
            self.assertEqual(ui.session_state.route_records, routes)
            self.assertEqual(ui.text_area[0].value, 'keep current')
            self.raw_responses['hub_t8_admission'] = '{}'
            ui.button[0].click().run()
            self.assertTrue(ui.error)
            self.assertEqual(ui.session_state.messages, history)


    def test_isolated_targets_presets_and_explicit_handoff_no_execution(self):
        # Model records are mocked: this verifies host transport/invariants, not live lexical admission.
        for target in ('AIS', 'IMAGET', 'CODEX', 'WORK', 'GENERIC'):
            for preset in ('NONE', 'P1', 'P2', 'P3'):
                with self.subTest(target=target, preset=preset):
                    self.payloads.clear(); self.reads.clear()
                    suffix = '' if preset == 'NONE' else f' {preset}'
                    self.messages[-1]['content'] = f'/AUTHOR {target}{suffix} ISOLATED\nCreate a prompt only.'
                    self.admission.update(target=target, preset=preset, isolated=True)
                    _, trace = self.run_t8()
                    self.assertTrue(trace['authoring_isolated'])
                    handoff = json.JSONDecoder().raw_decode(self.final().split('[T8 VERIFIED HANDOFF]\n')[1])[0]
                    self.assertTrue(handoff['admission']['isolated'])
                    self.assertEqual(handoff['admission']['preset'], preset)
                    self.assertEqual(len(self.payloads), 3)
                    self.assertTrue(all('tools' not in p for p in self.payloads))
                    self.assertEqual(self.reads, self.controls + [self.author_path])

    def test_invalid_isolated_records_stop_before_final(self):
        base = self.admission.copy()
        invalid = [dict(base, isolated=True, active=False, target='NONE'),
                   dict(base, isolated=True, contributor='CREATIVE'),
                   dict(base, isolated=True, contributor='BRAINSTORM'),
                   dict(base, isolated='true'), dict(base, isolated=1),
                   {k: v for k, v in base.items() if k != 'isolated'}]
        for record in invalid:
            with self.subTest(record=record):
                self.payloads.clear(); self.reads.clear()
                self.admission = record
                with self.assertRaisesRegex(ValueError, 'structured'):
                    self.run_t8()
                self.assertEqual(len(self.payloads), 2)

    def test_isolated_no_persistence_clarification_and_normal_context(self):
        self.messages[-1]['content'] = '/AUTHOR GENERIC ISOLATED\nCreate a prompt.'
        self.admission['isolated'] = True
        self.assertTrue(self.run_t8()[1]['authoring_isolated'])
        for content, active in [('Clarification without fresh trigger', False),
                                ('Reauthor it without fresh trigger', False),
                                ('/AUTHOR GENERIC\nUse the earlier source.', True)]:
            self.payloads.clear(); self.reads.clear()
            self.messages[-1]['content'] = content
            self.admission.update(active=active, target='GENERIC' if active else 'NONE', isolated=False)
            _, trace = self.run_t8()
            self.assertFalse(trace['authoring_isolated'])
            self.assertEqual(trace['authoring_active'], active)
            self.assertEqual(self.payloads[-1]['input'], self.messages)

    def test_isolated_keeps_history_and_mandatory_source_boundary_controls(self):
        self.messages[1]['content'] = 'CANARY_AMBIENT is an accepted decision.'
        self.messages[-1]['content'] = '/AUTHOR GENERIC ISOLATED\nCompare only current options.'
        self.admission['isolated'] = True
        self.run_t8()
        for payload in self.payloads:
            self.assertEqual(payload['input'], self.messages)
        for boundary in ('SOURCE ISOLATION != CONTROL ISOLATION',
                         'accessible material explicitly referenced there with sufficient identification',
                         'Exclude unreferenced prior conversation, prior assistant conclusions',
                         'not a channel for importing excluded task objectives',
                         'do not inherit an isolation mode or source selection automatically'):
            self.assertIn(boundary, self.final())
        self.assertIn(self.original_read(app.HUB_CI_PATH).decode('utf-8'), self.final())

    def test_isolated_genuine_blocker_remains_and_blocks_authoring(self):
        self.admission.update(isolated=True, unresolved_blockers=['Decisive source is ambiguous.'])
        _, trace = self.run_t8()
        self.assertIn('Decisive source is ambiguous.', trace['unresolved_blockers'])
        self.assertIn('Do not execute Authoring.', self.final())
        self.assertNotIn('# Prompt Authoring', self.final())

    def test_malformed_isolation_model_inactive_is_not_repaired_by_host(self):
        fixtures = app.HUB_CI_PATH.parent / 'candidates/authoring_v0_7/ISOLATION_TEST_CASES.json'
        cases = json.loads(fixtures.read_text(encoding='utf-8'))['cases']
        invalid = next(case['invalid'] for case in cases if case['id'] == 'I8')
        self.admission.update(active=False, target='NONE', isolated=False)
        for text in invalid:
            with self.subTest(text=text):
                self.payloads.clear(); self.reads.clear()
                self.messages[-1]['content'] = text
                _, trace = self.run_t8()
                self.assertFalse(trace['authoring_active'])
                self.assertFalse(trace['authoring_isolated'])
                self.assertNotIn('# Prompt Authoring', self.final())
                self.assertEqual(self.payloads[1]['input'][-1]['content'], text)


if __name__ == '__main__':
    unittest.main()
