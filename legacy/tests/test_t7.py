import copy
import hashlib
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from openai import OpenAI
from streamlit.testing.v1 import AppTest

import app
import test_app
import test_t3


TECH = 'HUB-PKG-TECHNICAL'
CONCEPT = 'HUB-PKG-CONCEPT-DEVELOPMENT'


def package(package_id):
    identities = {
        TECH: ('HUB-DOM-TECHNICAL', 'REASONING_PROFILE'),
        CONCEPT: ('HUB-DOM-CONCEPT-DEVELOPMENT', 'DOMAIN_CONTROL'),
        'HUB-PKG-AUTHORING': ('HUB-CAP-AUTHORING', 'CAPABILITY'),
        'HUB-PKG-AIS': ('HUB-PIPE-AIS', 'TOOL_PIPELINE'),
        'HUB-PKG-IMAGET': ('HUB-PIPE-IMAGET', 'TOOL_PIPELINE'),
    }
    module, role = identities[package_id]
    return dict(package_id=package_id, entrypoint_module_id=module, runtime_role=role,
                application_scope='current scoped portion: '+package_id, reason='model selection fixture')


def leaf(module_id):
    return dict(module_id=module_id, runtime_role='DOMAIN_CONTROL' if module_id == 'HUB-DOM-CREATIVE' else 'CAPABILITY',
                application_scope='current explicit span: '+module_id, reason='model selection fixture')


