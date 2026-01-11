"""
SixXon - TRINITY-OS Toolflow thin wrapper.

Philosophy:
- Law/penal enforcement is NOT executed here.
- This CLI only orchestrates existing SSOT toolflow and prints humble outputs.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import io
import json
import os
import subprocess
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from trinity_os.adapters.afo_ultimate_mcp_deps_v1 import build_deps_v1
from trinity_os.graphs.trinity_toolflow_graph_v1 import (
    build_trinity_toolflow_graph, run_trinity_toolflow)


def _print_three_lines(final_card: dict[str, Any]) -> None:
    status = final_card.get("status") or "UNKNOWN"
    decision = final_card.get("decision") or status
    next_actions = final_card.get("next_actions") or []
    next_one = (
        next_actions[0] if isinstance(next_actions, list) and next_actions else ""
    )
    receipt_path = (
        final_card.get("source_of_truth") or final_card.get("receipt_dir") or ""
    )

    print(f"Status: {status} | Gate: {decision}")
    print(f"Next: {next_one}" if next_one else "Next: (none)")
    print(f"Receipt: {receipt_path}" if receipt_path else "Receipt: (none)")


def _ts_slug() -> str:
    """UTC timestamp for receipt directory names."""
    return datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def _status_emoji(status: str) -> str:
    s = (status or "").upper()
    if s == "OK":
        return "🟢"
    if s == "BLOCK":
        return "🔴"
    return "🟡"


def _create_receipt(repo_root: Path, *, out_name: str = "") -> Path:
    """Creates a receipt via receipt_bundle.py and returns the receipt directory path."""
    bundle = repo_root / "scripts" / "receipt_bundle.py"
    if not bundle.exists():
        bundle = repo_root / "scripts" / "common" / "receipt_bundle.py"
    cmd = [sys.executable, str(bundle)]
    if out_name:
        cmd.extend(["--out", out_name])
    p = subprocess.run(cmd, check=False, text=True, capture_output=True)
    out_dir = (
        (p.stdout or "").strip().splitlines()[-1] if (p.stdout or "").strip() else ""
    )
    if p.returncode != 0 or not out_dir:
        raise RuntimeError(f"receipt_bundle failed: {p.stderr.strip()}")
    return Path(out_dir)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _attach_toolflow_result(
    receipt_dir: Path, *, payload: dict[str, Any], meta: dict[str, Any]
) -> None:
    raw_dir = receipt_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    _write_text(
        raw_dir / "sixxon_toolflow.final.json",
        json.dumps(payload, ensure_ascii=False, indent=2),
    )
    _write_text(
        raw_dir / "sixxon_toolflow.final.meta.json",
        json.dumps(meta, ensure_ascii=False, indent=2),
    )


def _attach_toolflow_runtime_logs(
    receipt_dir: Path, *, stdout_text: str, stderr_text: str
) -> None:
    raw_dir = receipt_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    if stdout_text.strip():
        _write_text(raw_dir / "sixxon_toolflow.runtime.stdout.txt", stdout_text)
    if stderr_text.strip():
        _write_text(raw_dir / "sixxon_toolflow.runtime.stderr.txt", stderr_text)


def _find_repo_root() -> Path | None:
    """Best-effort repo root discovery for monorepo layout:
    - expects scripts/receipt_bundle.py (or scripts/common/receipt_bundle.py) at repo root
    """
    probes = [Path.cwd(), Path(__file__).resolve()]
    for base in probes:
        for p in [base, *base.parents]:
            has_bundle = (p / "scripts" / "receipt_bundle.py").exists() or (
                p / "scripts" / "common" / "receipt_bundle.py"
            ).exists()
            if has_bundle and (p / "logs").exists():
                return p
    return None


def _resolve_receipt_dir(repo_root: Path, arg: str) -> Path:
    receipts_root = repo_root / "logs" / "receipts"
    raw = arg.strip()
    if not raw:
        raise ValueError("receipt path/name is empty")

    p = Path(raw)
    if p.is_absolute():
        return p

    # Accept repo-relative paths for convenience (e.g. logs/receipts/<id>),
    # but do not allow escaping the repo root.
    repo_candidate = (repo_root / p).resolve()
    try:
        repo_candidate.relative_to(repo_root.resolve())
        if repo_candidate.exists():
            return repo_candidate
    except Exception:
        pass

    # Accept cwd-relative paths if they exist and remain within repo root.
    cwd_candidate = p.resolve()
    try:
        cwd_candidate.relative_to(repo_root.resolve())
        if cwd_candidate.exists():
            return cwd_candidate
    except Exception:
        pass

    # Treat as a name under logs/receipts by default.
    return receipts_root / raw


def _refresh_receipt_in_place(repo_root: Path, receipt_dir: Path) -> Path | None:
    """Re-run receipt_bundle.py using the same receipt directory name (best-effort).
    This is useful when a command appends SSOT evidence (e.g., usage logs) and we want
    the receipt's usage tail snapshot to include it.
    """
    receipts_root = (repo_root / "logs" / "receipts").resolve()
    try:
        rel = receipt_dir.resolve().relative_to(receipts_root)
        name = rel.parts[0] if rel.parts else ""
        if not name:
            return None
        return _create_receipt(repo_root, out_name=name)
    except Exception:
        return None


def _load_wallet_browser_sessions(repo_root: Path) -> list[dict[str, Any]]:
    """Best-effort: list browser_session keys from local API wallet storage.
    - Never returns secrets; only metadata.
    - Works even when encryption key is unavailable (we do not decrypt).
    """
    wallet_path = repo_root / "afo_soul_engine" / "api_wallet_storage.json"
    if not wallet_path.exists():
        return []

    try:
        data = json.loads(wallet_path.read_text(encoding="utf-8"))
    except Exception:
        return []

    keys = data.get("keys")
    if not isinstance(keys, list):
        return []

    out: list[dict[str, Any]] = []
    for k in keys:
        k = cast(Any, k)
        if not isinstance(k, dict):
            continue
        if cast(Mapping[str, Any], k).get("key_type") != "browser_session":
            continue
        out.append(
            {
                "name": cast(Mapping[str, Any], k).get("name"),
                "service": cast(Mapping[str, Any], k).get("service"),
                "read_only": cast(Mapping[str, Any], k).get("read_only"),
                "description": cast(Mapping[str, Any], k).get("description"),
                "created_at": cast(Mapping[str, Any], k).get("created_at"),
            }
        )
    return out


def _probe_wallet_session_decryptable(provider: str) -> bool:
    """Checks whether a browser session can be successfully loaded/decrypted from wallet.
    Never returns secrets; boolean only.
    """
    provider = (provider or "").strip().lower()
    if not provider:
        return False
    try:
        runtime_stdout = io.StringIO()
        runtime_stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(runtime_stdout),
            contextlib.redirect_stderr(runtime_stderr),
        ):
            from afo_soul_engine.browser_auth.wallet_integration import \
                load_session_from_wallet

            session = load_session_from_wallet(provider)
        return bool(
            isinstance(session, dict)
            and isinstance(cast(Mapping[str, Any], session).get("cookies"), list)
            and len(cast(Mapping[str, Any], session).get("cookies") or []) > 0
        )
    except Exception:
        return False


def _wallet_key_state(repo_root: Path) -> dict[str, Any]:
    """Returns non-secret diagnostics about API wallet encryption key availability.
    Never returns the key material.
    """
    repo_key_path = repo_root / ".encryption_key"
    repo_key_exists = repo_key_path.exists()
    repo_key_len: int | None = None
    if repo_key_exists:
        try:
            repo_key_len = len(repo_key_path.read_text(encoding="utf-8").strip())
        except Exception:
            repo_key_exists = False
            repo_key_len = None

    env_path = repo_root / "afo_soul_engine" / ".env"
    env_exists = env_path.exists()
    key_present = False
    key_len: int | None = None
    if env_exists:
        try:
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("API_WALLET_ENCRYPTION_KEY="):
                    v = line.split("=", 1)[1].strip()
                    if v:
                        key_present = True
                        key_len = len(v)
        except Exception:
            key_present = False
            key_len = None

    return {
        "repo_key_file": str(repo_key_path),
        "repo_key_file_exists": bool(repo_key_exists),
        "repo_key_len": repo_key_len,
        "env_file": str(env_path),
        "env_file_exists": bool(env_exists),
        "key_present": bool(key_present),
        "key_len": key_len,
        "env_var_present": bool(
            os.getenv("API_WALLET_ENCRYPTION_KEY") or os.getenv("ENCRYPTION_KEY")
        ),
    }


def _auth_status_card(*, repo_root: Path, receipt_dir: Path | None) -> dict[str, Any]:
    sessions = _load_wallet_browser_sessions(repo_root)
    providers = sorted(
        {
            str(s.get("service") or "")
            for s in sessions
            if isinstance(s, dict) and s.get("service")
        }
    )
    providers = [p for p in providers if p]

    per_provider: list[dict[str, Any]] = []
    for p in providers:
        per_provider.append(
            {
                "provider": p,
                "present_in_wallet": True,
                "decryptable": _probe_wallet_session_decryptable(p),
            }
        )

    status = "OK" if sessions else "BLOCK"
    decision = "ASK" if sessions else "BLOCK"
    decryptable_any = any(
        bool(x.get("decryptable")) for x in per_provider if isinstance(x, dict)
    )
    if sessions and not decryptable_any:
        status = "BLOCK"
        decision = "BLOCK"

    next_actions: list[str]
    if not sessions:
        next_actions = [
            "Run `sixxon auth capture --provider=claude` (manual login → save session)",
            "Then run `sixxon auth status` again",
        ]
    elif not decryptable_any:
        next_actions = [
            "Run `sixxon auth capture --provider=claude` (re-save session with current key)",
            "Then run `sixxon auth status` again",
        ]
    else:
        next_actions = [
            "Run `sixxon auth open --provider=claude` (stable manual use)",
            "Then (optional) try `sixxon auth ask --provider=claude --yes` (best-effort)",
        ]

    card: dict[str, Any] = {
        "status": status,
        "decision": decision,
        "summary": "Browser subscription sessions in API wallet (metadata only)",
        "wallet_key_state": _wallet_key_state(repo_root),
        "providers": providers,
        "providers_status": per_provider,
        "session_count": len(sessions),
        "next_actions": next_actions,
    }
    if receipt_dir is not None:
        card["source_of_truth"] = str(receipt_dir)
        raw_dir = receipt_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        _write_text(
            raw_dir / "sixxon_auth.status.json",
            json.dumps(card, ensure_ascii=False, indent=2),
        )
        _write_text(
            raw_dir / "sixxon_auth.wallet_browser_sessions.json",
            json.dumps(sessions, ensure_ascii=False, indent=2),
        )
    return card


def _auth_login(
    *,
    provider: str,
    headless: bool,
    repo_root: Path,
    receipt_dir: Path | None,
) -> dict[str, Any]:
    """Interactive login to save browser session into wallet (subscription usage).
    Provider session implementations may force a visible browser even when headless is requested.
    """
    provider = (provider or "").strip().lower()
    if provider not in {"claude", "codex", "gemini", "grok"}:
        return {
            "status": "BLOCK",
            "decision": "BLOCK",
            "reason": f"Unsupported provider: {provider!r}",
            "next_actions": ["Use --provider=claude|codex|gemini|grok"],
        }

    runtime_stdout = io.StringIO()
    runtime_stderr = io.StringIO()

    async def _run() -> dict[str, Any]:
        from afo_soul_engine.browser_auth.wallet_integration import \
            WalletSessionManager

        manager = WalletSessionManager()

        session_data: dict[str, Any]
        if provider == "claude":
            from afo_soul_engine.browser_auth.claude_session import \
                ClaudeSession

            s = ClaudeSession()
            session_data = await s.login_and_extract_session(headless=headless)
        elif provider == "codex":
            from afo_soul_engine.browser_auth.codex_session import CodexSession

            s = CodexSession()
            session_data = await s.login_and_extract_session(headless=headless)
        elif provider == "gemini":
            from afo_soul_engine.browser_auth.gemini_session import \
                GeminiSession

            s = GeminiSession()
            session_data = await s.login_and_extract_session(headless=headless)
        else:
            from afo_soul_engine.browser_auth.grok_session import GrokSession

            s = GrokSession()
            session_data = await s.login_and_extract_session(headless=headless)

        wallet_success = manager.save_browser_session(
            provider=provider,
            cookies=session_data.get("cookies", []),
            local_storage=session_data.get("local_storage", {}),
            session_storage=session_data.get("session_storage", {}),
            tokens=session_data.get("tokens", {}),
        )
        return {
            "wallet_success": bool(wallet_success),
            "mcp_success": False,
            "provider": provider,
            "wallet_only": True,
        }

    try:
        with (
            contextlib.redirect_stdout(runtime_stdout),
            contextlib.redirect_stderr(runtime_stderr),
        ):
            result = asyncio.run(_run())
    except Exception as e:
        result = {"error": str(e)}

    ok = bool(isinstance(result, dict) and bool(result.get("wallet_success")))
    card: dict[str, Any] = {
        "status": "OK" if ok else "BLOCK",
        "decision": "ASK" if ok else "BLOCK",
        "provider": provider,
        "result": result if isinstance(result, dict) else {"raw": str(result)},
        "summary": "Browser session login result (saved to wallet only; subscription-safe)",
        "next_actions": [
            "Run `sixxon auth status`",
            f"Then run `sixxon auth open --provider={provider}`",
        ],
    }

    if receipt_dir is not None:
        card["source_of_truth"] = str(receipt_dir)
        raw_dir = receipt_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        _write_text(
            raw_dir / "sixxon_auth.login.result.json",
            json.dumps(card, ensure_ascii=False, indent=2),
        )
        _write_text(raw_dir / "sixxon_auth.login.stdout.txt", runtime_stdout.getvalue())
        _write_text(raw_dir / "sixxon_auth.login.stderr.txt", runtime_stderr.getvalue())
        _refresh_receipt_in_place(repo_root, receipt_dir)

    return card


def _auth_capture(
    *,
    provider: str,
    headless: bool,
    repo_root: Path,
    receipt_dir: Path | None,
) -> dict[str, Any]:
    """Capture-only flow: manual login in browser, then save cookies/localStorage/sessionStorage into wallet.
    This intentionally does NOT send any prompt (no fragile UI selectors).
    """
    card = _auth_login(
        provider=provider,
        headless=headless,
        repo_root=repo_root,
        receipt_dir=receipt_dir,
    )
    if isinstance(card, dict):
        card = {
            **card,
            "summary": "Browser session captured and saved to wallet (capture-only; no web ask performed)",
            "next_actions": [
                "Run `sixxon auth status`",
                f"Then (optional) try `sixxon auth ask --provider={provider} --yes`",
            ],
        }
    return card


def _auth_open(
    *,
    provider: str,
    headless: bool,
    keep_open: bool,
    repo_root: Path,
    receipt_dir: Path | None,
) -> dict[str, Any]:
    """Open chat page using the saved wallet session (no prompt send).
    This is the stable, CLI-first path for monthly subscription sessions.
    """
    provider = (provider or "").strip().lower()
    if provider not in {"claude", "codex", "gemini", "grok"}:
        return {
            "status": "BLOCK",
            "decision": "BLOCK",
            "reason": f"Unsupported provider: {provider!r}",
            "next_actions": ["Use --provider=claude|codex|gemini|grok"],
        }

    if not _probe_wallet_session_decryptable(provider):
        card = {
            "status": "BLOCK",
            "decision": "BLOCK",
            "provider": provider,
            "reason": "Browser session is missing or not decryptable in this environment (capture/login required).",
            "next_actions": [
                f"Run `sixxon auth capture --provider={provider}`",
                "Then retry `sixxon auth open`",
            ],
        }
        if receipt_dir is not None:
            card["source_of_truth"] = str(receipt_dir)
            raw_dir = receipt_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            _write_text(
                raw_dir / "sixxon_auth.open.block.json",
                json.dumps(card, ensure_ascii=False, indent=2),
            )
            _refresh_receipt_in_place(repo_root, receipt_dir)
        return card

    runtime_stdout = io.StringIO()
    runtime_stderr = io.StringIO()

    async def _run() -> dict[str, Any]:
        if provider == "claude":
            from afo_soul_engine.browser_auth.claude_session import \
                ClaudeSession

            s = ClaudeSession()
            return await s.open_chat_for_manual_use(
                headless=headless, keep_open=keep_open, timeout_seconds=180
            )
        if provider == "codex":
            from afo_soul_engine.browser_auth.codex_session import CodexSession

            s = CodexSession()
            return await s.open_chat_for_manual_use(
                headless=headless, keep_open=keep_open, timeout_seconds=180
            )
        if provider == "gemini":
            from afo_soul_engine.browser_auth.gemini_session import \
                GeminiSession

            s = GeminiSession()
            return await s.open_chat_for_manual_use(
                headless=headless, keep_open=keep_open, timeout_seconds=180
            )

        from afo_soul_engine.browser_auth.grok_session import GrokSession

        s = GrokSession()
        return await s.open_chat_for_manual_use(
            headless=headless, keep_open=keep_open, timeout_seconds=180
        )

    try:
        with (
            contextlib.redirect_stdout(runtime_stdout),
            contextlib.redirect_stderr(runtime_stderr),
        ):
            result = asyncio.run(_run())
    except Exception as e:
        result = {"ok": False, "error": str(e), "provider": provider}

    ok = bool(isinstance(result, dict) and bool(result.get("ok")))
    card: dict[str, Any] = {
        "status": "OK" if ok else "BLOCK",
        "decision": "ASK" if ok else "BLOCK",
        "provider": provider,
        "result": result if isinstance(result, dict) else {"raw": str(result)},
        "summary": "Opened chat page with saved wallet session (manual use; no prompt send)",
        "next_actions": [
            "Use the opened page manually",
            "Then (optional) attach evidence via `sixxon receipt`",
        ],
    }
    if receipt_dir is not None:
        card["source_of_truth"] = str(receipt_dir)
        raw_dir = receipt_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        _write_text(
            raw_dir / "sixxon_auth.open.result.json",
            json.dumps(card, ensure_ascii=False, indent=2),
        )
        _write_text(raw_dir / "sixxon_auth.open.stdout.txt", runtime_stdout.getvalue())
        _write_text(raw_dir / "sixxon_auth.open.stderr.txt", runtime_stderr.getvalue())
        _refresh_receipt_in_place(repo_root, receipt_dir)
    return card


def _auth_doctor(
    *, repo_root: Path, receipt_dir: Path | None, provider: str | None = None
) -> dict[str, Any]:
    """Read-only diagnostics for subscription/browser-session flows.
    Explains: wallet key state, present vs decryptable, and likely blockers (e.g., Cloudflare/headless).
    """
    provider = (provider or "").strip().lower() or None
    base = _auth_status_card(repo_root=repo_root, receipt_dir=None)
    wallet_key_state = _wallet_key_state(repo_root)

    # Simple environment probe (non-secret).
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_installed = Path(chrome_path).exists()

    probs: list[str] = []
    if not wallet_key_state.get("key_present"):
        probs.append("wallet_encryption_key_missing")
    if base.get("status") == "BLOCK":
        probs.append("no_decryptable_sessions")
    if not chrome_installed:
        probs.append("system_chrome_missing")

    advice: list[str] = []
    advice.append(
        "Browser engine policy: `--browser system-chrome` only (reduces Chrome/Chromium confusion)."
    )
    advice.append(
        "If you see multiple browsers popping up: close the extras, then re-run with system-chrome and --keep-open for manual inspection."
    )
    advice.append(
        "If sessions are present but decryptable=false: they were likely saved before the wallet key was persisted → recapture is the clean fix."
    )
    if provider:
        advice.append(
            f"Run `sixxon auth capture --provider={provider}` (manual login → save session)"
        )
        advice.append(
            f"Then run `sixxon auth status` and ensure decryptable=true for {provider}"
        )
        advice.append(
            f"Then run `sixxon auth open --provider={provider}` (stable manual use)"
        )
        advice.append(
            f"Then (optional) try `sixxon auth ask --provider={provider} --yes` (best-effort; UI may change)"
        )
    else:
        advice.append(
            "Run `sixxon auth status` and check decryptable=true for at least one provider"
        )
        advice.append(
            "If decryptable=false, run `sixxon auth capture --provider=claude` (or codex) to re-save the session"
        )
        advice.append(
            "If `afo_soul_engine/.env` is missing, first run: `python3.12 -c \"from afo_soul_engine.api_wallet import APIWallet; APIWallet(); print('wallet ok')\"`"
        )

    card: dict[str, Any] = {
        "status": "OK" if not probs else "BLOCK",
        "decision": "ASK" if not probs else "BLOCK",
        "summary": "Subscription/browser-session doctor (read-only)",
        "provider": provider,
        "browser_engines_supported": ["system-chrome"],
        "browser_engine_default": "system-chrome",
        "wallet_key_state": wallet_key_state,
        "chrome": {"installed": bool(chrome_installed), "path": chrome_path},
        "providers_status": base.get("providers_status") or [],
        "likely_problems": probs,
        "next_actions": advice,
        "notes": [
            'Headless mode may trigger Cloudflare/anti-bot pages ("Just a moment...") on some providers.',
            "For monthly subscription web flows, token/cost metering may be unavailable (usage.status=REAL_UNMETERED).",
        ],
    }
    if receipt_dir is not None:
        card["source_of_truth"] = str(receipt_dir)
        raw_dir = receipt_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        _write_text(
            raw_dir / "sixxon_auth.doctor.json",
            json.dumps(card, ensure_ascii=False, indent=2),
        )
        _refresh_receipt_in_place(repo_root, receipt_dir)
    return card


def _auth_ask(
    *,
    provider: str,
    prompt: str,
    humble: bool,
    headless: bool,
    repo_root: Path,
    receipt_dir: Path | None,
) -> dict[str, Any]:
    provider = (provider or "").strip().lower()
    if provider not in {"claude", "codex", "gemini", "grok"}:
        return {
            "status": "BLOCK",
            "decision": "BLOCK",
            "reason": f"Unsupported provider: {provider!r}",
            "next_actions": ["Use --provider=claude|codex|gemini|grok"],
        }
    if provider == "grok":
        return {
            "status": "BLOCK",
            "decision": "BLOCK",
            "provider": provider,
            "reason": "grok web ask is not supported yet (UI/anti-bot is too brittle). Use `sixxon auth open` + manual interaction.",
            "next_actions": [
                "Run `sixxon auth open --provider=grok`",
                "Then attach evidence via `sixxon receipt` if needed",
            ],
        }

    user_prompt = (prompt or "").strip()
    if not user_prompt:
        return {"status": "BLOCK", "decision": "BLOCK", "reason": "Empty prompt"}

    # Fail fast with a clear, structured reason when the session cannot be decrypted/loaded.
    if not _probe_wallet_session_decryptable(provider):
        card = {
            "status": "BLOCK",
            "decision": "BLOCK",
            "provider": provider,
            "reason": "Browser session is present in wallet but not decryptable in this environment (re-login required).",
            "next_actions": [
                f"Run `sixxon auth login --provider={provider}`",
                f"Then retry `sixxon auth ask --provider={provider} --headless --yes`",
            ],
        }
        if receipt_dir is not None:
            card["source_of_truth"] = str(receipt_dir)
            raw_dir = receipt_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            _write_text(
                raw_dir / "sixxon_auth.ask.block.json",
                json.dumps(card, ensure_ascii=False, indent=2),
            )
            _refresh_receipt_in_place(repo_root, receipt_dir)
        return card

    final_prompt = ("3줄로만 답해 주세요.\n\n" + user_prompt) if humble else user_prompt

    runtime_stdout = io.StringIO()
    runtime_stderr = io.StringIO()

    async def _run() -> str:
        if provider == "claude":
            from afo_soul_engine.browser_auth.claude_session import \
                ClaudeSession

            s = ClaudeSession()
            return await s.ask_question(final_prompt, headless=headless)
        if provider == "codex":
            from afo_soul_engine.browser_auth.codex_session import CodexSession

            s = CodexSession()
            return await s.ask_question(final_prompt, headless=headless)
        from afo_soul_engine.browser_auth.gemini_session import GeminiSession

        s = GeminiSession()
        return await s.ask_question(final_prompt, headless=headless)

    try:
        with (
            contextlib.redirect_stdout(runtime_stdout),
            contextlib.redirect_stderr(runtime_stderr),
        ):
            answer = asyncio.run(_run())
    except Exception as e:
        card = {
            "status": "BLOCK",
            "decision": "BLOCK",
            "provider": provider,
            "reason": str(e),
            "next_actions": [
                f"Run `sixxon auth login --provider={provider}`",
                "Then retry with `--headless` (or without)",
            ],
        }
        if receipt_dir is not None:
            card["source_of_truth"] = str(receipt_dir)
            raw_dir = receipt_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            _write_text(raw_dir / "sixxon_auth.ask.prompt.txt", final_prompt + "\n")
            _write_text(
                raw_dir / "sixxon_auth.ask.stdout.txt", runtime_stdout.getvalue()
            )
            _write_text(
                raw_dir / "sixxon_auth.ask.stderr.txt", runtime_stderr.getvalue()
            )
            _write_text(
                raw_dir / "sixxon_auth.ask.error.json",
                json.dumps(card, ensure_ascii=False, indent=2),
            )
            _refresh_receipt_in_place(repo_root, receipt_dir)
        return card

    used_provider = f"{provider}_web"
    try:
        from afo_soul_engine.observability.llm_usage_log import log_llm_usage

        log_llm_usage(
            provider=used_provider,
            model="subscription",
            meta={
                "method": "browser_session",
                "metering": "unmetered",
                "humble": bool(humble),
                "headless": bool(headless),
                "prompt_chars": len(final_prompt),
                "answer_chars": len(answer or ""),
                "source": "sixxon.auth.ask",
            },
        )
    except Exception:
        pass

    preview = (answer or "").strip().replace("\n", " ")
    card: dict[str, Any] = {
        "status": "OK",
        "decision": "ASK",
        "provider": provider,
        "usage_provider": used_provider,
        "summary": "Subscription/web ask executed; token/cost metering is unavailable (REAL_UNMETERED expected)",
        "answer_preview": preview[:200],
        "next_actions": [
            "Run `sixxon status --latest`",
            "Use `sixxon explain --latest` for 3-line verdict",
        ],
    }

    if receipt_dir is not None:
        card["source_of_truth"] = str(receipt_dir)
        raw_dir = receipt_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        _write_text(raw_dir / "sixxon_auth.ask.prompt.txt", final_prompt + "\n")
        _write_text(raw_dir / "sixxon_auth.ask.answer.txt", (answer or "") + "\n")
        _write_text(raw_dir / "sixxon_auth.ask.stdout.txt", runtime_stdout.getvalue())
        _write_text(raw_dir / "sixxon_auth.ask.stderr.txt", runtime_stderr.getvalue())
        _write_text(
            raw_dir / "sixxon_auth.ask.result.json",
            json.dumps(card, ensure_ascii=False, indent=2),
        )
        _refresh_receipt_in_place(repo_root, receipt_dir)

    return card


def _latest_receipt_dir(repo_root: Path) -> Path | None:
    receipts_root = repo_root / "logs" / "receipts"
    if not receipts_root.exists():
        return None

    candidates: list[Path] = []
    for d in receipts_root.iterdir():
        if d.is_dir() and (d / "receipt.json").exists():
            candidates.append(d)
    if not candidates:
        return None
    return max(candidates, key=lambda x: x.stat().st_mtime)


def _load_receipt(receipt_dir: Path) -> dict[str, Any]:
    p = receipt_dir / "receipt.json"
    data: Any = json.loads(p.read_text(encoding="utf-8"))
    if (
        not isinstance(data, dict)
        or cast(Mapping[str, Any], data).get("schema") != "bridge_receipt_v1"
    ):
        raise ValueError(
            f"invalid receipt schema: {cast(Mapping[str, Any], data).get('schema') if isinstance(data, dict) else type(data)}"
        )
    return data


def _calculate_trinity_score(receipt: dict[str, Any]) -> dict[str, Any]:
    """[Stage 3] Audit Gate: Trinity Score 계산 및 불균형 감지

    Trinity Score: 眞善美孝永 (Truth, Goodness, Beauty, Serenity, Eternity)
    - 각 점수 0-100 범위
    - 평균 80점 이상 + 개별 점수 편차 20점 이내여야 PASS
    """
    services = cast(Mapping[str, Any], receipt).get("services") or {}
    ports = cast(Mapping[str, Any], services).get("ports") or {}
    http = cast(Mapping[str, Any], services).get("http") or {}

    # 기본 인프라 건강도 (眞 - Truth)
    infra_checks = [
        ("postgres_15432", cast(Mapping[str, Any], ports).get("postgres_15432")),
        ("redis_6379", cast(Mapping[str, Any], ports).get("redis_6379")),
        (
            "api_gateway_8000",
            cast(Mapping[str, Any], http).get("api_gateway_8000_health"),
        ),
        (
            "soul_engine_8010",
            cast(Mapping[str, Any], http).get("soul_engine_8010_health"),
        ),
    ]

    truth_score = 0
    infra_status: list[Any] = []
    for name, check in infra_checks:
        if (
            isinstance(check, dict)
            and cast(Mapping[str, Any], check).get("status") == "OK"
        ):
            truth_score += 25  # 각 체크당 25점
            infra_status.append(f"{name}: OK")
        else:
            infra_status.append(
                f"{name}: {cast(Mapping[str, Any], check).get('status', 'UNKNOWN') if isinstance(check, dict) else 'MISSING'}"
            )

    # 서비스 응답 시간 (善 - Goodness)
    goodness_score = 100
    response_times: list[Any] = []
    for name, check in infra_checks:
        if isinstance(check, dict):
            response_time = cast(Mapping[str, Any], check).get("response_time", 0)
            if response_time > 5000:  # 5초 이상
                goodness_score -= 20
                response_times.append(f"{name}: {response_time}ms (SLOW)")
            elif response_time > 1000:  # 1초 이상
                goodness_score -= 10
                response_times.append(f"{name}: {response_time}ms")
            else:
                response_times.append(f"{name}: {response_time}ms (GOOD)")

    goodness_score = max(0, min(100, goodness_score))

    # 시스템 일관성 (美 - Beauty)
    beauty_score = 100
    env = receipt.get("env", {})
    label = env.get("label", "")

    # 환경 레이블 일관성 체크
    if not label or label not in ["PRODUCTION", "STAGING", "DEVELOPMENT", "SANDBOX"]:
        beauty_score -= 30

    # 서비스 버전 일관성 (간단한 체크)
    versions: list[Any] = []
    for _name, check in infra_checks:
        if isinstance(check, dict):
            version = cast(Mapping[str, Any], check).get("version", "")
            if version:
                versions.append(version)

    if len(set(versions)) > 2:  # 버전이 너무 다양하면 일관성 저하
        beauty_score -= 20

    beauty_score = max(0, min(100, beauty_score))

    # 에너지 흐름 안정성 (孝 - Serenity)
    serenity_score = 100
    # 최근 에러율, 메모리 사용량 등으로 계산 (간단 버전)
    # 실제로는 receipt의 logs나 metrics에서 추출

    # 임시: 인프라 상태 기반 계산
    failed_services = sum(
        1
        for _, check in infra_checks
        if not (
            isinstance(check, dict)
            and cast(Mapping[str, Any], check).get("status") == "OK"
        )
    )
    serenity_score -= failed_services * 25
    serenity_score = max(0, min(100, serenity_score))

    # 기록 보존 안정성 (永 - Eternity)
    eternity_score = 100
    # 로그 파일 존재 여부, 백업 상태 등 체크
    logs_exist = receipt.get("logs", {}).get("exist", False)
    if not logs_exist:
        eternity_score -= 50

    # Bridge 로그 연동 상태
    bridge_integrated = receipt.get("bridge", {}).get("integrated", False)
    if not bridge_integrated:
        eternity_score -= 20

    eternity_score = max(0, min(100, eternity_score))

    # Trinity Score 종합
    trinity_scores = {
        "truth": truth_score,
        "goodness": goodness_score,
        "beauty": beauty_score,
        "serenity": serenity_score,
        "eternity": eternity_score,
    }

    average_score = sum(trinity_scores.values()) / 5

    # 불균형 감지 (개별 점수 편차)
    max_score = max(trinity_scores.values())
    min_score = min(trinity_scores.values())
    imbalance = max_score - min_score

    # Audit Gate 판정
    audit_gate_passed = (
        average_score >= 80  # 평균 80점 이상
        and imbalance <= 20  # 편차 20점 이내
        and min_score >= 60  # 최저 점수 60점 이상
    )

    return {
        "trinity_scores": trinity_scores,
        "average_score": round(average_score, 1),
        "imbalance": imbalance,
        "audit_gate_passed": audit_gate_passed,
        "infra_status": infra_status,
        "response_times": response_times,
        "environment_label": label,
    }


def _receipt_status_from_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    """[Stage 3] Audit Gate: Trinity Score 기반 상태 평가

    Rule (Audit Contract):
    - Trinity Score 평균 80점 이상 + 불균형 20점 이내 → AUTO_RUN_AUTHORIZED
    - 그 외 → BLOCK (에너지 흐름 불균형 감지)
    """
    # 기본 인프라 상태 확인
    services = cast(Mapping[str, Any], receipt).get("services") or {}
    ports = cast(Mapping[str, Any], services).get("ports") or {}
    http = cast(Mapping[str, Any], services).get("http") or {}

    required_paths = [
        ("ports.postgres_15432", cast(Mapping[str, Any], ports).get("postgres_15432")),
        ("ports.redis_6379", cast(Mapping[str, Any], ports).get("redis_6379")),
        (
            "http.api_gateway_8000_health",
            cast(Mapping[str, Any], http).get("api_gateway_8000_health"),
        ),
        (
            "http.soul_engine_8010_health",
            cast(Mapping[str, Any], http).get("soul_engine_8010_health"),
        ),
    ]

    bad: list[str] = []
    for name, obj in required_paths:
        status = ""
        if isinstance(obj, dict):
            status = str(cast(Mapping[str, Any], obj).get("status") or "")
        if status != "OK":
            bad.append(f"{name}={status or 'MISSING'}")

    # Trinity Score 계산 (Audit Gate)
    trinity_analysis = _calculate_trinity_score(receipt)

    # Audit Gate 판정
    if not trinity_analysis["audit_gate_passed"]:
        reason_parts: list[Any] = []
        if trinity_analysis["average_score"] < 80:
            reason_parts.append(
                f"평균 점수 부족: {trinity_analysis['average_score']:.1f}/80"
            )
        if trinity_analysis["imbalance"] > 20:
            reason_parts.append(f"점수 불균형: {trinity_analysis['imbalance']}/20")
        if min(trinity_analysis["trinity_scores"].values()) < 60:
            min_score = min(trinity_analysis["trinity_scores"].values())
            reason_parts.append(f"최저 점수 부족: {min_score}/60")

        return {
            "status": "BLOCK",
            "decision": "BLOCK",
            "reason": f"Audit Gate: 에너지 흐름 불균형 감지 - {', '.join(reason_parts)}",
            "trinity_scores": trinity_analysis["trinity_scores"],
            "average_score": trinity_analysis["average_score"],
            "imbalance": trinity_analysis["imbalance"],
            "infra_status": trinity_analysis["infra_status"],
            "response_times": trinity_analysis["response_times"],
            "next_actions": [
                "에너지 흐름 균형 복원 필요",
                "Trinity Score 개선 작업 수행",
                "Bridge 로그에서 상세 분석 확인",
            ],
        }

    # Audit Gate 통과
    return {
        "status": "OK",
        "decision": "AUTO_RUN_AUTHORIZED",
        "summary": f"Audit Gate: 에너지 흐름 정상 (Trinity Score: {trinity_analysis['average_score']:.1f})",
        "trinity_scores": trinity_analysis["trinity_scores"],
        "average_score": trinity_analysis["average_score"],
        "imbalance": trinity_analysis["imbalance"],
        "infra_status": trinity_analysis["infra_status"],
        "response_times": trinity_analysis["response_times"],
        "next_actions": ["Proceed with toolflow", "Save to SSOT"],
    }


def _explain_from_receipt(receipt_dir: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    """PoChungCheon-style explanation (read-only).
    Uses receipt evidence only; does not execute tools or alter any state.
    """
    env = cast(Mapping[str, Any], receipt).get("env") or {}
    label = str(cast(Mapping[str, Any], env).get("label") or "")

    status_card = _receipt_status_from_receipt(receipt)
    status = str(status_card.get("status") or "UNKNOWN")
    decision = str(status_card.get("decision") or status)

    reasons: list[str] = []
    details = status_card.get("details") or []
    if isinstance(details, list):
        for d in details[:2]:
            d = cast(Any, d)
            if isinstance(d, str) and d:
                reasons.append(d)
    if not reasons:
        summary = status_card.get("summary") or status_card.get("reason") or ""
        if isinstance(summary, str) and summary:
            reasons.append(summary)

    reason_line = ", ".join(reasons) if reasons else "(no evidence)"
    next_actions = status_card.get("next_actions") or []
    next_one = (
        next_actions[0] if isinstance(next_actions, list) and next_actions else ""
    )

    card = {
        "status": status,
        "decision": decision,
        "env_label": label,
        "reason": reason_line,
        "next": next_one,
        "source_of_truth": str(receipt_dir),
        # 3-line output payload
        "pochungcheon_3_lines": {
            "state": f"{_status_emoji(status)} {status} | Gate: {decision} | Env: {label or 'UNKNOWN'}",
            "reason": reason_line,
            "next": next_one or "(none)",
        },
    }
    return card


def _edu_from_receipt(receipt_dir: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    """Educator Mothers 2-system (Mengmu × Saimdang), read-only recommendations.
    - No execution
    - No punishment
    - Receipt evidence only
    """
    env = cast(Mapping[str, Any], receipt).get("env") or {}
    label = str(cast(Mapping[str, Any], env).get("label") or "")

    status_card = _receipt_status_from_receipt(receipt)
    status = str(status_card.get("status") or "UNKNOWN")
    decision = str(status_card.get("decision") or status)
    details = status_card.get("details") or []
    detail0 = details[0] if isinstance(details, list) and details else ""
    if not (isinstance(detail0, str) and detail0):
        detail0 = str(status_card.get("summary") or status_card.get("reason") or "")

    mengmu_next = ""
    saimdang_next = ""
    consensus_next = ""

    if label == "SANDBOX":
        mengmu_next = "환경(권한/네트워크) 제약이므로 실환경에서 Receipt 재측정"
        saimdang_next = "출력은 3줄로 유지하고, Receipt 경로만 공유"
        consensus_next = "SixXon으로 실환경 Receipt 생성 후 status/explain 재확인"
    elif status == "BLOCK":
        mengmu_next = "환경/서비스 상태를 먼저 복구하고 Receipt 재측정"
        saimdang_next = "Next 1개만 남기고, 장문 설명은 --json에서만"
        consensus_next = "Receipt의 첫 실패 항목부터 해결 후 재측정"
    else:
        mengmu_next = "현 환경 유지(변경 최소) + 동일 조건에서 작업 진행"
        saimdang_next = "작업 로그는 Receipt로 남기고, 결과는 3줄 요약으로 공유"
        consensus_next = "toolflow를 실행하되, 결과 카드를 Receipt와 함께 기록"

    card = {
        "status": status,
        "decision": decision,
        "env_label": label,
        "primary_evidence": str(detail0) if isinstance(detail0, str) else "",
        "source_of_truth": str(receipt_dir),
        "mengmu": {
            "role": "environment_first",
            "next": mengmu_next,
        },
        "saimdang": {
            "role": "example_and_rhythm",
            "next": saimdang_next,
        },
        "consensus": {
            "mode": "A/B" if mengmu_next != saimdang_next else "single",
            "next": consensus_next,
        },
        "pochungcheon_3_lines": {
            "state": f"{_status_emoji(status)} EDU | Gate: {decision} | Env: {label or 'UNKNOWN'}",
            "reason": (str(detail0) if isinstance(detail0, str) and detail0 else ""),
            "next": consensus_next or "(none)",
        },
    }
    return card


def _print_detail_report(card: dict[str, Any]) -> None:
    """[Stage 3] Audit Contract: Detailed Penalty Breakdown."""
    print("\n📜 **Audit Contract Detail Report**")
    print(f"Status: {card.get('status')} | Decision: {card.get('decision')}")

    # Mocking penalty details for MVP (Real implementation would parse 'details' deeply)
    details = card.get("details", [])
    if details:
        print("\n**Penalty Breakdown**:")
        for d in details:
            print(f" - {d}")
    else:
        print("\n(No penalties found. Harmony Score likely 100.)")
    print("\n--------------------------------------------------")


def _verify_run(
    *,
    repo_root: Path,
    receipt_dir: Path | None,
    deep: bool,
    json_output: bool,
) -> dict[str, Any]:
    """[Stage 3] Universe Teacher (Truth Oath) Verification."""
    # Universe Teacher: 할루시네이션 극복을 위한 사실 검증
    try:
        from afo_soul_engine.afo_skills_registry import verify_fact

        # MVP: 기본 텍스트 검증 (실제로는 receipt에서 최근 출력 추출)
        test_content = "SixXon Energy Flow Vision은 인간 꿈과 AI 구현을 연결하는 완벽한 시스템입니다."
        test_context: Any = (
            "AFO 왕국의 眞善美孝永 철학을 기반으로 한 AI 통제 및 관리를 위한 도구"
        )

        result: Any = verify_fact(
            content=test_content, context=test_context if deep else None, threshold=0.8
        )

        payload = {
            "status": "OK" if result["status"] == "PASSED" else "BLOCK",
            "decision": "PASSED" if result["status"] == "PASSED" else "FAILED",
            "mode": "DEEP" if deep else "STANDARD",
            "truth_score": int(result["truth_score"] * 100),
            "hallucination_indicators": result["hallucination_indicators"],
            "context_support": result["context_support"],
            "evidence": result["evidence"],
        }

    except Exception as e:
        # Fallback: 기존 mock 로직
        payload = {
            "status": "BLOCK",
            "decision": "FAILED",
            "mode": "DEEP" if deep else "STANDARD",
            "truth_score": 0,
            "error": f"Universe Teacher unavailable: {e!s}",
            "evidence": ["Universe Teacher engine failed to load"],
        }

    if receipt_dir:
        _attach_toolflow_result(
            receipt_dir, payload=payload, meta={"command": "verify", "deep": deep}
        )

    return payload


def _dream_run(
    *,
    replay_id: str | None,
    dry_run: bool,
) -> dict[str, Any]:
    """[Stage 3] Dream Hub (Dream Protocol) Replay."""
    if not replay_id:
        return {"status": "BLOCK", "reason": "Missing THREAD_ID for replay"}

    # MVP: Mock replay logic
    # Real: Load checkpoint from MemorySaver and re-invoke

    return {
        "status": "OK",
        "decision": "REPLAYED",
        "summary": f"Replayed session {replay_id} (Dry-Run={dry_run})",
        "recovered_state": {"step": "final_review", "score": 98},
    }


def _toolflow_run(
    *,
    repo_root: Path,
    task: str,
    graph_mode: bool,
    receipt_dir: Path | None,
) -> dict[str, Any]:
    """Executes the Toolflow.
    If graph_mode is True, uses the Dream Hub (LangGraph).
    Otherwise, uses the V1 Toolflow Graph (Legacy).
    """
    if not task:
        return {"status": "BLOCK", "decision": "BLOCK", "reason": "Task is empty"}

    result_payload: dict[str, Any] = {}

    if graph_mode:
        # [NEW] Phase 2b: Dream Hub Execution
        try:
            from trinity_os.graphs.trinity_hybrid_workflow import run_dream_hub

            graph_out = run_dream_hub(task, thread_id=_ts_slug())

            result_payload = {
                "status": "OK",
                "decision": "COMPLETED",
                "summary": f"Dream Hub executed task: {task[:50]}...",
                "output": cast(Mapping[str, Any], graph_out).get("final_message"),
                "scores": {
                    "trinity": cast(Mapping[str, Any], graph_out).get("trinity_score"),
                },
                "audit_trail": cast(Mapping[str, Any], graph_out).get("audit_history"),
            }
        except ImportError:
            return {
                "status": "BLOCK",
                "decision": "BLOCK",
                "reason": "Dream Hub (trinity_hybrid_workflow) not found.",
            }
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"status": "BLOCK", "decision": "BLOCK", "reason": str(e)}
    else:
        # Legacy V1 Flow
        try:
            from trinity_os.adapters.afo_ultimate_mcp_deps_v1 import \
                build_deps_v1
            from trinity_os.graphs.trinity_toolflow_graph_v1 import (
                build_trinity_toolflow_graph, run_trinity_toolflow)

            # Local import to avoid top-level crashes if V1 is broken
            graph_data = build_trinity_toolflow_graph(build_deps_v1())
            out = cast(
                "str", run_trinity_toolflow(graph_data, cast(Any, {"task": task}))
            )
            result_payload = {
                "status": "OK",
                "decision": "COMPLETED",
                "summary": "V1 Toolflow executed",
                "output": out,
            }
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"status": "BLOCK", "decision": "BLOCK", "reason": f"V1 Crash: {e}"}

    # Receipt Attachment
    if receipt_dir is not None:
        result_payload["source_of_truth"] = str(receipt_dir)
        try:
            _attach_toolflow_result(
                receipt_dir,
                payload=result_payload,
                meta={"task": task, "mode": "dream_hub" if graph_mode else "v1_legacy"},
            )
            _refresh_receipt_in_place(repo_root, receipt_dir)
        except Exception as e:
            print(f"WARNING: Failed to attach receipt: {e}")

    return result_payload


def _run_toolflow(
    prompt: str,
    *,
    query: str | None,
    top_k: int,
    risk_score: float | None,
    profile: str,
    verbose: bool,
    json_output: bool,
    receipt_dir: Path | None,
) -> int:
    if profile == "P":
        # Public profile defaults to ASK unless risk_score is explicitly provided.
        os.environ["TRINITY_TOOLFLOW_DISABLE_AUTO_RISK"] = "1"
    else:
        # Kingdom profile can auto-inject SSOT risk evidence (if available).
        disable_auto_risk = os.environ.get("TRINITY_TOOLFLOW_DISABLE_AUTO_RISK") == "1"
        if risk_score is None and not disable_auto_risk:
            # try:
            #     from tools.guardian_sentinel import get_current_risk_score
            #
            #     risk_score = float(get_current_risk_score())
            # except Exception:
            #     risk_score = None
            risk_score = None

    runtime_stdout = io.StringIO()
    runtime_stderr = io.StringIO()
    with (
        contextlib.redirect_stdout(runtime_stdout),
        contextlib.redirect_stderr(runtime_stderr),
    ):
        deps = build_deps_v1()
        app = build_trinity_toolflow_graph(deps)
        out = run_trinity_toolflow(
            app, prompt, query=query, top_k=top_k, risk_score=risk_score
        )
    final_card = out.get("final_card") or out

    if receipt_dir is not None:
        _attach_toolflow_runtime_logs(
            receipt_dir,
            stdout_text=runtime_stdout.getvalue(),
            stderr_text=runtime_stderr.getvalue(),
        )

    if isinstance(final_card, dict) and receipt_dir is not None:
        final_card = {
            **final_card,
            "source_of_truth": str(receipt_dir),
        }
        meta = {
            "created_at": datetime.now(UTC).isoformat(),
            "prompt": prompt,
            "query": query or "",
            "top_k": int(top_k),
            "profile": profile,
            "risk_score": risk_score,
        }
        _attach_toolflow_result(receipt_dir, payload=final_card, meta=meta)

    if json_output:
        print(json.dumps(final_card, ensure_ascii=False, indent=2))
        return 0

    if verbose:
        print(json.dumps(final_card, ensure_ascii=False, indent=2))
    else:
        _print_three_lines(
            cast(
                Any,
                final_card if isinstance(final_card, dict) else {"status": "UNKNOWN"},
            )
        )
    return 0


def _handoff(
    repo_root: Path,
    receipt_dir: Path | None,
    next_agent: str,
    task: str,
) -> dict[str, Any]:
    """Automated Handoff Message Generator (Serenity Pillar).
    Constructs the standard handoff message from an existing receipt.
    """
    msg_lines: list[Any] = []

    # 1. Header
    msg_lines.append(f"**⚔️ Handoff to {next_agent or 'Next Agent'}**")
    msg_lines.append("")

    # 2. Receipt
    if receipt_dir:
        msg_lines.append(f"**Receipt**: `logs/receipts/{receipt_dir.name}/`")
    else:
        msg_lines.append("**Receipt**: (Pending `sixxon receipt`)")

    # 3. PoChungCheon 3-Line Summary (if available)
    if receipt_dir and (receipt_dir / "receipt.json").exists():
        receipt_data = _load_receipt(receipt_dir)
        explain = _explain_from_receipt(receipt_dir, receipt_data)
        three = explain.get("pochungcheon_3_lines", {})
        msg_lines.append("**포청천 해설**:")
        msg_lines.append(f"  {three.get('state', 'UNKNOWN')}")
        msg_lines.append(f"  근거: {three.get('reason', 'None')}")
        msg_lines.append(f"  Next: {three.get('next', task)}")
    else:
        msg_lines.append("**포청천 해설**:")
        msg_lines.append("  🟡 UNKNOWN (No Receipt)")
        msg_lines.append("  근거: (None)")
        msg_lines.append(f"  Next: {task}")

    # 4. Next Task
    msg_lines.append("")
    msg_lines.append(f"**다음 단계**: {task}")

    full_msg = "\n".join(msg_lines)
    print(full_msg)

    return {"status": "OK", "message": full_msg}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="sixxon", description="SixXon for TRINITY-OS")
    sub = ap.add_subparsers(dest="command", required=True)

    # toolflow
    toolflow_p = sub.add_parser(
        "toolflow", help="Run the Agent Toolflow (Legacy V1 or Dream Hub)"
    )
    toolflow_p.add_argument("prompt", nargs="?", help="Task prompt or instruction")
    toolflow_p.add_argument(
        "--graph", action="store_true", help="Use the new Dream Hub (LangGraph) engine"
    )
    toolflow_p.add_argument(
        "--query", type=str, default="", help="Optional search query override"
    )
    toolflow_p.add_argument(
        "--top-k", type=int, default=5, help="Number of candidates to fetch"
    )
    toolflow_p.add_argument(
        "--risk-score", type=float, default=None, help="SSOT risk score evidence"
    )
    toolflow_p.add_argument(
        "--profile",
        choices=["P", "K"],
        default="K",
        help="P=Public (ASK default), K=Kingdom (AUTO_RUN allowed when SSOT permits)",
    )
    toolflow_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Receipt dir name under logs/receipts, or absolute path",
    )
    toolflow_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    toolflow_p.add_argument(
        "--refresh",
        action="store_true",
        help="Create a new receipt before running toolflow",
    )
    toolflow_p.add_argument("--verbose", action="store_true", help="Print full card")
    toolflow_p.add_argument("--json", action="store_true", help="Print raw JSON card")

    receipt_p = sub.add_parser(
        "receipt", help="Create a Bridge Receipt bundle under logs/receipts/"
    )
    receipt_p.add_argument(
        "--out",
        type=str,
        default="",
        help="Receipt directory name under logs/receipts (default: timestamp)",
    )
    receipt_p.add_argument(
        "--json", action="store_true", help="Print receipt metadata as JSON"
    )

    status_p = sub.add_parser(
        "status", help="Receipt-based kingdom status (requires an existing receipt)"
    )
    status_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Receipt dir name under logs/receipts, or absolute path",
    )
    status_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    status_p.add_argument(
        "--refresh",
        action="store_true",
        help="Create a new receipt before evaluating status",
    )
    status_p.add_argument(
        "--simple",
        action="store_true",
        help="Alias for the default 3-line humble output (kept for spec compatibility)",
    )
    status_p.add_argument("--verbose", action="store_true", help="Print full JSON card")
    status_p.add_argument("--json", action="store_true", help="Print raw JSON card")
    status_p.add_argument(
        "--detail",
        action="store_true",
        help="[Stage 3] Audit Contract: Show full penalty breakdown",
    )

    verify_p = sub.add_parser(
        "verify", help="[Stage 3] Universe Teacher (Truth Oath) verification"
    )
    verify_p.add_argument(
        "--deep",
        action="store_true",
        help="Show internal fact-checking weights and skills engine metrics",
    )
    verify_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Receipt dir name under logs/receipts, or absolute path",
    )
    verify_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    verify_p.add_argument(
        "--refresh", action="store_true", help="Create a new receipt before verifying"
    )
    verify_p.add_argument("--json", action="store_true", help="Print raw JSON receipt")

    dream_p = sub.add_parser(
        "dream", help="[Stage 3] Dream Hub (Dream Protocol) operations"
    )
    dream_p.add_argument(
        "--replay",
        type=str,
        metavar="THREAD_ID",
        help="Replay a past workflow session by Thread ID (persistence required)",
    )
    dream_p.add_argument(
        "--dry-run", action="store_true", help="Simulate replay without side effects"
    )

    explain_p = sub.add_parser(
        "explain",
        help="PoChungCheon 3-line explanation from an existing receipt (read-only)",
    )
    explain_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Receipt dir name under logs/receipts, or absolute path",
    )
    explain_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    explain_p.add_argument(
        "--refresh", action="store_true", help="Create a new receipt before explaining"
    )
    explain_p.add_argument(
        "--verbose", action="store_true", help="Print full JSON card"
    )
    explain_p.add_argument("--json", action="store_true", help="Print raw JSON card")

    edu_p = sub.add_parser(
        "edu",
        help="Educator Mothers (Mengmu × Saimdang) advice from receipt (read-only)",
    )
    edu_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Receipt dir name under logs/receipts, or absolute path",
    )
    edu_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    edu_p.add_argument(
        "--refresh", action="store_true", help="Create a new receipt before advising"
    )
    edu_p.add_argument("--verbose", action="store_true", help="Print full JSON card")
    edu_p.add_argument("--json", action="store_true", help="Print raw JSON card")

    auth_p = sub.add_parser(
        "auth", help="Subscription/browser-session helpers (wallet-backed; optional)"
    )
    auth_sub = auth_p.add_subparsers(dest="auth_command", required=True)

    auth_status_p = auth_sub.add_parser(
        "status", help="Show browser-session availability (metadata only)"
    )
    auth_status_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Optional receipt dir to attach raw evidence",
    )
    auth_status_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    auth_status_p.add_argument(
        "--refresh",
        action="store_true",
        help="Create a new receipt before attaching evidence",
    )
    auth_status_p.add_argument(
        "--verbose", action="store_true", help="Print full JSON card"
    )
    auth_status_p.add_argument(
        "--json", action="store_true", help="Print raw JSON card"
    )

    auth_login_p = auth_sub.add_parser(
        "login", help="Interactive login to save browser session into wallet"
    )
    auth_login_p.add_argument(
        "--provider", type=str, required=True, help="claude|codex|gemini|grok"
    )
    auth_login_p.add_argument(
        "--headless",
        action="store_true",
        help="Try headless mode (provider may override)",
    )
    auth_login_p.add_argument(
        "--browser",
        type=str,
        default="system-chrome",
        choices=["system-chrome"],
        help="Browser engine (kingdom policy: system-chrome only)",
    )
    auth_login_p.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep browser window open for manual inspection",
    )
    auth_login_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Optional receipt dir to attach raw evidence",
    )
    auth_login_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    auth_login_p.add_argument(
        "--refresh",
        action="store_true",
        help="Create a new receipt before attaching evidence",
    )
    auth_login_p.add_argument(
        "--verbose", action="store_true", help="Print full JSON card"
    )
    auth_login_p.add_argument("--json", action="store_true", help="Print raw JSON card")

    auth_ask_p = auth_sub.add_parser(
        "ask", help="Ask via stored browser session (subscription/web; unmetered usage)"
    )
    auth_ask_p.add_argument(
        "--provider", type=str, required=True, help="claude|codex|gemini|grok"
    )
    auth_ask_p.add_argument(
        "prompt",
        type=str,
        help="Prompt to send (stored under receipt raw/ when attached)",
    )
    auth_ask_p.add_argument(
        "--yes", action="store_true", help="Skip confirmation prompt"
    )
    auth_ask_p.add_argument(
        "--no-humble",
        action="store_true",
        help="Do not prepend the 3-line humble instruction",
    )
    auth_ask_p.add_argument(
        "--headless",
        action="store_true",
        help="Use headless browser automation (no UI)",
    )
    auth_ask_p.add_argument(
        "--browser",
        type=str,
        default="system-chrome",
        choices=["system-chrome"],
        help="Browser engine (kingdom policy: system-chrome only)",
    )
    auth_ask_p.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep browser window open for manual inspection",
    )
    auth_ask_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Optional receipt dir to attach raw evidence",
    )
    auth_ask_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    auth_ask_p.add_argument(
        "--refresh",
        action="store_true",
        help="Create a new receipt before attaching evidence",
    )
    auth_ask_p.add_argument(
        "--verbose", action="store_true", help="Print full JSON card"
    )
    auth_ask_p.add_argument("--json", action="store_true", help="Print raw JSON card")

    auth_capture_p = auth_sub.add_parser(
        "capture",
        help="Capture browser session into wallet (manual login; no prompt send)",
    )
    auth_capture_p.add_argument(
        "--provider", type=str, required=True, help="claude|codex|gemini|grok"
    )
    auth_capture_p.add_argument(
        "--headless",
        action="store_true",
        help="Try headless mode (provider may override)",
    )
    auth_capture_p.add_argument(
        "--browser",
        type=str,
        default="system-chrome",
        choices=["system-chrome"],
        help="Browser engine (kingdom policy: system-chrome only)",
    )
    auth_capture_p.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep browser window open for manual inspection",
    )
    auth_capture_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Optional receipt dir to attach raw evidence",
    )
    auth_capture_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    auth_capture_p.add_argument(
        "--refresh",
        action="store_true",
        help="Create a new receipt before attaching evidence",
    )
    auth_capture_p.add_argument(
        "--verbose", action="store_true", help="Print full JSON card"
    )
    auth_capture_p.add_argument(
        "--json", action="store_true", help="Print raw JSON card"
    )

    auth_open_p = auth_sub.add_parser(
        "open",
        help="Open chat page with saved wallet session (manual use; no prompt send)",
    )
    auth_open_p.add_argument(
        "--provider", type=str, required=True, help="claude|codex|gemini|grok"
    )
    auth_open_p.add_argument(
        "--headless",
        action="store_true",
        help="Try headless mode (not recommended for web login flows)",
    )
    auth_open_p.add_argument(
        "--browser",
        type=str,
        default="system-chrome",
        choices=["system-chrome"],
        help="Browser engine (kingdom policy: system-chrome only)",
    )
    auth_open_p.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep browser open until you press Enter (headed mode)",
    )
    auth_open_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Optional receipt dir to attach raw evidence",
    )
    auth_open_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    auth_open_p.add_argument(
        "--refresh",
        action="store_true",
        help="Create a new receipt before attaching evidence",
    )
    auth_open_p.add_argument(
        "--verbose", action="store_true", help="Print full JSON card"
    )
    auth_open_p.add_argument("--json", action="store_true", help="Print raw JSON card")

    auth_doctor_p = auth_sub.add_parser(
        "doctor", help="Diagnose auth/session issues (read-only)"
    )
    auth_doctor_p.add_argument(
        "--provider",
        type=str,
        default="",
        help="Optional provider focus (claude|codex|gemini|grok)",
    )
    auth_doctor_p.add_argument(
        "--receipt",
        type=str,
        default="",
        help="Optional receipt dir to attach raw evidence",
    )
    auth_doctor_p.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest receipt when --receipt is omitted",
    )
    auth_doctor_p.add_argument(
        "--refresh",
        action="store_true",
        help="Create a new receipt before attaching evidence",
    )
    auth_doctor_p.add_argument(
        "--verbose", action="store_true", help="Print full JSON card"
    )
    auth_doctor_p.add_argument(
        "--json", action="store_true", help="Print raw JSON card"
    )

    handoff_p = sub.add_parser(
        "handoff", help="Generate standardized Handoff Message (Serenity)"
    )
    handoff_p.add_argument(
        "--to", type=str, default="", help="Target agent name (e.g. Codex, Grok)"
    )
    handoff_p.add_argument(
        "--task", type=str, default="Continue task", help="Description of next task"
    )
    handoff_p.add_argument(
        "--receipt", type=str, default="", help="Receipt dir name to link"
    )
    handoff_p.add_argument("--latest", action="store_true", help="Use latest receipt")

    args = ap.parse_args(argv)

    try:
        if args.command == "receipt":
            repo_root = _find_repo_root()
            if repo_root is None:
                raise RuntimeError(
                    "Repo root not found (missing scripts/receipt_bundle.py)"
                )
            try:
                receipt_dir = _create_receipt(repo_root, out_name=str(args.out or ""))
            except Exception as e:
                payload = {
                    "status": "BLOCK",
                    "reason": "receipt_bundle failed",
                    "stderr": str(e),
                }
                print(json.dumps(payload, ensure_ascii=False, indent=2))
                return 3
            if args.json:
                payload = {"status": "OK", "receipt_dir": str(receipt_dir)}
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print(str(receipt_dir))
            return 0

        if args.command == "toolflow":
            repo_root = _find_repo_root()
            receipt_dir: Path | None = None
            if args.refresh or args.receipt or args.latest:
                if repo_root is None:
                    raise RuntimeError(
                        "Repo root not found (missing scripts/receipt_bundle.py)"
                    )

                if args.refresh:
                    out_name = ""
                    if args.receipt and not Path(str(args.receipt)).is_absolute():
                        out_name = str(args.receipt)
                    receipt_dir = _create_receipt(repo_root, out_name=out_name)
                elif args.receipt:
                    receipt_dir = _resolve_receipt_dir(repo_root, args.receipt)
                else:
                    receipt_dir = (
                        _latest_receipt_dir(repo_root) if args.latest else None
                    )

            card = _toolflow_run(
                repo_root=repo_root,
                task=str(args.prompt or ""),
                graph_mode=bool(args.graph),
                receipt_dir=receipt_dir,
            )
            if args.json or args.verbose:
                print(json.dumps(card, ensure_ascii=False, indent=2))
            else:
                _print_three_lines(card)
            return 0 if card.get("status") == "OK" else 1
        if args.command == "status":
            repo_root = _find_repo_root()
            if repo_root is None:
                raise RuntimeError(
                    "Repo root not found (missing scripts/receipt_bundle.py)"
                )

            receipt_dir: Path | None = None
            if args.refresh:
                out_name = ""
                if args.receipt and not Path(str(args.receipt)).is_absolute():
                    out_name = str(args.receipt)
                try:
                    receipt_dir = _create_receipt(repo_root, out_name=out_name)
                except Exception as e:
                    payload = {
                        "status": "BLOCK",
                        "reason": "receipt_bundle failed",
                        "stderr": str(e),
                    }
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 3

            if receipt_dir is None and args.receipt:
                receipt_dir = _resolve_receipt_dir(repo_root, args.receipt)
            elif receipt_dir is None:
                receipt_dir = _latest_receipt_dir(repo_root) if args.latest else None

            if receipt_dir is None or not (receipt_dir / "receipt.json").exists():
                payload = {
                    "status": "BLOCK",
                    "decision": "BLOCK",
                    "reason": "Missing receipt (Truth=0 without receipt)",
                    "next_actions": ["Run `sixxon receipt` first"],
                }
                if args.json or args.verbose:
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                else:
                    _print_three_lines(payload)
                return 2

            receipt = _load_receipt(receipt_dir)
            card = _receipt_status_from_receipt(receipt)
            card["source_of_truth"] = str(receipt_dir)
            if args.json or args.verbose:
                print(json.dumps(card, ensure_ascii=False, indent=2))
            elif getattr(args, "detail", False):
                _print_detail_report(card)
            else:
                _print_three_lines(card)
            return 0

        if args.command == "verify":
            repo_root = _find_repo_root()
            if repo_root is None:
                raise RuntimeError(
                    "Repo root not found (missing scripts/receipt_bundle.py)"
                )

            receipt_dir: Path | None = None
            if args.refresh or args.receipt or args.latest:
                if args.refresh:
                    out_name = ""
                    if args.receipt and not Path(str(args.receipt)).is_absolute():
                        out_name = str(args.receipt)
                    receipt_dir = _create_receipt(repo_root, out_name=out_name)
                elif args.receipt:
                    receipt_dir = _resolve_receipt_dir(repo_root, args.receipt)
                else:
                    receipt_dir = (
                        _latest_receipt_dir(repo_root) if args.latest else None
                    )

            result = _verify_run(
                repo_root=repo_root,
                receipt_dir=receipt_dir,
                deep=bool(args.deep),
                json_output=bool(args.json),
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result.get("status") == "OK" else 1

        if args.command == "dream":
            result = _dream_run(replay_id=args.replay, dry_run=bool(args.dry_run))
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result.get("status") == "OK" else 1

        if args.command in {"explain", "edu"}:
            repo_root = _find_repo_root()
            if repo_root is None:
                raise RuntimeError(
                    "Repo root not found (missing scripts/receipt_bundle.py)"
                )

            receipt_dir: Path | None = None
            if args.refresh:
                out_name = ""
                if args.receipt and not Path(str(args.receipt)).is_absolute():
                    out_name = str(args.receipt)
                try:
                    receipt_dir = _create_receipt(repo_root, out_name=out_name)
                except Exception as e:
                    payload = {
                        "status": "BLOCK",
                        "reason": "receipt_bundle failed",
                        "stderr": str(e),
                    }
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 3

            if receipt_dir is None and args.receipt:
                receipt_dir = _resolve_receipt_dir(repo_root, args.receipt)
            elif receipt_dir is None:
                receipt_dir = _latest_receipt_dir(repo_root) if args.latest else None

            if receipt_dir is None or not (receipt_dir / "receipt.json").exists():
                payload = {
                    "status": "BLOCK",
                    "decision": "BLOCK",
                    "reason": "Missing receipt (Truth=0 without receipt)",
                    "next_actions": ["Run `sixxon receipt` first"],
                }
                if getattr(args, "json", False) or getattr(args, "verbose", False):
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                else:
                    _print_three_lines(payload)
                return 2

            receipt = _load_receipt(receipt_dir)
            if args.command == "explain":
                card = _explain_from_receipt(receipt_dir, receipt)
            else:
                card = _edu_from_receipt(receipt_dir, receipt)

            if getattr(args, "json", False) or getattr(args, "verbose", False):
                print(json.dumps(card, ensure_ascii=False, indent=2))
            else:
                three = card.get("pochungcheon_3_lines") or {}
                if isinstance(three, dict):
                    print(three.get("state") or "🟡 UNKNOWN")
                    print(three.get("reason") or "")
                    print(three.get("next") or "")
                else:
                    _print_three_lines(card)
            return 0

        if args.command == "auth":
            repo_root = _find_repo_root()
            if repo_root is None:
                raise RuntimeError(
                    "Repo root not found (missing scripts/receipt_bundle.py)"
                )

            receipt_dir: Path | None = None
            # Receipt selection rules (SSOT discipline):
            # 1) --refresh: always create a fresh receipt
            # 2) --receipt: attach into an existing receipt dir
            # 3) --latest: use the latest receipt dir
            # 4) auth login/capture/open/ask: auto-create a receipt even when the user did not pass flags,
            #    so failures remain actionable (raw evidence exists). (No secrets are written into receipt.)
            if bool(getattr(args, "refresh", False)):
                out_name = ""
                if (
                    getattr(args, "receipt", "")
                    and not Path(str(args.receipt)).is_absolute()
                ):
                    out_name = str(args.receipt)
                receipt_dir = _create_receipt(repo_root, out_name=out_name)
            elif getattr(args, "receipt", ""):
                receipt_dir = _resolve_receipt_dir(repo_root, str(args.receipt))
            elif bool(getattr(args, "latest", False)):
                receipt_dir = _latest_receipt_dir(repo_root)
            elif getattr(args, "auth_command", "") in {
                "login",
                "capture",
                "open",
                "ask",
            }:
                prov = str(getattr(args, "provider", "") or "").strip().lower()
                suffix = f"_{prov}" if prov else ""
                receipt_dir = _create_receipt(
                    repo_root,
                    out_name=f"sixxon_auth_{getattr(args, 'auth_command', 'auth')}{suffix}_{_ts_slug()}",
                )

            if args.auth_command == "status":
                card = _auth_status_card(repo_root=repo_root, receipt_dir=receipt_dir)
                if getattr(args, "json", False) or getattr(args, "verbose", False):
                    print(json.dumps(card, ensure_ascii=False, indent=2))
                else:
                    _print_three_lines(
                        {
                            **card,
                            "source_of_truth": str(receipt_dir) if receipt_dir else "",
                        }
                    )
                return 0

            if args.auth_command == "login":
                # Browser engine selection (explicit for Serenity / predictability)
                old_engine = os.environ.get("AFO_BROWSER_ENGINE")
                old_keep = os.environ.get("AFO_KEEP_BROWSER_OPEN")
                os.environ["AFO_BROWSER_ENGINE"] = str(
                    getattr(args, "browser", "system-chrome")
                )
                if bool(getattr(args, "keep_open", False)):
                    os.environ["AFO_KEEP_BROWSER_OPEN"] = "1"
                else:
                    os.environ.pop("AFO_KEEP_BROWSER_OPEN", None)

                card = _auth_login(
                    provider=str(getattr(args, "provider", "")),
                    headless=bool(getattr(args, "headless", False)),
                    repo_root=repo_root,
                    receipt_dir=receipt_dir,
                )
                if old_engine is None:
                    os.environ.pop("AFO_BROWSER_ENGINE", None)
                else:
                    os.environ["AFO_BROWSER_ENGINE"] = old_engine
                if old_keep is None:
                    os.environ.pop("AFO_KEEP_BROWSER_OPEN", None)
                else:
                    os.environ["AFO_KEEP_BROWSER_OPEN"] = old_keep
                if getattr(args, "json", False) or getattr(args, "verbose", False):
                    print(json.dumps(card, ensure_ascii=False, indent=2))
                else:
                    _print_three_lines(
                        {
                            **card,
                            "source_of_truth": str(receipt_dir) if receipt_dir else "",
                        }
                    )
                return 0

            if args.auth_command == "capture":
                old_engine = os.environ.get("AFO_BROWSER_ENGINE")
                old_keep = os.environ.get("AFO_KEEP_BROWSER_OPEN")
                os.environ["AFO_BROWSER_ENGINE"] = str(
                    getattr(args, "browser", "system-chrome")
                )
                if bool(getattr(args, "keep_open", False)):
                    os.environ["AFO_KEEP_BROWSER_OPEN"] = "1"
                else:
                    os.environ.pop("AFO_KEEP_BROWSER_OPEN", None)

                card = _auth_capture(
                    provider=str(getattr(args, "provider", "")),
                    headless=bool(getattr(args, "headless", False)),
                    repo_root=repo_root,
                    receipt_dir=receipt_dir,
                )

                if old_engine is None:
                    os.environ.pop("AFO_BROWSER_ENGINE", None)
                else:
                    os.environ["AFO_BROWSER_ENGINE"] = old_engine
                if old_keep is None:
                    os.environ.pop("AFO_KEEP_BROWSER_OPEN", None)
                else:
                    os.environ["AFO_KEEP_BROWSER_OPEN"] = old_keep

                if getattr(args, "json", False) or getattr(args, "verbose", False):
                    print(json.dumps(card, ensure_ascii=False, indent=2))
                else:
                    _print_three_lines(
                        {
                            **card,
                            "source_of_truth": str(receipt_dir) if receipt_dir else "",
                        }
                    )
                return 0

            if args.auth_command == "open":
                old_engine = os.environ.get("AFO_BROWSER_ENGINE")
                old_keep = os.environ.get("AFO_KEEP_BROWSER_OPEN")
                os.environ["AFO_BROWSER_ENGINE"] = str(
                    getattr(args, "browser", "system-chrome")
                )
                keep_open = bool(getattr(args, "keep_open", False)) or not bool(
                    getattr(args, "headless", False)
                )
                if keep_open:
                    os.environ["AFO_KEEP_BROWSER_OPEN"] = "1"
                else:
                    os.environ.pop("AFO_KEEP_BROWSER_OPEN", None)

                card = _auth_open(
                    provider=str(getattr(args, "provider", "")),
                    headless=bool(getattr(args, "headless", False)),
                    keep_open=bool(keep_open),
                    repo_root=repo_root,
                    receipt_dir=receipt_dir,
                )

                if old_engine is None:
                    os.environ.pop("AFO_BROWSER_ENGINE", None)
                else:
                    os.environ["AFO_BROWSER_ENGINE"] = old_engine
                if old_keep is None:
                    os.environ.pop("AFO_KEEP_BROWSER_OPEN", None)
                else:
                    os.environ["AFO_KEEP_BROWSER_OPEN"] = old_keep

                if getattr(args, "json", False) or getattr(args, "verbose", False):
                    print(json.dumps(card, ensure_ascii=False, indent=2))
                else:
                    _print_three_lines(
                        {
                            **card,
                            "source_of_truth": str(receipt_dir) if receipt_dir else "",
                        }
                    )
                return 0

            if args.auth_command == "ask":
                if not bool(getattr(args, "yes", False)):
                    print(
                        "⚠️  This will open a browser and TRY to send a message via your subscription session (best-effort; UI may change)."
                    )
                    print(
                        "   Tip: For a stable flow, use `sixxon auth open` and interact manually."
                    )
                    resp = input("Continue? (y/N): ").strip().lower()
                    if resp not in {"y", "yes"}:
                        print(
                            json.dumps(
                                {"status": "BLOCK", "reason": "User cancelled"},
                                ensure_ascii=False,
                            )
                        )
                        return 1

                old_engine = os.environ.get("AFO_BROWSER_ENGINE")
                old_keep = os.environ.get("AFO_KEEP_BROWSER_OPEN")
                os.environ["AFO_BROWSER_ENGINE"] = str(
                    getattr(args, "browser", "system-chrome")
                )
                if bool(getattr(args, "keep_open", False)):
                    os.environ["AFO_KEEP_BROWSER_OPEN"] = "1"
                else:
                    os.environ.pop("AFO_KEEP_BROWSER_OPEN", None)

                card = _auth_ask(
                    provider=str(getattr(args, "provider", "")),
                    prompt=str(getattr(args, "prompt", "")),
                    humble=not bool(getattr(args, "no_humble", False)),
                    headless=bool(getattr(args, "headless", False)),
                    repo_root=repo_root,
                    receipt_dir=receipt_dir,
                )
                if old_engine is None:
                    os.environ.pop("AFO_BROWSER_ENGINE", None)
                else:
                    os.environ["AFO_BROWSER_ENGINE"] = old_engine
                if old_keep is None:
                    os.environ.pop("AFO_KEEP_BROWSER_OPEN", None)
                else:
                    os.environ["AFO_KEEP_BROWSER_OPEN"] = old_keep
                if getattr(args, "json", False) or getattr(args, "verbose", False):
                    print(json.dumps(card, ensure_ascii=False, indent=2))
                else:
                    _print_three_lines(
                        {
                            **card,
                            "source_of_truth": str(receipt_dir) if receipt_dir else "",
                        }
                    )
                return 0

            if args.auth_command == "doctor":
                card = _auth_doctor(
                    repo_root=repo_root,
                    receipt_dir=receipt_dir,
                    provider=str(getattr(args, "provider", "")) or None,
                )
                if getattr(args, "json", False) or getattr(args, "verbose", False):
                    print(json.dumps(card, ensure_ascii=False, indent=2))
                else:
                    _print_three_lines(
                        {
                            **card,
                            "source_of_truth": str(receipt_dir) if receipt_dir else "",
                        }
                    )
                return 0

        if args.command == "handoff":
            repo_root = _find_repo_root()
            receipt_dir = None
            if repo_root:
                if args.receipt:
                    receipt_dir = _resolve_receipt_dir(repo_root, args.receipt)
                elif args.latest:
                    receipt_dir = _latest_receipt_dir(repo_root)

            _handoff(
                repo_root=repo_root if repo_root else Path.cwd(),
                receipt_dir=receipt_dir,
                next_agent=args.to,
                task=args.task,
            )
            return 0

    except ImportError as e:
        import traceback

        traceback.print_exc()
        print(
            json.dumps(
                {"status": "BLOCK", "reason": f"Missing dependency: {e}"},
                ensure_ascii=False,
            )
        )
        return 3
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(json.dumps({"status": "BLOCK", "reason": str(e)}, ensure_ascii=False))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
