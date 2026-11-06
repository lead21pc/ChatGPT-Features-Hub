"""Minimal Codex CLI subscription transport proof.

C1 only: Python sends one prompt to Codex CLI and returns the final text.
This module does not perform Hub routing or replace M1 yet.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path


def _prompt(instructions: str, messages: list[dict[str, str]]) -> str:
    parts = []
    if instructions:
        parts.append("[INSTRUCTIONS]\n" + instructions)
    for message in messages:
        role = message.get("role")
        content = message.get("content")
        if not isinstance(role, str) or not isinstance(content, str):
            raise ValueError("C1 CLI: message phải có role/content dạng chuỗi.")
        parts.append(f"[{role.upper()}]\n{content}")
    if not parts:
        raise ValueError("C1 CLI: prompt rỗng.")
    return "\n\n".join(parts)


def call_codex_cli(
    instructions: str,
    messages: list[dict[str, str]],
    *,
    model: str = "gpt-6.1-sol",
    timeout: float = 120.0,
) -> str:
    """Call Codex CLI through the logged-in ChatGPT subscription and return final text."""
    prompt = _prompt(instructions, messages)
    env = os.environ.copy()
    env.pop("OPENAI_API_KEY", None)
    env.pop("CODEX_API_KEY", None)

    with tempfile.TemporaryDirectory(prefix="central-hub-cli-") as temp_dir:
        root = Path(temp_dir)
        output_path = root / "last_message.txt"
        command = [
            "codex.cmd", "exec",
            "--skip-git-repo-check",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "-s", "read-only",
            "-C", str(root),
            "-m", model,
            "-o", str(output_path),
            "-",
        ]
        try:
            result = subprocess.run(
                command,
                input=prompt,
                text=True,
                encoding="utf-8",
                errors="strict",
                capture_output=True,
                timeout=timeout,
                env=env,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"C1 CLI: không gọi được Codex CLI: {exc}") from None

        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            raise RuntimeError(f"C1 CLI: Codex CLI thất bại ({result.returncode}): {detail}")
        try:
            text = output_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise RuntimeError(f"C1 CLI: không đọc được final output: {exc}") from None
        if not text:
            raise RuntimeError("C1 CLI: Codex CLI không trả final text.")
        return text
