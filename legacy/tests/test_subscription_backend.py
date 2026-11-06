import json
import unittest
from unittest.mock import MagicMock, patch

import subscription_backend


class SubscriptionBackendTests(unittest.TestCase):
    def test_validation_rejects_empty_user(self):
        with self.assertRaises(ValueError):
            subscription_backend.call_subscription("", "   ")

    @patch("subscription_backend.subprocess.Popen")
    def test_transport_has_no_hub_semantics(self, popen):
        proc = MagicMock()
        popen.return_value = proc
        proc.poll.return_value = None
        proc.stdin = MagicMock()

        messages = iter([
            {"id": 1, "result": {"codexHome": "x", "platformFamily": "windows",
                                  "platformOs": "windows", "userAgent": "codex"}},
            {"id": 2, "result": {"thread": {"id": "thread-1"}}},
            {"id": 3, "result": {"turn": {"id": "turn-1"}}},
            {"method": "item/completed", "params": {
                "item": {"type": "agentMessage", "text": "ok"}}},
            {"method": "turn/completed", "params": {
                "threadId": "thread-1", "turn": {"status": "completed"}}},
        ])
        with patch("subscription_backend._read_json", side_effect=lambda *a: next(messages)):
            result = subscription_backend.call_subscription(
                "caller supplied instructions", "caller supplied user text",
                model="gpt-6.1-sol", output_schema={"type": "object"},
            )

        self.assertEqual(result, "ok")
        sent = "".join(call.args[0] for call in proc.stdin.write.call_args_list)
        self.assertIn('"ephemeral": true', sent)
        self.assertIn('"baseInstructions": "caller supplied instructions"', sent)
        self.assertIn('"outputSchema": {"type": "object"}', sent)
        for forbidden in ("HUB-PKG-TECHNICAL", "HUB-PKG-CONCEPT-DEVELOPMENT",
                          "HUB-PKG-AIS", "ROOT_PACKAGE_SELECTION"):
            self.assertNotIn(forbidden, sent)


if __name__ == "__main__":
    unittest.main()
