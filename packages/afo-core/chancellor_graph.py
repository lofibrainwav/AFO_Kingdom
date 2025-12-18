from typing import Annotated, Any, TypedDict

from langchain_core.messages import AIMessage, BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

# Import existing LLM Router logic for model execution
from llm_router import QualityTier, llm_router

# Antigravity 통합 (眞: 명시적 설정 전달)
try:
    from AFO.config.antigravity import antigravity
except ImportError:
    try:
        from config.antigravity import antigravity
    except ImportError:
        # Fallback: 기본값 사용
        class MockAntigravity:
            AUTO_DEPLOY = True
            DRY_RUN_DEFAULT = True
            ENVIRONMENT = "dev"
        antigravity = MockAntigravity()


# --- 1. State Definition (Chancellor's Memory - V2 Constitution) ---
class ChancellorState(TypedDict):
    # 1. 眞 (Truth): Persistent Message History (Auto-merge)
    messages: Annotated[list[BaseMessage], add_messages]

    # 2. 眞/善 (Metrics): Decision Basis
    trinity_score: float  # Current Trinity Score
    risk_score: float  # Current Risk Score

    # 3. 孝 (Serenity): Auto-Run Eligibility
    auto_run_eligible: bool  # If True, bypass human approval

    # 4. 天 (Context): External Environment
    kingdom_context: dict[str, Any]  # e.g. Family status, verification results

    # 5. 永 (Memory): Long-term Memory
    persistent_memory: dict[str, Any]

    # Operational fields
    current_speaker: str  # "user", "chancellor", "jegalryang", "samaui", "juyu"
    next_step: str  # Next node to visit
    analysis_results: dict[str, str]  # Store individual strategist outputs


# --- 2. Node Definitions (The Personas) ---


def chancellor_router_node(state: ChancellorState):
    """
    [Chancellor Node]
    The Supreme Orchestrator.
    Decides which Strategist should speak next or if the final answer is ready.
    
    Antigravity 통합: DRY_RUN 모드 감지 및 auto_run_eligible 조정
    """
    print("👑 [Chancellor] Analyzing state...")
    messages = state["messages"]
    messages[-1]

    # Antigravity 설정 확인 (kingdom_context에서 가져오거나 전역 설정 사용)
    context = state.get("kingdom_context", {}) or {}
    antigravity_config = context.get("antigravity", {})
    is_dry_run = antigravity_config.get("DRY_RUN_DEFAULT", antigravity.DRY_RUN_DEFAULT)
    
    # DRY_RUN 모드일 때는 auto_run_eligible을 False로 강제 (善: 안전 우선)
    if is_dry_run and state.get("auto_run_eligible", False):
        print("🛡️ [Chancellor] DRY_RUN 모드 감지 - auto_run_eligible을 False로 조정 (善)")
        state["auto_run_eligible"] = False

    # Simple heuristic routing for now (Upgrade to LLM-based later)
    # If this is the start (Human message), we might want to trigger all three or specific ones.
    # For V1, let's trigger Jegalryang (Truth) first if no analysis exists.

    analysis = state.get("analysis_results", {})

    strategist_order = context.get("strategist_order") or ["jegalryang", "samaui", "juyu"]
    max_strategists = context.get("max_strategists")
    try:
        max_n = int(max_strategists) if max_strategists is not None else len(strategist_order)
    except Exception:
        max_n = len(strategist_order)

    strategist_order = list(strategist_order)[: max(0, min(3, max_n))]

    # Visit strategists in requested order, up to max_strategists.
    for strategist in strategist_order:
        if strategist not in analysis:
            return {"next_step": strategist, "current_speaker": "chancellor"}

    # If all requested strategists have spoken, Chancellor synthesizes the final answer.
    return {"next_step": "finalize", "current_speaker": "chancellor"}


async def jegalryang_node(state: ChancellorState):
    """
    [Jegalryang Node] - Truth (矛)
    Focus: Architecture, Strategy, Technical Certainty.
    """
    print("⚔️ [Jegalryang] Analyzing Truth...")
    query = state["messages"][-1].content

    # Use LLM Router to call a "Smart" model (Truth requires intelligence)
    # Context can be passed to select specific persona prompts if we had them loaded here.
    # For now, we simulate the persona via system context augmentation in a real implementation.

    # In a full implementation, we would inject the System Prompt from TRINITY-OS/docs/personas/STRATEGIST_JEGALRYANG.md
    base_context = (state.get("kingdom_context") or {}).get("llm_context") or {}
    context = {
        **base_context,
        "quality_tier": base_context.get("quality_tier", QualityTier.PREMIUM),
        "max_tokens": base_context.get("max_tokens", 512),
    }

    response_data = await llm_router.execute_with_routing(
        f"당신은 제갈량(Truth)입니다. 다음 질문을 기술적/구조적 관점에서 분석하시오: {query}",
        context=context,
    )

    content = response_data.get("response", "분석 실패")

    return {
        "analysis_results": {**state.get("analysis_results", {}), "jegalryang": content},
        "messages": [AIMessage(content=f"[제갈량] {content}", name="jegalryang")],
    }


