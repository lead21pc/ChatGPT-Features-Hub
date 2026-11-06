import unittest
from unittest.mock import patch

import cli_model


class CliModelTests(unittest.TestCase):
    def test_prompt_rejects_invalid_message(self):
        with self.assertRaises(ValueError):
            cli_model._prompt("", [{"role": "user", "content": 3}])

    @patch("cli_model.subprocess.run")
    def test_call_reads_last_message_and_strips_api_env(self, run):
        def fake_run(command, **kwargs):
            output_path = command[command.index("-o") + 1]
            from pathlib import Path
            Path(output_path).write_text("C1 CLI OK\n", encoding="utf-8")
            self.assertNotIn("OPENAI_API_KEY", kwargs["env"])
            self.assertNotIn("CODEX_API_KEY", kwargs["env"])
            self.assertIn("--ephemeral", command)
            self.assertIn("--ignore-user-config", command)
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()

        run.side_effect = fake_run
        self.assertEqual(
            cli_model.call_codex_cli("", [{"role": "user", "content": "test"}]),
            "C1 CLI OK",
        )


if __name__ == "__main__":
    unittest.main()
