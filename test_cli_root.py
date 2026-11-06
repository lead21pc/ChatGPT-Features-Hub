import unittest
from unittest.mock import patch

import cli_root


class CliRootTests(unittest.TestCase):
    @patch("cli_root.cli_model.call_codex_cli")
    def test_validates_technical_route(self, call):
        call.return_value = """{
          "task_scope": "diagnose intermittent computer stutter",
          "selected_packages": [{
            "package_id": "HUB-PKG-TECHNICAL",
            "entrypoint_module_id": "HUB-DOM-TECHNICAL",
            "runtime_role": "REASONING_PROFILE",
            "application_scope": "diagnose competing mechanisms",
            "reason": "mechanism diagnosis is requested",
            "version": "1.0",
            "declared_source_path": ""
          }],
          "unresolved_blockers": []
        }"""
        route = cli_root.select_root(
            {"model": "gpt-6.1-sol"},
            [{"role": "user", "content": "Máy tính thỉnh thoảng khựng."}],
        )
        self.assertEqual(
            [item["package_id"] for item in route["selected_packages"]],
            ["HUB-PKG-TECHNICAL"],
        )
        self.assertEqual(call.call_args.kwargs["output_schema"]["type"], "object")


if __name__ == "__main__":
    unittest.main()
