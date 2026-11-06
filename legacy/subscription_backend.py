"""Stateless Codex app-server subscription transport experiment.

Transport only: no Central Hub routing, package, or semantic decisions live here.
Each call starts a fresh ephemeral thread in an empty temporary workspace.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path


def _request(proc, request_id, method, params):
    message = {"id": request_id, "method": method, "params": params}
    proc.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
    proc.stdin.flush()


def _notify(proc, method, params=None):
    message = {"method": method}
    if params is not None:
        message["params"] = params
    proc.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
    proc.stdin.flush()


def _read_json(proc, deadline):
    while time.monotonic() < deadline:
        line = proc.stdout.readline()
        if not line:
            if proc.poll() is not None:
                detail = proc.stderr.read().strip()
                raise RuntimeError(
                    f"Subscription backend: app-server exited ({proc.returncode}): {detail}"
                )
            continue
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    raise TimeoutError("Subscription backend: timed out waiting for app-server.")


def _wait_response(proc, request_id, deadline):
    while True:
        message = _read_json(proc, deadline)
        if message.get("id") == request_id:
            if "error" in message:
                raise RuntimeError(
                    "Subscription backend: app-server request failed: "
                    + json.dumps(message["error"], ensure_ascii=False)
                )
            return message.get("result")


def call_subscription(
    instructions: str,
    user_text: str,
    *,
    model: str = "gpt-6.1-sol",
    output_schema: dict | None = None,
    timeout: float = 120.0,
) -> str:
    """Return one final assistant response from a fresh subscription-backed thread."""
    if not isinstance(instructions, str) or not isinstance(user_text, str):
        raise ValueError("Subscription backend: instructions/user_text must be strings.")
    if not user_text.strip():
        raise ValueError("Subscription backend: empty user input.")

    env = os.environ.copy()
    env.pop("OPENAI_API_KEY", None)
    env.pop("CODEX_API_KEY", None)

    with tempfile.TemporaryDirectory(
        prefix="central-hub-app-server-", ignore_cleanup_errors=True
    ) as temp_dir:
        command = [
            "codex.cmd", "app-server", "--stdio",
            "-c", 'analytics.enabled=false',
        ]
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="strict",
            env=env,
            cwd=str(Path(temp_dir).parent),
            bufsize=1,
        )
        deadline = time.monotonic() + timeout
        try:
            _request(proc, 1, "initialize", {
                "clientInfo": {
                    "name": "central-hub-local",
                    "version": "subscription-backend-proof",
                },
                "capabilities": {"experimentalApi": True},
            })
            _wait_response(proc, 1, deadline)
            _notify(proc, "initialized", {})

            _request(proc, 2, "thread/start", {
                "model": model,
                "cwd": str(Path(temp_dir).resolve()),
                "sandbox": "read-only",
                "approvalPolicy": "never",
                "ephemeral": True,
                "baseInstructions": instructions,
                "dynamicTools": [],
                "environments": [],
                "runtimeWorkspaceRoots": [],
                "allowProviderModelFallback": False,
            })
            thread_result = _wait_response(proc, 2, deadline)
            thread_id = thread_result["thread"]["id"]

            turn_params = {
                "threadId": thread_id,
                "input": [{"type": "text", "text": user_text}],
            }
            if output_schema is not None:
                turn_params["outputSchema"] = output_schema
            _request(proc, 3, "turn/start", turn_params)
            _wait_response(proc, 3, deadline)

            final_parts = []
            while True:
                message = _read_json(proc, deadline)
                method = message.get("method")
                params = message.get("params") or {}
                if method == "item/completed":
                    item = params.get("item") or {}
                    if item.get("type") == "agentMessage":
                        text = item.get("text")
                        if isinstance(text, str) and text.strip():
                            final_parts.append(text)
                elif method == "agentMessage/delta":
                    # Deltas are intentionally ignored; completed agent messages are authoritative.
                    continue
                elif method == "turn/completed" and params.get("threadId") == thread_id:
                    turn = params.get("turn") or {}
                    status = turn.get("status")
                    if status not in ("completed", None):
                        raise RuntimeError(
                            f"Subscription backend: turn ended with status {status!r}."
                        )
                    break

            text = "\n".join(final_parts).strip()
            if not text:
                raise RuntimeError("Subscription backend: no final assistant text.")
            return text
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proc.kill()
