"""local_model — a thin headless `claude -p` bridge (the Max-session path the strands use).

complete(prompt) shells `claude -p --output-format json` on the local Max subscription and returns the model's
text. It strips the conflicting auth/proxy env (ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN / ANTHROPIC_BASE_URL /
proxies) so the OAuth session resolves, and requires CLAUDE_CODE_OAUTH_TOKEN in the environment (the long-lived
`claude setup-token`). This is what turns the PENDING harness runs into real numbers — no hosted API, no per-call
cost. Optional, dev-only; the harnesses' deterministic parts work without it.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess

_STRIP = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL",
          "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy")
_CLAUDE = shutil.which("claude") or "claude"


def available() -> bool:
    return bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"))


def _env() -> dict:
    e = {k: v for k, v in os.environ.items() if k not in _STRIP}
    e["NO_PROXY"] = "127.0.0.1,localhost"
    return e


def complete(prompt: str, system: str = "", timeout: int = 180) -> str:
    """One headless claude -p completion on the Max subscription. Returns the model's text ('' on error)."""
    if not available():
        raise RuntimeError("CLAUDE_CODE_OAUTH_TOKEN not set — export it (e.g. from brain-os/.env) to run live benches")
    cmd = [_CLAUDE, "-p", prompt, "--output-format", "json"]
    if system:
        cmd += ["--append-system-prompt", system]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                             env=_env(), timeout=timeout)
        d = json.loads(out.stdout or "{}")
        return "" if d.get("is_error") else (d.get("result") or "")
    except Exception:
        return ""


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("claude on PATH:", _CLAUDE, "| token present:", available())
    if available():
        print("smoke:", repr(complete("Reply with exactly the token: BRIDGE_OK")[:40]))
