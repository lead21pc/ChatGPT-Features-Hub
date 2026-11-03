import json
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

import app
import test_app
import test_t3


class T4Tests(unittest.TestCase):
    setUp = test_app.Stage2Tests.setUp
    client = test_app.Stage2Tests.client
    ui_context = test_app.Stage2Tests.ui_context

    def test_exact_active_copies_and_runtime_inventory(self):
        paths = (app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH)
        self.assertEqual(set(paths[0].parent.iterdir()),
                         set(paths) | {app.CREATIVE_PATH, app.BRAINSTORM_PATH, app.DEBATE_PATH})
        for path in paths:
            source = Path('upstream/Central Hub/library_modules') / path.name
            self.assertEqual(path.read_bytes(), source.read_bytes())
        self.assertIn(b'Status: ACTIVE', paths[0].read_bytes())
        self.assertIn(b'Version: 1.1', paths[0].read_bytes())
        self.assertIn(b'status: ACTIVE', paths[1].read_bytes())
        self.assertIn(b"version: '1.1'", paths[1].read_bytes())

    def test_payload_exact_order_reads_each_request_and_no_other_bodies(self):
        paths = (app.HUB_CI_PATH, app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH)
        bodies = [path.read_bytes() for path in paths]
        reads = []

        def read_bytes(path):
            reads.append(path)
            self.assertIn(path, paths)
            return bodies[paths.index(path)]

        with patch.object(Path, 'read_bytes', read_bytes), patch.object(app, 'OpenAI', self.client):
            history = []
            for turn in range(2):
                messages = history + [{'role': 'user', 'content': f'Lượt {turn}'}]
                answer = app.call_model(self.config, messages, app.MODES[4])
                self.assertEqual(self.payloads[-1], {
                    'model': self.config['model'], 'input': messages, 'store': False,
                    'instructions': (bodies[0] + app.T4_BINDING_NOTE.encode('utf-8')
                                     + bodies[1] + bodies[2]).decode('utf-8'),
                })
                history = messages + [{'role': 'assistant', 'content': answer}]
                bodies = [b'\xef\xbb\xbfupdated\r\n' + body for body in bodies]
        self.assertEqual(reads, list(paths) * 2)

    def test_required_file_failures_before_client(self):
        original = Path.read_bytes
        for target in (app.HUB_CI_PATH, app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH):
            for failure in (FileNotFoundError(), PermissionError(), OSError(), b'\xff'):
                def read_bytes(path):
                    if path == target:
                        if isinstance(failure, bytes):
                            return failure
                        raise failure
                    return original(path)
                with self.subTest(target=target.name, failure=failure), \
                     patch.object(Path, 'read_bytes', read_bytes), patch.object(app, 'OpenAI') as client:
                    with self.assertRaisesRegex(ValueError, 'T4:.*' + target.name + '.*không chuyển sang T2/T1/T0'):
                        app.call_model(self.config, [], app.MODES[4])
                    client.assert_not_called()

    def test_old_modes_do_not_read_concept(self):
        original = Path.read_bytes

        def read_bytes(path):
            self.assertNotIn(path, (app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH))
            return original(path)

        with patch.object(Path, 'read_bytes', read_bytes), patch.object(app, 'OpenAI', self.client):
            for mode in app.MODES[:3]:
                app.call_model(self.config, [], mode)
        # T3's existing test restricts all reads to its four controls and checks JSON-only payload.

    def test_ui_shared_history_labels_and_t3_isolation(self):
        with self.ui_context(), patch('openai.OpenAI', self.client):
            ui = AppTest.from_file('app.py').run()
            modes = [app.MODES[i] for i in (0, 4, 1, 4, 2, 4)]
            for index, mode in enumerate(modes):
                ui.radio[0].set_value(mode).run()
                ui.text_area[0].set_value(f'Lượt {index}')
                ui.button[0].click().run()
                self.assertFalse(ui.exception)
                self.assertFalse(ui.error)
                self.assertEqual(self.payloads[-1]['input'], ui.session_state.messages[:-1])
            self.assertEqual([c.caption[0].value for c in ui.chat_message if c.name == 'assistant'], modes)
            history = list(ui.session_state.messages)
            record = {'task_scope': 'Test', 'selected_packages': [], 'unresolved_blockers': []}
            routing = test_t3.T3Tests()
            routing.setUp()
            routing.body['output'][0]['content'][0]['text'] = json.dumps(record)
            with patch('openai.OpenAI', routing.client):
                ui.radio[0].set_value(app.MODES[3]).run()
                ui.text_area[0].set_value('T3 riêng')
                ui.button[0].click().run()
                self.assertEqual(routing.payloads[-1]['input'], [{'role': 'user', 'content': 'T3 riêng'}])
            self.assertEqual(ui.session_state.messages, history)
            self.assertEqual(json.loads(ui.json[-1].value), record)
            routes = list(ui.session_state.route_records)
            ui.radio[0].set_value(app.MODES[4]).run()
            ui.text_area[0].set_value('T4 tiếp')
            ui.button[0].click().run()
            self.assertEqual(self.payloads[-1]['input'], history + [{'role': 'user', 'content': 'T4 tiếp'}])
            self.assertEqual(ui.session_state.route_records, routes)

    def test_ui_read_failures_preserve_history_prompt_and_routes(self):
        original = Path.read_bytes
        with self.ui_context(), patch('openai.OpenAI', self.client):
            ui = AppTest.from_file('app.py').run()
            ui.text_area[0].set_value('T0 trước')
            ui.button[0].click().run()
            history = list(ui.session_state.messages)
            ui.radio[0].set_value(app.MODES[4]).run()
            for target in (app.HUB_CI_PATH, app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH):
                def read_bytes(path):
                    if path == target:
                        raise PermissionError()
                    return original(path)
                calls = len(self.payloads)
                with patch.object(Path, 'read_bytes', read_bytes):
                    ui.text_area[0].set_value('Giữ prompt')
                    ui.button[0].click().run()
                self.assertFalse(ui.exception)
                self.assertIn('T4:', ui.error[0].value)
                self.assertEqual(ui.session_state.messages, history)
                self.assertEqual(ui.session_state.route_records, [])
                self.assertEqual(ui.text_area[0].value, 'Giữ prompt')
                self.assertEqual(len(self.payloads), calls)


if __name__ == '__main__':
    unittest.main()