async def samaui_node(state: ChancellorState):
    """
    [Samaui Node] - Goodness (盾)
    Focus: Ethics, Stability, Risk Management.
    """
    print("🛡️ [Samaui] Checking Risks...")
    query = state["messages"][0].content  # Analyze original query
    truth_analysis = state["analysis_results"].get("jegalryang", "")

    base_context = (state.get("kingdom_context") or {}).get("llm_context") or {}
    context = {
        **base_context,
        "quality_tier": base_context.get("quality_tier", QualityTier.STANDARD),
        "max_tokens": base_context.get("max_tokens", 512),
    }

    response_data = await llm_router.execute_with_routing(
        f"당신은 사마의(Goodness)입니다. 제갈량의 분석('{truth_analysis[:200]}...')과 원본 질문('{query}')을 보고 윤리적/안전 리스크를 검토하시오.",
        context=context,
    )

    content = response_data.get("response", "검토 실패")

    return {
        "analysis_results": {**state.get("analysis_results", {}), "samaui": content},
        "messages": [AIMessage(content=f"[사마의] {content}", name="samaui")],
    }


async def juyu_node(state: ChancellorState):
    """
    [Juyu Node] - Beauty (橋)
    Focus: Narrative, UX, User Experience.
    """
    print("🌉 [Juyu] Polishing UX...")
    state["messages"][0].content
    truth = state["analysis_results"].get("jegalryang", "")
    goodness = state["analysis_results"].get("samaui", "")

    base_context = (state.get("kingdom_context") or {}).get("llm_context") or {}
    context = {
        **base_context,
        "quality_tier": base_context.get("quality_tier", QualityTier.PREMIUM),
        "max_tokens": base_context.get("max_tokens", 512),
    }

    response_data = await llm_router.execute_with_routing(
        f"당신은 주유(Beauty)입니다. 기술({truth[:100]}...)과 안전({goodness[:100]}...)을 종합하여 사용자에게 가장 아름답고 쉬운 서사로 정리하시오.",
        context=context,
    )

    content = response_data.get("response", "정리 실패")

    return {
        "analysis_results": {**state.get("analysis_results", {}), "juyu": content},
        "messages": [AIMessage(content=f"[주유] {content}", name="juyu")],
    }


async def chancellor_finalize_node(state: ChancellorState):
    """
    [Finalize]
    Chancellor synthesizes the final report.
    """
    print("👑 [Chancellor] Synthesizing Final Report...")
    analysis = state["analysis_results"]

    # Only include available analyses (graph may be configured to consult fewer strategists).
    parts: list[str] = [
        "당신은 승상(Chancellor)입니다. 책사의 의견을 종합하여 최종 보고를 하시오.",
        "가장 중요한 것은 사령관의 평온(孝)입니다.",
    ]
    if analysis.get("jegalryang"):
        parts.append(f"[제갈량]: {analysis.get('jegalryang')}")
    if analysis.get("samaui"):
        parts.append(f"[사마의]: {analysis.get('samaui')}")
    if analysis.get("juyu"):
        parts.append(f"[주유]: {analysis.get('juyu')}")
    final_prompt = "\n\n".join(parts)

    base_context = (state.get("kingdom_context") or {}).get("llm_context") or {}
    context = {
        **base_context,
        "quality_tier": base_context.get("quality_tier", QualityTier.ULTRA),
        "max_tokens": base_context.get("max_tokens", 768),
    }

    response_data = await llm_router.execute_with_routing(final_prompt, context=context)

    content = response_data.get("response", "종합 실패")

    return {"messages": [AIMessage(content=content, name="chancellor")]}


# --- 3. Graph Construction ---


def build_chancellor_graph():
    workflow = StateGraph(ChancellorState)

    # Add Nodes
    workflow.add_node("chancellor", chancellor_router_node)
    workflow.add_node("jegalryang", jegalryang_node)
    workflow.add_node("samaui", samaui_node)
    workflow.add_node("juyu", juyu_node)
    workflow.add_node("finalize", chancellor_finalize_node)

    # Add Edges
    workflow.set_entry_point("chancellor")

    # Conditional Edge from Chancellor
    def route_logic(state):
        return state["next_step"]

    workflow.add_conditional_edges(
        "chancellor",
        route_logic,
        {"jegalryang": "jegalryang", "samaui": "samaui", "juyu": "juyu", "finalize": "finalize"},
    )

    # Strategies return to Chancellor
    workflow.add_edge("jegalryang", "chancellor")
    workflow.add_edge("samaui", "chancellor")
    workflow.add_edge("juyu", "chancellor")
    workflow.add_edge("finalize", END)

    # Persistence Strategy (Dev: Memory, Prod: Postgres)
    # Using MemorySaver for current verification as per V2 Constitution (Dev Mode)
    checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)


# Singleton Instance
chancellor_graph = build_chancellor_graph()
