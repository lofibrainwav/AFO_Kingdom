from typing import Annotated, Any, TypedDict

from langchain_core.messages import AIMessage, BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

# Import existing LLM Router logic for model execution
from llm_router import QualityTier, llm_router


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
    """
    print("👑 [Chancellor] Analyzing state...")
    messages = state["messages"]
    messages[-1]

    # Simple heuristic routing for now (Upgrade to LLM-based later)
    # If this is the start (Human message), we might want to trigger all three or specific ones.
    # For V1, let's trigger Jegalryang (Truth) first if no analysis exists.

    analysis = state.get("analysis_results", {})

    # 1. If no Truth analysis, call Jegalryang
    if "jegalryang" not in analysis:
        return {"next_step": "jegalryang", "current_speaker": "chancellor"}

    # 2. If Truth exists but no Goodness, call Samaui
    if "samaui" not in analysis:
        return {"next_step": "samaui", "current_speaker": "chancellor"}

    # 3. If Truth & Goodness exist but no Beauty, call Juyu
    if "juyu" not in analysis:
        return {"next_step": "juyu", "current_speaker": "chancellor"}

    # 4. If all three have spoken, Chancellor synthesizes the final answer.
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
    response_data = await llm_router.execute_with_routing(
        f"당신은 제갈량(Truth)입니다. 다음 질문을 기술적/구조적 관점에서 분석하시오: {query}",
        context={"quality_tier": QualityTier.PREMIUM},
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

    response_data = await llm_router.execute_with_routing(
        f"당신은 사마의(Goodness)입니다. 제갈량의 분석('{truth_analysis[:200]}...')과 원본 질문('{query}')을 보고 윤리적/안전 리스크를 검토하시오.",
        context={"quality_tier": QualityTier.STANDARD},
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

    response_data = await llm_router.execute_with_routing(
        f"당신은 주유(Beauty)입니다. 기술({truth[:100]}...)과 안전({goodness[:100]}...)을 종합하여 사용자에게 가장 아름답고 쉬운 서사로 정리하시오.",
        context={"quality_tier": QualityTier.PREMIUM},
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

    final_prompt = f"""
    당신은 승상(Chancellor)입니다. 3책사의 의견을 종합하여 최종 보고를 하시오.
    가장 중요한 것은 사령관의 평온(孝)입니다.

    [제갈량]: {analysis.get("jegalryang")}
    [사마의]: {analysis.get("samaui")}
    [주유]: {analysis.get("juyu")}
    """

    response_data = await llm_router.execute_with_routing(
        final_prompt, context={"quality_tier": QualityTier.ULTRA}
    )

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
