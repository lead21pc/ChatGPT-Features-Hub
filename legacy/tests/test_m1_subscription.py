import json
import unittest
from unittest.mock import patch

import m1
import t8
import t9
import subscription_backend
from test_t9 import root_package


class M1SubscriptionRootTests(unittest.TestCase):
    def test_subscription_root_uses_same_control_stack_and_validator(self):
        config = {"model": "gpt-6.1-sol"}
        messages = [{"role": "user", "content": "Current scoped request"}]
        selected = root_package(t8.TECHNICAL)
        raw = json.dumps({
            "task_scope": "current",
            "selected_packages": [selected],
            "unresolved_blockers": [],
        })
        with patch.object(subscription_backend, "call_subscription", return_value=raw) as call:
            route, trace = m1.call_root_subscription(config, messages)

        self.assertEqual(route["selected_packages"][0]["package_id"], t8.TECHNICAL)
        self.assertEqual(trace["root_selected_package_ids"], [t8.TECHNICAL])
        args, kwargs = call.call_args
        self.assertIn(m1.NOTE, args[0])
        self.assertIn(m1.ROOT_TASK, args[0])
        self.assertEqual(args[1], messages[0]["content"])
        self.assertEqual(kwargs["model"], config["model"])
        self.assertIs(kwargs["output_schema"], t9.ROUTE_SCHEMA)

    def test_subscription_root_rejects_history_for_bounded_proof(self):
        with self.assertRaisesRegex(ValueError, "exactly one current user message"):
            m1.call_root_subscription(
                {"model": "gpt-6.1-sol"},
                [{"role": "assistant", "content": "old"}, {"role": "user", "content": "new"}],
            )


if __name__ == "__main__":
    unittest.main()
