import json
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

import app
import test_app
import test_t3


class T5Tests(unittest.TestCase):
    setUp = test_app.Stage2Tests.setUp
    client = test_app.Stage2Tests.client
    ui_context = test_app.Stage2Tests.ui_context

    def paths(self):
        return (app.HUB_CI_PATH, app.CONCEPT_CORE_PATH, app.CONCEPT_CATALOG_PATH,
                app.CREATIVE_PATH, app.BRAINSTORM_PATH, app.DEBATE_PATH)

    def test_exact_active_leaf_copies(self):
        for path, version in ((app.CREATIVE_PATH, b'1.1'),
                              (app.BRAINSTORM_PATH, b'1.1'), (app.DEBATE_PATH, b'1.0')):
            body = path.read_bytes()
            self.assertEqual(body, (Path('legacy/upstream/Central Hub/library_modules') / path.name).read_bytes())
            self.assertIn(b'Status: ACTIVE', body)
            self.assertIn(b'Version: ' + version, body)

    def test_payload_byte_order_exact_reads_no_cache_or_other_bodies(self):
        paths = self.paths()
        bodies = [path.read_bytes() for path in paths]
        reads = []

        def read_bytes(path):
            reads.append(path)
            self.assertIn(path, paths)
            return bodies[paths.index(path)]

        with patch.object(Path, 'read_bytes', read_bytes), patch.object(app, 'OpenAI', self.client):
            history = []
            for turn in range(2):
                # Python passes even malformed/literal controls through unchanged.
                messages = history + [{'role': 'user', 'content': f'{turn}: `/DEBATE x #` /CREATIVE x /BRAINSTORM y #'}]
                answer = app.call_model(self.config, messages, app.MODES[5])
                self.assertEqual(self.payloads[-1], {
                    'model': self.config['model'], 'input': messages, 'store': False,
                    'instructions': (bodies[0] + app.T5_CALIBRATION_ADAPTER.encode('utf-8')
                                     + b''.join(bodies[1:])).decode('utf-8'),
                })
                history = messages + [{'role': 'assistant', 'content': answer}]
                bodies = [b'\xef\xbb\xbfupdated\r\n' + body for body in bodies]
        self.assertEqual(reads, list(paths) * 2)

    def test_all_file_failures_before_api_and_preserve_ui_state(self):
        original = Path.read_bytes
        with self.ui_context(), patch('openai.OpenAI', self.client):
            ui = AppTest.from_file('app.py').run()
            ui.radio[0].set_value(app.MODES[0]).run()
            ui.text_area[0].set_value('T0 trước')
            ui.button[0].click().run()
            history = list(ui.session_state.messages)
            labels = dict(ui.session_state.response_modes)
            routes = [{'prompt': 'trước', 'record': {'selected_packages': []}}]
            ui.session_state.route_records = routes
            ui.radio[0].set_value(app.MODES[5]).run()
            for target in self.paths():
                for failure in (FileNotFoundError(), PermissionError(), OSError(), b'\xff'):
                    def read_bytes(path):
                        if path == target:
                            if isinstance(failure, bytes):
                                return failure
                            raise failure
                        return original(path)
                    with self.subTest(target=target.name, failure=failure), \
                         patch.object(Path, 'read_bytes', read_bytes), \
                         patch('openai.OpenAI') as client:
                        ui.text_area[0].set_value('Giữ prompt')
                        ui.button[0].click().run()
                        client.assert_not_called()
                        self.assertFalse(ui.exception)
                        self.assertIn('T5: Không đọc được ' + target.name, ui.error[0].value)
                        self.assertIn('không chuyển sang T4/T2/T1/T0', ui.error[0].value)
                        self.assertEqual(ui.session_state.messages, history)
                        self.assertEqual(ui.session_state.response_modes, labels)
                        self.assertEqual(ui.session_state.route_records, routes)
                        self.assertEqual(ui.text_area[0].value, 'Giữ prompt')

    def test_t0_to_t4_never_read_new_leaves(self):
        original = Path.read_bytes
        reads = []

        def read_bytes(path):
            reads.append(path)
            self.assertNotIn(path, self.paths()[3:])
            return original(path)

        with patch.object(Path, 'read_bytes', read_bytes), patch.object(app, 'OpenAI', self.client):
            for index in (0, 1, 2, 4):
                app.call_model(self.config, [], app.MODES[index])
        routing = test_t3.T3Tests()
        routing.setUp()
        with patch.object(Path, 'read_bytes', read_bytes), patch.object(app, 'OpenAI', routing.client):
            self.assertEqual(app.inspect_route(self.config, 'T3'), routing.record)
            self.assertEqual(routing.payloads[-1]['text']['format']['type'], 'json_schema')

    def test_shared_history_visible_labels_and_t3_isolation(self):
        with self.ui_context(), patch('openai.OpenAI', self.client):
            ui = AppTest.from_file('app.py').run()
            modes = [app.MODES[i] for i in (0, 5, 1, 5, 2, 5, 4, 5)]
            self.assertIn('T5 - Concept Scoped Leaves', ui.radio[0].options)
            for index, mode in enumerate(modes):
                ui.radio[0].set_value(mode).run()
                ui.text_area[0].set_value(f'Lượt {index}')
                ui.button[0].click().run()
                self.assertFalse(ui.exception)
                self.assertFalse(ui.error)
                self.assertEqual(self.payloads[-1]['input'], ui.session_state.messages[:-1])
            self.assertEqual([c.caption[0].value for c in ui.chat_message if c.name == 'assistant'], modes)
            history = list(ui.session_state.messages)
            routing = test_t3.T3Tests()
            routing.setUp()
            with patch('openai.OpenAI', routing.client):
                ui.radio[0].set_value(app.MODES[3]).run()
                ui.text_area[0].set_value('T3 riêng')
                ui.button[0].click().run()
                self.assertEqual(routing.payloads[-1]['input'], [{'role': 'user', 'content': 'T3 riêng'}])
                self.assertEqual(json.loads(ui.json[-1].value), routing.record)
            self.assertEqual(ui.session_state.messages, history)
            routes = list(ui.session_state.route_records)
            ui.radio[0].set_value(app.MODES[5]).run()
            ui.text_area[0].set_value('T5 tiếp')
            ui.button[0].click().run()
            self.assertEqual(self.payloads[-1]['input'], history + [{'role': 'user', 'content': 'T5 tiếp'}])
            self.assertEqual(ui.session_state.route_records, routes)


if __name__ == '__main__':
    unittest.main()
