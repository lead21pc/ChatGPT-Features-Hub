import json
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

import app
import test_app
import test_t3


class T6Tests(unittest.TestCase):
    setUp = test_app.Stage2Tests.setUp
    client = test_app.Stage2Tests.client
    ui_context = test_app.Stage2Tests.ui_context

    def paths(self):
        return (app.HUB_CI_PATH, app.TECHNICAL_PATH, app.CONCEPT_CORE_PATH,
                app.CONCEPT_CATALOG_PATH, app.CREATIVE_PATH,
                app.BRAINSTORM_PATH, app.DEBATE_PATH)

    def test_exact_payload_order_rereads_and_no_other_sources(self):
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
                messages = history + [{'role': 'user', 'content':
                    f'{turn}: mechanism? `/DEBATE x #` /CREATIVE x /BRAINSTORM y #'}]
                answer = app.call_model(self.config, messages, app.MODES[6])
                self.assertEqual(self.payloads[-1], {
                    'model': self.config['model'], 'input': messages, 'store': False,
                    'instructions': (bodies[0] + app.T6_COMPOSITION_ADAPTER.encode('utf-8')
                                     + b''.join(bodies[1:])).decode('utf-8'),
                })
                history = messages + [{'role': 'assistant', 'content': answer}]
                bodies = [b'\xef\xbb\xbfupdated\r\n' + body for body in bodies]
        self.assertEqual(reads, list(paths) * 2)

    def test_required_file_failures_preserve_history_routes_and_prompt(self):
        original = Path.read_bytes
        with self.ui_context(), patch('openai.OpenAI', self.client):
            ui = AppTest.from_file('app.py').run()
            ui.text_area[0].set_value('prior')
            ui.button[0].click().run()
            history = list(ui.session_state.messages)
            labels = dict(ui.session_state.response_modes)
            routes = [{'prompt': 'prior route', 'record': {'selected_packages': []}}]
            ui.session_state.route_records = routes
            ui.radio[0].set_value(app.MODES[6]).run()
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
                        ui.text_area[0].set_value('keep prompt')
                        ui.button[0].click().run()
                        client.assert_not_called()
                        self.assertFalse(ui.exception)
                        self.assertIn('T6: Không đọc được ' + target.name, ui.error[0].value)
                        self.assertIn('không chuyển sang chế độ khác', ui.error[0].value)
                        self.assertEqual(ui.session_state.messages, history)
                        self.assertEqual(ui.session_state.response_modes, labels)
                        self.assertEqual(ui.session_state.route_records, routes)
                        self.assertEqual(ui.text_area[0].value, 'keep prompt')

    def test_t0_to_t5_read_sets_unchanged(self):
        original = Path.read_bytes
        reads = []

        def read_bytes(path):
            reads.append(path)
            return original(path)

        ci, technical, core, catalog, creative, brainstorm, debate = self.paths()
        expected = {0: [], 1: [ci], 2: [ci, technical], 4: [ci, core, catalog],
                    5: [ci, core, catalog, creative, brainstorm, debate]}
        with patch.object(Path, 'read_bytes', read_bytes), patch.object(app, 'OpenAI', self.client):
            for index, paths in expected.items():
                reads.clear()
                app.call_model(self.config, [], app.MODES[index])
                self.assertEqual(reads, paths)
        routing = test_t3.T3Tests()
        routing.setUp()
        reads.clear()
        with patch.object(Path, 'read_bytes', read_bytes), patch.object(app, 'OpenAI', routing.client):
            self.assertEqual(app.inspect_route(self.config, 'T3'), routing.record)
        self.assertEqual(reads, list(routing.paths))
        self.assertEqual(routing.payloads[-1]['text']['format']['type'], 'json_schema')

    def test_shared_history_labels_and_t3_round_trip(self):
        with self.ui_context(), patch('openai.OpenAI', self.client):
            ui = AppTest.from_file('app.py').run()
            self.assertIn('T6 - Concept + Technical Composition', ui.radio[0].options)
            modes = [app.MODES[i] for i in (0, 6, 1, 6, 2, 6, 4, 6, 5, 6)]
            for index, mode in enumerate(modes):
                ui.radio[0].set_value(mode).run()
                ui.text_area[0].set_value(f'turn {index}')
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
                ui.text_area[0].set_value('isolated route')
                ui.button[0].click().run()
                self.assertEqual(routing.payloads[-1]['input'],
                                 [{'role': 'user', 'content': 'isolated route'}])
                self.assertEqual(json.loads(ui.json[-1].value), routing.record)
            self.assertEqual(ui.session_state.messages, history)
            routes = list(ui.session_state.route_records)
            ui.radio[0].set_value(app.MODES[6]).run()
            ui.text_area[0].set_value('resume')
            ui.button[0].click().run()
            self.assertFalse(ui.exception)
            self.assertFalse(ui.error)
            self.assertEqual(self.payloads[-1]['input'], history + [{'role': 'user', 'content': 'resume'}])
            self.assertEqual(ui.session_state.route_records, routes)


if __name__ == '__main__':
    unittest.main()
