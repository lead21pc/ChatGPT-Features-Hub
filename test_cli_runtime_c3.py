import unittest
from unittest.mock import patch

import cli_runtime_c3


class CliRuntimeC3Tests(unittest.TestCase):
    @patch("cli_runtime_c3.cli_model.call_codex_cli")
    @patch("cli_runtime_c3.cli_root.select_root")
    def test_technical_end_to_end_shape(self, root, call):
        root.return_value = {
            "task_scope": "diagnose stutter",
            "selected_packages": [{
                "package_id": "HUB-PKG-TECHNICAL",
                "entrypoint_module_id": "HUB-DOM-TECHNICAL",
                "runtime_role": "REASONING_PROFILE",
                "application_scope": "diagnose causes",
                "reason": "technical diagnosis",
                "version": "1.0",
                "declared_source_path": "",
            }],
            "unresolved_blockers": [],
        }
        call.return_value = "final"
        answer, trace = cli_runtime_c3.call_c3(
            {"model": "gpt-6.1-sol"},
            [{"role": "user", "content": "Máy tính khựng."}],
        )
        self.assertEqual(answer, "final")
        self.assertEqual(trace["root_selected_package_ids"], ["HUB-PKG-TECHNICAL"])
        self.assertEqual(trace["retrieved_module_ids"], ["HUB-DOM-TECHNICAL"])
        self.assertTrue(trace["retrieval_verified"])
        self.assertIn("HUB-DOM-TECHNICAL", call.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
