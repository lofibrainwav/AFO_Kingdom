from __future__ import annotations

import importlib
import inspect
import json
import os
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


def _maybe_import(mod: str):
    try:
        return importlib.import_module(mod)
    except Exception:
        return None


def _call_flex(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    try:
        return fn(*args, **kwargs)
    except TypeError:
        pass
    try:
        return fn(*args)
    except TypeError:
        pass
    return fn(**kwargs)


def _normalize_candidates(items: Any) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        return []
    out: list[dict[str, Any]] = []
    for it in items:
        if isinstance(it, dict):
            sid = str(it.get("skill_id") or it.get("id") or it.get("name") or "")
            title = str(it.get("title") or it.get("name") or sid)
            out.append({"skill_id": sid, "title": title, **it})
    return out


def _pick_list(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("candidates", "results", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return _normalize_candidates(value)
    return []


def _find_registry() -> Any:
    mod = _maybe_import("afo_soul_engine.afo_skills_registry")
    if mod is None:
        raise RuntimeError("Cannot import afo_soul_engine.afo_skills_registry")

    for name in ("SKILLS_REGISTRY", "skills_registry", "registry"):
        v = getattr(mod, name, None)
        if v is not None:
            return v

    classes: list[tuple[str, Any]] = []
    for n, obj in vars(mod).items():
        if inspect.isclass(obj) and "Registry" in n:
            classes.append((n, obj))
    for _, cls in classes:
        try:
            return cls()
        except Exception:
            continue

    raise RuntimeError("Could not construct a Skills Registry from afo_soul_engine.afo_skills_registry")


def _resolve_fn(mod, names: list[str]) -> Callable[..., Any] | None:
    if mod is None:
        return None
    for name in names:
        fn = getattr(mod, name, None)
        if callable(fn):
            return fn
    return None


def build_deps_v1():
    """AFO Ultimate MCP / Skills Registry를 실제 함수로 연결한 Deps 빌더.

    - MCP 서버가 직접 import 가능하면 그 함수를 우선 사용.
    - 불가하면 Skills Registry fallback 사용.
    """
    from trinity_os.graphs.trinity_toolflow_graph_v1 import Deps

    mcp_mod = _maybe_import("mcp_servers.afo_ultimate_mcp_server")

    try:
        registry = _find_registry()
    except Exception:
        registry = None

    mcp_tool_search = _resolve_fn(mcp_mod, ["tool_search", "search_tools", "search_tool"])
    mcp_get_card = _resolve_fn(mcp_mod, ["get_skill_card", "skill_card", "get_card"])
    mcp_exec = _resolve_fn(mcp_mod, ["execute_skill_proxy", "execute_skill", "run_skill"])

    def tool_search(query: str, top_k: int) -> dict[str, Any]:
        if mcp_tool_search is not None:
            out = _call_flex(mcp_tool_search, query=query, top_k=top_k)
            if isinstance(out, dict):
                return {"candidates": _pick_list(out)}
        if registry is None:
            return {"candidates": []}

        for meth in ("search", "search_skills", "search_registry", "filter", "find"):
            fn = getattr(registry, meth, None)
            if callable(fn):
                try:
                    out = _call_flex(fn, query=query, top_k=top_k)
                    if isinstance(out, dict):
                        return {"candidates": _pick_list(out)}
                    if isinstance(out, list):
                        return {"candidates": _normalize_candidates(out)}
                except Exception:
                    continue
        return {"candidates": []}

    def get_skill_card(skill_id: str) -> dict[str, Any]:
        if mcp_get_card is not None:
            out = _call_flex(mcp_get_card, skill_id=skill_id)
            if isinstance(out, dict):
                return out
        if registry is None:
            return {}
        for meth in ("get_skill_card", "get_card", "get", "get_skill"):
            fn = getattr(registry, meth, None)
            if callable(fn):
                out = _call_flex(fn, skill_id) if meth in ("get", "get_skill") else _call_flex(fn, skill_id=skill_id)
                if isinstance(out, dict):
                    return out
        return {}

    def serenity_gate_existing(payload: dict[str, Any]) -> dict[str, Any]:
        force = os.environ.get("TRINITY_TOOLFLOW_FORCE_DECISION")
        if force in ("AUTO_RUN", "ASK", "BLOCK"):
            return {"decision": force}

        def _load_latest_trinity_score() -> tuple[float | None, datetime | None, str | None]:
            """SSOT 기반 Trinity 점수 로딩:
            - logs/trinity_health_*.json 중 "미래가 아닌" 최신 기록에서 overall_trinity_score를 읽는다.
            - 없거나 파싱 실패 시 None.
            """
            log_dir = Path(os.environ.get("AFO_TRINITY_LOG_DIR", "logs"))
            if not log_dir.exists():
                return None, None, None
            files = list(log_dir.glob("trinity_health_*.json"))
            if not files:
                return None, None, None

            now_utc = datetime.now(UTC)
            local_tz = datetime.now().astimezone().tzinfo

            best_score: float | None = None
            best_ts: datetime | None = None
            best_path: str | None = None

            # 1) timestamp(파일 내용)이 신뢰 가능하고 "미래가 아닌" 항목 중 최신을 우선
            # 2) timestamp가 없거나 파싱 실패면 파일 mtime(UTC)로 대체
            for p in files:
                ts_from_file = datetime.fromtimestamp(p.stat().st_mtime, tz=UTC)
                ts = ts_from_file
                score: float | None = None
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                except Exception:
                    data = None
                if isinstance(data, dict):
                    raw_score = data.get("overall_trinity_score")
                    if isinstance(raw_score, (int, float)):
                        score = float(raw_score)
                    ts_raw = data.get("timestamp")
                    if isinstance(ts_raw, str):
                        try:
                            parsed = datetime.fromisoformat(ts_raw)
                            if parsed.tzinfo is None and local_tz is not None:
                                parsed = parsed.replace(tzinfo=local_tz)
                            if parsed.tzinfo is not None:
                                ts = parsed.astimezone(UTC)
                        except Exception:
                            ts = ts_from_file

                if score is None:
                    continue

                # "미래 timestamp"는 AUTO_RUN 근거로 쓰지 않기 위해 후보에서 제외
                # (로컬/UTC 오차를 감안해 2분은 허용)
                if ts > (now_utc + timedelta(minutes=2)):
                    continue

                if best_ts is None or ts > best_ts:
                    best_score = score
                    best_ts = ts
                    best_path = str(p)

            if best_score is not None:
                return best_score, best_ts, best_path

            # 후보가 전부 미래/손상인 경우: mtime 기준 최신을 반환(단, 신선도 체크에서 stale 처리)
            latest_by_mtime = max(files, key=lambda x: x.stat().st_mtime)
            try:
                data = json.loads(latest_by_mtime.read_text(encoding="utf-8"))
            except Exception:
                return None, None, str(latest_by_mtime)
            score = data.get("overall_trinity_score")
            ts = datetime.fromtimestamp(latest_by_mtime.stat().st_mtime, tz=UTC)
            if isinstance(score, (int, float)):
                return float(score), ts, str(latest_by_mtime)
            return None, ts, str(latest_by_mtime)

        for mod_name, fn_names in (
            (
                "afo_soul_engine.serenity_decision_engine",
                ["serenity_gate", "decide", "decide_mode"],
            ),
            ("afo_soul_engine.health.serenity_gate", ["serenity_gate", "decide"]),
            ("afo_soul_engine.trinity_gate", ["serenity_gate", "decide"]),
        ):
            mod = _maybe_import(mod_name)
            fn = _resolve_fn(mod, fn_names)
            if fn is not None:
                try:
                    out = _call_flex(fn, payload)
                except Exception:
                    out = None
                if isinstance(out, dict) and (out.get("decision") or out.get("mode")):
                    return out

        # --- SSOT Serenity Gate fallback (Quantum Balance Lock) ---
        qbl_mod = _maybe_import("afo_soul_engine.core.quantum_balance_lock")
        get_gate_verdict = _resolve_fn(qbl_mod, ["get_gate_verdict"])
        should_auto_run = _resolve_fn(qbl_mod, ["should_auto_run"])

        total_score, ts, src = _load_latest_trinity_score()
        if total_score is None or get_gate_verdict is None:
            return {
                "decision": "ASK",
                "reason": "No valid Trinity score evidence",
                "source": src,
            }

        # 점수의 신선도(Health First): 오래된 스코어는 AUTO_RUN 근거로 쓰지 않는다.
        max_age_min = int(os.environ.get("TRINITY_TOOLFLOW_MAX_SCORE_AGE_MINUTES", "60"))
        is_stale = False
        if ts is not None:
            age_min = (datetime.now(UTC) - ts).total_seconds() / 60.0
            # 미래 timestamp는 stale로 간주(시간 불일치/조작 방지)
            is_stale = True if age_min < -1.0 else age_min > float(max_age_min)

        gate_status = None
        try:
            gate_status = _call_flex(get_gate_verdict, total_score=total_score)
        except Exception:
            gate_status = None

        if gate_status == "BLOCK" or total_score < 80.0:
            return {
                "decision": "BLOCK",
                "gate_status": gate_status,
                "total_score": total_score,
                "source": src,
            }

        # Risk는 SSOT에서 오지 않으면 보수적으로 ‘unknown’ 처리
        risk_score = payload.get("risk_score")
        if not isinstance(risk_score, (int, float)):
            risk_score = 10.0  # unknown risk → AUTO_RUN 금지

        auto_run = False
        if should_auto_run is not None and not is_stale:
            try:
                auto_run = bool(
                    _call_flex(
                        should_auto_run,
                        workflow_name="TRINITY Toolflow",
                        total_score=total_score,
                        risk_score=float(risk_score),
                    )
                )
            except Exception:
                auto_run = False

        if auto_run:
            return {
                "decision": "AUTO_RUN",
                "gate_status": gate_status,
                "total_score": total_score,
                "risk_score": float(risk_score),
                "source": src,
            }

        return {
            "decision": "ASK",
            "gate_status": gate_status,
            "total_score": total_score,
            "risk_score": float(risk_score),
            "stale_score": is_stale,
            "source": src,
        }

    def execute_skill_proxy(skill_id: str, args: dict[str, Any]) -> dict[str, Any]:
        if mcp_exec is not None:
            for call_kwargs in (
                {"skill_id": skill_id, "params": args},
                {"skill_id": skill_id, "args": args},
            ):
                try:
                    out = _call_flex(mcp_exec, **call_kwargs)
                except Exception:
                    out = None
                if isinstance(out, dict):
                    return out

            try:
                out = _call_flex(mcp_exec, skill_id, args)
            except Exception:
                out = None
            if isinstance(out, dict):
                return out

        for mod_name, fn_names in (
            (
                "afo_soul_engine.skill_executor",
                ["execute_skill_proxy", "execute_skill", "run_skill"],
            ),
            (
                "afo_soul_engine.skills",
                ["execute_skill_proxy", "execute_skill", "run_skill"],
            ),
        ):
            mod = _maybe_import(mod_name)
            fn = _resolve_fn(mod, fn_names)
            if fn is not None:
                try:
                    out = _call_flex(fn, skill_id=skill_id, args=args)
                except Exception:
                    out = None
                if isinstance(out, dict):
                    return out

        return {
            "ok": False,
            "error": "execute_skill_proxy not found",
            "skill_id": skill_id,
            "args": args,
        }

    return Deps(
        tool_search=tool_search,
        get_skill_card=get_skill_card,
        serenity_gate_existing=serenity_gate_existing,
        execute_skill_proxy=execute_skill_proxy,
    )