class T7Tests(unittest.TestCase):
    ui_context = test_app.Stage2Tests.ui_context

    def setUp(self):
        self.config = {'openai_api_key': 'test-key', 'model': 'gpt-5.6-sol'}
        self.payloads = []
        self.reads = []
        self.original_read = Path.read_bytes
        self.route = dict(task_scope='current task', selected_packages=[], unresolved_blockers=[])
        self.local = dict(selected_leaves=[], unresolved_blockers=[])
        self.manifest = json.loads(app.T7_BINDINGS_PATH.read_text(encoding='utf-8'))
        self.controls = [app.HUB_CI_PATH, app.HUB_ROUTER_PATH, app.HUB_ARCHITECTURE_PATH,
                         app.HUB_CATALOG_PATH, app.T7_BINDINGS_PATH]
        self.history = [{'role': 'user', 'content': 'prior'}, {'role': 'assistant', 'content': 'prior reply'},
                        {'role': 'user', 'content': 'current /DEBATE literal? #'}]

    def client(self, **kwargs):
        self.assertEqual(kwargs['max_retries'], 0)
        self.assertEqual(kwargs['base_url'], 'https://api.openai.com/v1')
        self.assertEqual(kwargs['timeout'], 120.0)

        def respond(request):
            payload = json.loads(request.content)
            self.payloads.append(payload)
            name = payload.get('text', {}).get('format', {}).get('name')
            text = json.dumps(self.route if name == 'hub_t7_root' else self.local) if name else 'Phản hồi T7.'
            return httpx.Response(200, json={
                'id': 'resp_t7', 'object': 'response', 'created_at': 0, 'status': 'completed',
                'model': self.config['model'], 'output': [{'id': 'msg_t7', 'type': 'message',
                'role': 'assistant', 'status': 'completed', 'content': [
                    {'type': 'output_text', 'text': text, 'annotations': []}]}],
            })
        return OpenAI(**kwargs, http_client=httpx.Client(transport=httpx.MockTransport(respond)))

    def run_t7(self):
        def read(path):
            self.reads.append(path)
            return self.original_read(path)
        with patch.object(Path, 'read_bytes', read), patch.object(app, 'OpenAI', self.client):
            return app.call_t7(self.config, self.history)

    def test_manifest_inventory_paths_hashes_and_unchanged_runtime(self):
        bindings = app.t7_load_bindings(app.T7_BINDINGS_PATH.read_text(encoding='utf-8'))
        self.assertEqual(set(bindings), {TECH, CONCEPT})
        artifacts = [bindings[TECH]['entrypoint'], bindings[CONCEPT]['entrypoint'],
                     bindings[CONCEPT]['local_catalog'], *bindings[CONCEPT]['leaves']]
        self.assertEqual([a['module_id'] for a in artifacts], [
            'HUB-DOM-TECHNICAL', 'HUB-DOM-CONCEPT-DEVELOPMENT', 'HUB-CATALOG-CONCEPT-DEVELOPMENT',
            'HUB-DOM-CREATIVE', 'HUB-CAP-BRAINSTORM', 'HUB-CAP-DEBATE'])
        repo = Path(app.__file__).resolve().parent
        for artifact in artifacts:
            path = (repo / artifact['path']).resolve()
            self.assertTrue(path.is_relative_to(repo/'runtime'))
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), artifact['sha256'])
            self.assertEqual(app.t7_retrieve(artifact).encode('utf-8'), path.read_bytes())
            committed = subprocess.check_output(['git', 'show', 'HEAD:'+artifact['path']])
            self.assertEqual(path.read_bytes(), committed)

    def test_root_rereads_exact_controls_and_config_without_bodies(self):
        for turn in range(2):
            answer, trace = self.run_t7()
            self.assertEqual(answer, 'Phản hồi T7.')
            root, final = self.payloads[-2:]
            for path in self.controls[:4]:
                self.assertIn(path.read_bytes().decode('utf-8'), root['instructions'])
            self.assertNotIn(app.T7_BINDINGS_PATH.read_text(encoding='utf-8'), root['instructions'])
            for leaf_id in ('HUB-DOM-CREATIVE', 'HUB-CAP-BRAINSTORM', 'HUB-CAP-DEBATE'):
                self.assertNotIn(leaf_id, root['instructions'])
            self.assertEqual(root['text']['format']['schema'], app.ROUTE_SCHEMA)
            self.assertTrue(root['text']['format']['strict'])
            self.assertEqual(trace['locally_retrieved_module_ids'], [])
            self.assertTrue(final['instructions'].startswith(app.HUB_CI_PATH.read_text(encoding='utf-8')))
            for path in (app.TECHNICAL_PATH, app.CONCEPT_CORE_PATH, app.CREATIVE_PATH):
                self.assertNotIn(path.read_text(encoding='utf-8'), root['instructions'])
                self.assertNotIn(path.read_text(encoding='utf-8'), final['instructions'])
        self.assertEqual(self.reads, self.controls*2)
        for payload in self.payloads:
            self.assertEqual(payload['input'], self.history)
            self.assertEqual(payload['model'], self.config['model'])
            self.assertFalse(payload['store'])

    def test_controls_and_config_changes_are_seen_next_request(self):
        original = self.original_read
        changed = False
        reads = []
        def read(path):
            reads.append(path)
            if path in self.controls[:4]:
                return original(path) + (b'\n# fresh-control\n' if changed else b'')
            if path == app.T7_BINDINGS_PATH and changed:
                manifest = copy.deepcopy(self.manifest)
                manifest['host_purpose'] += ' fresh-binding'
                return json.dumps(manifest).encode()
            return original(path)
        with patch.object(Path, 'read_bytes', read), patch.object(app, 'OpenAI', self.client):
            app.call_t7(self.config, self.history)
            changed = True
            app.call_t7(self.config, self.history)
        self.assertNotIn('fresh-control', self.payloads[0]['instructions'])
        self.assertEqual(self.payloads[2]['instructions'].count('fresh-control'), 4)
        self.assertNotIn('fresh-binding', self.payloads[2]['instructions'])
        self.assertEqual(reads.count(app.T7_BINDINGS_PATH), 2)

    def test_technical_only(self):
        self.route['selected_packages'] = [package(TECH)]
        _, trace = self.run_t7()
        self.assertEqual(self.reads, self.controls+[app.TECHNICAL_PATH])
        self.assertEqual(trace['locally_retrieved_package_ids'], [TECH])
        self.assertEqual(trace['locally_retrieved_module_ids'], ['HUB-DOM-TECHNICAL'])
        self.assertIn(app.TECHNICAL_PATH.read_text(encoding='utf-8'), self.payloads[-1]['instructions'])
        self.assertNotIn('HUB-DOM-CONCEPT-DEVELOPMENT', self.payloads[-1]['instructions'])
        for path in self.controls[1:4]:
            self.assertNotIn(path.read_text(encoding='utf-8'), self.payloads[-1]['instructions'])

    def test_concept_core_and_each_leaf_selective(self):
        for target in (None, app.CREATIVE_PATH, app.BRAINSTORM_PATH, app.DEBATE_PATH):
            with self.subTest(target=target):
                self.payloads.clear()
                self.reads.clear()
                self.route['selected_packages'] = [package(CONCEPT)]
                module = target.name.split('_v')[0] if target else None
                self.local['selected_leaves'] = [leaf(module)] if target else []
                _, trace = self.run_t7()
                self.assertEqual(self.reads, self.controls+[app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH]+([target] if target else []))
                root, local, final = self.payloads
                self.assertEqual(local['text']['format']['schema'], app.LEAF_SCHEMA)
                self.assertTrue(local['text']['format']['strict'])
                self.assertIn('[T7 CONCEPT LOCAL BINDING AVAILABILITY]', local['instructions'])
                self.assertIn('expected not-yet-retrieved state is not an unresolved blocker', local['instructions'])
                for path in (app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH):
                    body = path.read_text(encoding='utf-8')
                    self.assertIn(body, local['instructions'])
                    self.assertIn(body, final['instructions'])
                    self.assertNotIn(body, root['instructions'])
                for path in (app.CREATIVE_PATH, app.BRAINSTORM_PATH, app.DEBATE_PATH):
                    body = path.read_text(encoding='utf-8')
                    self.assertNotIn(body, local['instructions'])
                    self.assertEqual(body in final['instructions'], path == target)
                self.assertEqual(trace['concept_selected_leaf_ids'], [module] if module else [])
                self.assertEqual(trace['unresolved_blockers'], [])
                if target == app.DEBATE_PATH:
                    self.assertIn('resolution: UNRESOLVED', final['instructions'])
                    self.assertIn('LOCAL_RUNTIME_FILE is the current T7 binding authority', final['instructions'])

    def test_coexistence_and_deterministic_body_order(self):
        self.route['selected_packages'] = [package(CONCEPT), package(TECH)]
        self.local['selected_leaves'] = [leaf('HUB-CAP-DEBATE'), leaf('HUB-DOM-CREATIVE'), leaf('HUB-CAP-BRAINSTORM')]
        _, trace = self.run_t7()
        final = self.payloads[-1]['instructions']
        paths = (app.HUB_CI_PATH, app.TECHNICAL_PATH, app.CONCEPT_CORE_PATH,
                 app.CONCEPT_CATALOG_PATH, app.CREATIVE_PATH, app.BRAINSTORM_PATH, app.DEBATE_PATH)
        positions = [final.index(p.read_text(encoding='utf-8')) for p in paths]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(trace['locally_retrieved_module_ids'][-3:], ['HUB-DOM-CREATIVE', 'HUB-CAP-BRAINSTORM', 'HUB-CAP-DEBATE'])

    def test_unsupported_packages_block_independently_without_reads(self):
        unsupported = ['HUB-PKG-AUTHORING', 'HUB-PKG-AIS', 'HUB-PKG-IMAGET']
        self.route['selected_packages'] = [package(p) for p in unsupported+[TECH, CONCEPT]]
        self.local['selected_leaves'] = [leaf('HUB-CAP-DEBATE')]
        _, trace = self.run_t7()
        self.assertEqual(self.reads, self.controls+[app.TECHNICAL_PATH, app.CONCEPT_CORE_PATH,
                         app.CONCEPT_CATALOG_PATH, app.DEBATE_PATH])
        self.assertEqual(trace['locally_retrieved_package_ids'], [TECH, CONCEPT])
        self.assertEqual(len(trace['unresolved_blockers']), 3)
        for package_id in unsupported:
            self.assertTrue(any(package_id in b for b in trace['unresolved_blockers']))
            self.assertIn(package_id, self.payloads[-1]['instructions'])
        self.assertIn('must not be emulated', self.payloads[-1]['instructions'])

    def test_root_hallucination_mismatch_and_duplicate(self):
        invalid = [dict(package(TECH), package_id='HUB-PKG-FAKE'),
                   dict(package(TECH), entrypoint_module_id='HUB-DOM-FAKE'),
                   dict(package(TECH), runtime_role='CAPABILITY')]
        for selection in invalid:
            with self.subTest(selection=selection):
                self.reads.clear()
                self.route['selected_packages'] = [selection]
                _, trace = self.run_t7()
                self.assertEqual(self.reads, self.controls)
                self.assertEqual(trace['locally_retrieved_package_ids'], [])
                self.assertTrue(trace['unresolved_blockers'])
        self.route['selected_packages'] = [package(TECH), package(TECH)]
        _, trace = self.run_t7()
        self.assertTrue(any('duplicate' in b for b in trace['unresolved_blockers']))

    def test_leaf_hallucination_or_mismatch_blocks_only_leaf(self):
        for selection in (leaf('HUB-CAP-UNKNOWN'), dict(leaf('HUB-CAP-DEBATE'), runtime_role='DOMAIN_CONTROL')):
            self.reads.clear()
            self.route['selected_packages'] = [package(CONCEPT)]
            self.local['selected_leaves'] = [selection]
            _, trace = self.run_t7()
            self.assertEqual(self.reads, self.controls+[app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH])
            self.assertEqual(trace['locally_retrieved_package_ids'], [CONCEPT])
            self.assertTrue(trace['unresolved_blockers'])

    def test_core_control_and_config_errors_stop_before_api(self):
        for path in self.controls:
            for failure in (FileNotFoundError(), PermissionError(), OSError(), b'\xff'):
                def read(target):
                    if target == path:
                        if isinstance(failure, bytes):
                            return failure
                        raise failure
                    return self.original_read(target)
                with self.subTest(path=path, failure=failure), patch.object(Path, 'read_bytes', read), patch.object(app, 'OpenAI') as client:
                    with self.assertRaisesRegex(ValueError, 'T7:'):
                        app.call_t7(self.config, self.history)
                    client.assert_not_called()
        for bad in ('{', '[]', '{"status":"ACTIVE","status":"INACTIVE"}', '{}'):
            def read(path):
                return bad.encode() if path == app.T7_BINDINGS_PATH else self.original_read(path)
            with self.subTest(bad=bad), patch.object(Path, 'read_bytes', read), patch.object(app, 'OpenAI') as client:
                with self.assertRaises(ValueError):
                    app.call_t7(self.config, self.history)
                client.assert_not_called()

    def test_selected_artifact_errors_block_portion_without_fallback(self):
        self.route['selected_packages'] = [package(TECH), package(CONCEPT)]
        self.local['selected_leaves'] = [leaf('HUB-CAP-DEBATE')]
        for path in (app.TECHNICAL_PATH, app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH, app.DEBATE_PATH):
            for failure in (FileNotFoundError(), PermissionError(), OSError(), b'changed', b'\xff'):
                reads = []
                def read(target):
                    reads.append(target)
                    if target == path:
                        if isinstance(failure, bytes):
                            return failure
                        raise failure
                    return self.original_read(target)
                with self.subTest(path=path, failure=failure), patch.object(Path, 'read_bytes', read), patch.object(app, 'OpenAI', self.client):
                    _, trace = app.call_t7(self.config, self.history)
                    self.assertTrue(trace['unresolved_blockers'])
                    self.assertNotIn(path.name.split('_v')[0], trace['locally_retrieved_module_ids'])
                    self.assertTrue(set(reads).issubset(set(self.controls+[app.TECHNICAL_PATH, app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH, app.DEBATE_PATH])))
                    if path == app.TECHNICAL_PATH:
                        self.assertIn(CONCEPT, trace['locally_retrieved_package_ids'])
                    else:
                        self.assertIn(TECH, trace['locally_retrieved_package_ids'])

    def test_path_escape_never_reads_target_and_utf8_after_hash(self):
        for bad_path in ('../upstream/body.md', 'runtime/../upstream/body.md',
                         'upstream/body.md', 'C:/outside/body.md', 'runtime/../../body.md'):
            manifest = copy.deepcopy(self.manifest)
            manifest['packages'][TECH]['entrypoint']['path'] = bad_path
            reads = []
            def read(path):
                reads.append(path)
                return json.dumps(manifest).encode() if path == app.T7_BINDINGS_PATH else self.original_read(path)
            self.route['selected_packages'] = [package(TECH)]
            with self.subTest(path=bad_path), patch.object(Path, 'read_bytes', read), patch.object(app, 'OpenAI', self.client):
                _, trace = app.call_t7(self.config, self.history)
                self.assertEqual(reads, self.controls)
                self.assertTrue(trace['unresolved_blockers'])
        artifact = copy.deepcopy(self.manifest['packages'][TECH]['entrypoint'])
        artifact['sha256'] = hashlib.sha256(b'\xff').hexdigest()
        with patch.object(Path, 'read_bytes', return_value=b'\xff'), self.assertRaises(ValueError):
            app.t7_retrieve(artifact)

    def test_malformed_structured_result_stops_without_retry(self):
        for bad in ([], {}, dict(self.route, selected_packages=['bad']), dict(self.route, unresolved_blockers=[1])):
            self.route = bad
            self.payloads.clear()
            with patch.object(app, 'OpenAI', self.client), self.assertRaises(ValueError):
                app.call_t7(self.config, self.history)
            self.assertEqual(len(self.payloads), 1)
        self.route = dict(task_scope='', selected_packages=[package(CONCEPT)], unresolved_blockers=[])
        self.local = {'selected_leaves': 'bad', 'unresolved_blockers': []}
        self.payloads.clear()
        with patch.object(app, 'OpenAI', self.client), self.assertRaises(ValueError):
            app.call_t7(self.config, self.history)
        self.assertEqual(len(self.payloads), 2)

    def test_ui_t7_history_mode_t3_isolation_and_total_failure(self):
        with self.ui_context(), patch('openai.OpenAI', self.client):
            ui = AppTest.from_file('app.py').run()
            ui.radio[0].set_value(app.MODES[7]).run()
            ui.text_area[0].set_value('T7 first')
            ui.button[0].click().run()
            self.assertFalse(ui.exception)
            self.assertFalse(ui.error)
            self.assertEqual(ui.chat_message[-1].caption[0].value, app.MODES[7])
            history = list(ui.session_state.messages)
            labels = dict(ui.session_state.response_modes)
            routing = test_t3.T3Tests()
            routing.setUp()
            with patch('openai.OpenAI', routing.client):
                ui.radio[0].set_value(app.MODES[3]).run()
                ui.text_area[0].set_value('T3 isolated')
                ui.button[0].click().run()
                self.assertEqual(routing.payloads[-1]['input'], [{'role': 'user', 'content': 'T3 isolated'}])
            self.assertEqual(ui.session_state.messages, history)
            routes = list(ui.session_state.route_records)
            ui.radio[0].set_value(app.MODES[7]).run()
            with patch.object(Path, 'read_bytes', side_effect=FileNotFoundError()), patch('openai.OpenAI') as client:
                ui.text_area[0].set_value('keep prompt')
                ui.button[0].click().run()
                client.assert_not_called()
            self.assertFalse(ui.exception)
            self.assertTrue(ui.error)
            self.assertEqual(ui.session_state.messages, history)
            self.assertEqual(ui.session_state.response_modes, labels)
            self.assertEqual(ui.session_state.route_records, routes)
            self.assertEqual(ui.text_area[0].value, 'keep prompt')
            ui.button[0].click().run()
            self.assertFalse(ui.error)
            for payload in self.payloads[-2:]:
                self.assertEqual(payload['input'], history+[{'role': 'user', 'content': 'keep prompt'}])
            self.assertEqual(ui.session_state.route_records, routes)

    def test_binding_inventory_errors_stop_before_api(self):
        mutations = []
        for key, value in (("status", "INACTIVE"), ("binding_version", "0.2"),
                           ("retrieval_authority", "LIBRARY_MODULE")):
            manifest = copy.deepcopy(self.manifest)
            manifest[key] = value
            mutations.append(manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest['packages']['HUB-PKG-AIS'] = manifest['packages'][TECH]
        mutations.append(manifest)
        for key, value in (("module_id", "FAKE"), ("runtime_role", "CAPABILITY"),
                           ("version", "9"), ("sha256", "bad")):
            manifest = copy.deepcopy(self.manifest)
            manifest['packages'][TECH]['entrypoint'][key] = value
            mutations.append(manifest)
        for manifest in mutations:
            def read(path):
                return json.dumps(manifest).encode() if path == app.T7_BINDINGS_PATH else self.original_read(path)
            with self.subTest(manifest=manifest), patch.object(Path, 'read_bytes', read), patch.object(app, 'OpenAI') as client:
                with self.assertRaises(ValueError):
                    app.call_t7(self.config, self.history)
                client.assert_not_called()

    def test_root_and_leaf_catalog_identity_changes_block_without_guess(self):
        self.route['selected_packages'] = [package(TECH), package(CONCEPT)]
        def read(path):
            data = self.original_read(path)
            if path == app.HUB_CATALOG_PATH:
                return data.replace(b"version: '1.0'", b"version: '9.0'", 1)
            return data
        with patch.object(Path, 'read_bytes', read), patch.object(app, 'OpenAI', self.client):
            _, trace = app.call_t7(self.config, self.history)
        self.assertNotIn(TECH, trace['locally_retrieved_package_ids'])
        self.assertIn(CONCEPT, trace['locally_retrieved_package_ids'])
        self.assertTrue(trace['unresolved_blockers'])
        self.route['selected_packages'] = [package(CONCEPT)]
        self.local['selected_leaves'] = [leaf('HUB-CAP-DEBATE')]
        local_bytes = self.original_read(app.CONCEPT_CATALOG_PATH).replace(
            b"- module_id: HUB-CAP-DEBATE", b"- module_id: HUB-CAP-NOT-DEBATE")
        manifest = copy.deepcopy(self.manifest)
        manifest['packages'][CONCEPT]['local_catalog']['sha256'] = hashlib.sha256(local_bytes).hexdigest()
        reads = []
        def read(path):
            reads.append(path)
            if path == app.CONCEPT_CATALOG_PATH:
                return local_bytes
            if path == app.T7_BINDINGS_PATH:
                return json.dumps(manifest).encode()
            return self.original_read(path)
        with patch.object(Path, 'read_bytes', read), patch.object(app, 'OpenAI', self.client):
            _, trace = app.call_t7(self.config, self.history)
        self.assertNotIn(app.DEBATE_PATH, reads)
        self.assertTrue(trace['unresolved_blockers'])

    def test_model_blockers_and_multiple_leaf_scopes_preserved(self):
        self.route['selected_packages'] = [package(CONCEPT)]
        self.route['unresolved_blockers'] = ['root scoped unresolved input']
        self.local['unresolved_blockers'] = ['leaf scoped ambiguity']
        self.local['selected_leaves'] = [leaf('HUB-DOM-CREATIVE'),
            dict(leaf('HUB-DOM-CREATIVE'), application_scope='second independent span')]
        _, trace = self.run_t7()
        self.assertEqual(trace['unresolved_blockers'], ['root scoped unresolved input', 'leaf scoped ambiguity'])
        self.assertEqual(self.reads.count(app.CREATIVE_PATH), 1)
        self.assertIn('second independent span', self.payloads[-1]['instructions'])
        self.assertIn('root scoped unresolved input', self.payloads[-1]['instructions'])
        self.assertIn('leaf scoped ambiguity', self.payloads[-1]['instructions'])

    def test_upstream_unchanged_outside_authorized_m2_promotion(self):
        baseline = 'a1163c3d54d4934b7870cb634e4d04bb22d2b21d'
        prefix = 'upstream/Central Hub/'
        changed = {
            prefix + p for p in (
                'HUB_ROUTER_v1.1.yaml', 'AUTHORING_PROMOTION.md', 'README.md',
                'RUNTIME_EVIDENCE_CHANGELOG.md', 'tests/test_authoring_candidate.py',
                'tests/test_authoring_m1.py', 'tests/test_authoring_m2.py',
                'tests/test_authoring_m4.py', 'tests/test_authoring_isolation.py')}
        archived = {prefix + p for p in ('HUB_ARCHITECTURE_v1.8.md',
                    'HUB_PACKAGE_CATALOG_v1.8.yaml', 'library_modules/HUB-CAP-AUTHORING_v0.6.md')}
        added = {prefix + p for p in ('HUB_ARCHITECTURE_v1.9.md', 'HUB_PACKAGE_CATALOG_v1.9.yaml',
                                     'library_modules/HUB-CAP-AUTHORING_v0.7.md')}
        archive_prefix = prefix + 'Source_archive/Authoring 0.7 M2 2026-11-05/'
        archive_files = {archive_prefix + p for p in ('HUB_ARCHITECTURE_v1.8.md',
            'HUB_PACKAGE_CATALOG_v1.8.yaml', 'library_modules/HUB-CAP-AUTHORING_v0.6.md',
            'HUB_ROUTER_v1.1.yaml', 'AUTHORING_PROMOTION.md', 'ARCHIVE_RECEIPT.json')}
        redacted_reports = {prefix + p for p in (
            'MIGRATION_REPORT.md',
            'Source_archive/AIS_PROMOTION_ARCHIVE_RECEIPT_2026-10-21.json',
            'tests/test_ais_research_core.py',
            'tests/test_hub_router_candidate.py',
            'Source_archive/AIS research-core promotion 2026-10-21/candidates/ais_research_core/IMPLEMENTATION_REPORT.md',
            'candidates/authoring_v0/AUTHORING_TEST_CASES.md',
            'candidates/fth_afm015_workspace_pilot/PHASE_4_ADMISSION_DRY_RUN.md',
            'candidates/fth_afm015_workspace_pilot/README.md',
            'tests/SHOPPING_M2_1_REGRESSIONS.md',
            'tool_pipelines/AIS/AIS_PROMOTION_REPORT.md',
        )}
        paths = subprocess.check_output(['git', 'ls-tree', '-rz', '--name-only', baseline, '--', 'upstream']).decode('utf-8').rstrip('\0').split('\0')
        self.assertEqual(len(paths), 208)
        for path in paths:
            with self.subTest(path=path):
                committed = subprocess.check_output(['git', 'cat-file', 'blob', baseline+':'+path])
                relocated = Path('legacy') / path
                if path in archived:
                    self.assertFalse(relocated.exists())
                    self.assertEqual((Path('legacy') / (archive_prefix + path[len(prefix):])).read_bytes(), committed)
                elif path not in changed | redacted_reports:
                    self.assertEqual(relocated.read_bytes(), committed)
        actual = {p.relative_to('legacy').as_posix() for p in Path('legacy/upstream').rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts}
        self.assertEqual(actual - set(paths), added | archive_files)


if __name__ == '__main__':
    unittest.main()
