from __future__ import annotations

"""
TRINITY Graph Toolflow v1 (Thin Layer)

Search → Card → Gate → (DryRun?) → Execute

목적:
- MCP Tool Search + Programmatic Calling 흐름을 AFO에 맞게 얇게 조립한다.
- 점수/판정은 새로 만들지 않고, 기존 SSOT(Registry/Gate/Proxy)만 호출한다.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, TypedDict

Decision = Literal["AUTO_RUN", "ASK", "BLOCK"]


class Candidate(TypedDict, total=False):
    skill_id: str
    title: str
    score_hint: float | None
    tags: list[str] | None
    reason: str | None


class FlowState(TypedDict, total=False):
    user_prompt: str
    query: str
    top_k: int
    risk_score: float | None

    candidates: list[dict[str, Any]]
    selected_skill_id: str
    selected_title: str

    skill_card: dict[str, Any]
    decision: Decision
    gate_evidence: dict[str, Any]

    dry_run_supported: bool
    dry_run_result: dict[str, Any]
    exec_result: dict[str, Any]

    approval_packet: dict[str, Any]
    final_card: dict[str, Any]


@dataclass(frozen=True)
class Deps:
    """
    외부 의존성(실제 MCP/Registry/Gate/Proxy)을 얇게 주입받는 구조.

    - tool_search: 검색 결과 후보군 반환
    - get_skill_card: 단일 스킬 카드 반환
    - serenity_gate_existing: AUTO_RUN/ASK/BLOCK 판정(기존 게이트)
    - execute_skill_proxy: DRY_RUN/EXECUTE 실행(기존 프록시)
    """

    tool_search: Callable[[str, int], dict[str, Any]]
    get_skill_card: Callable[[str], dict[str, Any]]
    serenity_gate_existing: Callable[[dict[str, Any]], dict[str, Any]]
    execute_skill_proxy: Callable[[str, dict[str, Any]], dict[str, Any]]


def _pick_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("candidates", "results", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return [v for v in value if isinstance(v, dict)]
    return []


def _normalize_decision(raw: Any) -> Decision:
    if raw in ("AUTO_RUN", "ASK", "BLOCK"):
        return raw
    return "ASK"


def _infer_dry_run_supported(skill_card: dict[str, Any]) -> bool:
    for key in ("dry_run_supported", "supports_dry_run"):
        value = skill_card.get(key)
        if isinstance(value, bool):
            return value
    # 기본은 DRY_RUN 지원으로 가정(안전 우선)
    return True


def node_tool_search(state: FlowState, deps: Deps) -> FlowState:
    user_prompt = state.get("user_prompt", "")
    query = state.get("query") or user_prompt
    top_k = int(state.get("top_k") or 5)
    out = deps.tool_search(query, top_k)
    candidates = _pick_candidates(out)
    return {**state, "query": query, "top_k": top_k, "candidates": candidates}


def node_select(state: FlowState, deps: Deps) -> FlowState:
    candidates = state.get("candidates") or []
    if not candidates:
        return {**state, "selected_skill_id": "", "selected_title": ""}

    best = candidates[0]
    skill_id = str(best.get("skill_id") or best.get("id") or best.get("name") or "")
    title = str(best.get("title") or best.get("name") or skill_id)
    return {**state, "selected_skill_id": skill_id, "selected_title": title}


def node_get_card(state: FlowState, deps: Deps) -> FlowState:
    skill_id = state.get("selected_skill_id") or ""
    card = deps.get_skill_card(skill_id) if skill_id else {}
    dry_run_supported = _infer_dry_run_supported(card)
    return {**state, "skill_card": card, "dry_run_supported": dry_run_supported}


def node_serenity_gate(state: FlowState, deps: Deps) -> FlowState:
    payload = {
        "user_prompt": state.get("user_prompt", ""),
        "skill_id": state.get("selected_skill_id") or "",
        "skill_card": state.get("skill_card") or {},
    }
    risk_score = state.get("risk_score")
    if isinstance(risk_score, (int, float)):
        payload["risk_score"] = float(risk_score)
    out = deps.serenity_gate_existing(payload) or {}
    decision = _normalize_decision(out.get("decision") or out.get("mode"))
    return {**state, "decision": decision, "gate_evidence": out}


def node_dry_run(state: FlowState, deps: Deps) -> FlowState:
    skill_id = state.get("selected_skill_id") or ""
    args = {
        "mode": "dry_run",
        "skill_card": state.get("skill_card") or {},
        "user_prompt": state.get("user_prompt", ""),
    }
    out = deps.execute_skill_proxy(skill_id, args) if skill_id else {}
    return {**state, "dry_run_result": out}


def node_execute(state: FlowState, deps: Deps) -> FlowState:
    skill_id = state.get("selected_skill_id") or ""
    args = {
        "mode": "execute",
        "skill_card": state.get("skill_card") or {},
        "user_prompt": state.get("user_prompt", ""),
    }
    out = deps.execute_skill_proxy(skill_id, args) if skill_id else {}
    return {**state, "exec_result": out}


def node_ask(state: FlowState, deps: Deps) -> FlowState:
    skill_id = state.get("selected_skill_id") or ""
    title = state.get("selected_title") or skill_id
    card = state.get("skill_card") or {}

    approval_packet = {
        "skill_id": skill_id,
        "title": title,
        "why_this": card.get("purpose") or card.get("description") or "",
        "required_inputs": card.get("input_schema") or card.get("inputs") or {},
        "proposed_args": {},
        "risk_notes": card.get("risk_notes") or card.get("permissions") or [],
        "rollback": card.get("rollback") or "No-op",
        "choices": ["Approve & Execute", "Edit Inputs", "Cancel"],
    }
    gate_evidence = state.get("gate_evidence") or {}
    final_card = {
        "status": "ASK",
        "approval_packet": approval_packet,
        "gate_evidence": gate_evidence,
    }
    return {
        **state,
        "approval_packet": approval_packet,
        "final_card": final_card,
    }


def node_final_block(state: FlowState, deps: Deps) -> FlowState:
    skill_id = state.get("selected_skill_id") or ""
    title = state.get("selected_title") or skill_id
    gate_evidence = state.get("gate_evidence") or {}
    final_card = {
        "status": "BLOCK",
        "skill_id": skill_id,
        "title": title,
        "reason": "Blocked by Serenity Gate",
        "next_actions": ["Revise prompt", "Run tool_search with tighter query"],
        "gate_evidence": gate_evidence,
    }
    return {**state, "final_card": final_card}


def node_final_no_candidates(state: FlowState, deps: Deps) -> FlowState:
    gate_evidence = state.get("gate_evidence") or {}
    final_card = {
        "status": "NO_CANDIDATES",
        "query": state.get("query") or "",
        "next_actions": ["Try different keywords", "Increase top_k"],
        "gate_evidence": gate_evidence,
    }
    return {**state, "final_card": final_card}


def node_final_ok(state: FlowState, deps: Deps) -> FlowState:
    skill_id = state.get("selected_skill_id") or ""
    title = state.get("selected_title") or skill_id
    gate_evidence = state.get("gate_evidence") or {}
    exec_result = state.get("exec_result") or {}
    dry_run_result = state.get("dry_run_result") or {}

    ok_flag = exec_result.get("ok")
    code = exec_result.get("code")
    exec_failed = (ok_flag is False) or (isinstance(code, int) and code != 0)

    if exec_failed:
        reason = "Execution failed"
        if isinstance(code, int):
            reason = f"{reason} (code={code})"
        final_card = {
            "status": "BLOCK",
            "skill_id": skill_id,
            "title": title,
            "decision": "BLOCK",
            "reason": reason,
            "next_actions": ["Open logs", "Retry with ASK", "Run health checks"],
            "dry_run_result": dry_run_result,
            "exec_result": exec_result,
            "gate_evidence": gate_evidence,
        }
        return {**state, "final_card": final_card}

    final_card = {
        "status": "OK",
        "skill_id": skill_id,
        "title": title,
        "decision": state.get("decision") or "AUTO_RUN",
        "summary": "Tool Search → Card → Gate → Execute",
        "next_actions": ["Run another tool_search", "Save to SSOT", "Open logs"],
        "dry_run_result": dry_run_result,
        "exec_result": exec_result,
        "gate_evidence": gate_evidence,
    }
    return {**state, "final_card": final_card}


def build_trinity_toolflow_graph(deps: Deps):
    """
    LangGraph로 Toolflow를 컴파일한다.
    LangGraph가 없는 환경이면 ImportError를 올려 호출자가 처리하도록 한다.
    """
    from langgraph.graph import END, StateGraph

    graph = StateGraph(FlowState)
    graph.add_node("TOOL_SEARCH", lambda s: node_tool_search(s, deps))
    graph.add_node("SELECT", lambda s: node_select(s, deps))
    graph.add_node("GET_CARD", lambda s: node_get_card(s, deps))
    graph.add_node("SERENITY_GATE", lambda s: node_serenity_gate(s, deps))
    graph.add_node("DRY_RUN", lambda s: node_dry_run(s, deps))
    graph.add_node("EXECUTE", lambda s: node_execute(s, deps))
    graph.add_node("ASK", lambda s: node_ask(s, deps))
    graph.add_node("FINAL_BLOCK", lambda s: node_final_block(s, deps))
    graph.add_node("FINAL_NO_CANDIDATES", lambda s: node_final_no_candidates(s, deps))
    graph.add_node("FINAL_OK", lambda s: node_final_ok(s, deps))

    graph.set_entry_point("TOOL_SEARCH")
    graph.add_edge("TOOL_SEARCH", "SELECT")

    def route_after_select(state: FlowState) -> str:
        return (
            "FINAL_NO_CANDIDATES"
            if not (state.get("selected_skill_id") or "")
            else "GET_CARD"
        )

    graph.add_conditional_edges(
        "SELECT",
        route_after_select,
        {"FINAL_NO_CANDIDATES": "FINAL_NO_CANDIDATES", "GET_CARD": "GET_CARD"},
    )

    graph.add_edge("GET_CARD", "SERENITY_GATE")

    def route_after_gate(state: FlowState) -> str:
        decision = state.get("decision") or "ASK"
        if decision == "BLOCK":
            return "FINAL_BLOCK"
        if decision == "ASK":
            return "ASK"
        return "DRY_RUN" if bool(state.get("dry_run_supported", True)) else "EXECUTE"

    graph.add_conditional_edges(
        "SERENITY_GATE",
        route_after_gate,
        {
            "FINAL_BLOCK": "FINAL_BLOCK",
            "ASK": "ASK",
            "DRY_RUN": "DRY_RUN",
            "EXECUTE": "EXECUTE",
        },
    )

    graph.add_edge("DRY_RUN", "EXECUTE")
    graph.add_edge("EXECUTE", "FINAL_OK")

    graph.add_edge("ASK", END)
    graph.add_edge("FINAL_BLOCK", END)
    graph.add_edge("FINAL_NO_CANDIDATES", END)
    graph.add_edge("FINAL_OK", END)

    return graph.compile()


def run_trinity_toolflow(
    app,
    user_prompt: str,
    *,
    query: str | None = None,
    top_k: int = 5,
    risk_score: float | None = None,
) -> FlowState:
    init: FlowState = {"user_prompt": user_prompt, "top_k": int(top_k)}
    if query:
        init["query"] = query
    if risk_score is not None:
        init["risk_score"] = float(risk_score)
    return app.invoke(init)
