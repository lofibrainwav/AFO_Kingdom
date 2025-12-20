from datetime import datetime
from typing import Annotated, Any, TypedDict

from langchain_core.messages import AIMessage, BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

# Import existing LLM Router logic for model execution
from llm_router import QualityTier, llm_router

try:
    from AFO.domain.metrics.trinity_manager import TrinityManager, trinity_manager
except ImportError:
    trinity_manager: TrinityManager | None = None  # type: ignore

# Antigravity 통합 (眞: 명시적 설정 전달)
try:
    from AFO.config.antigravity import antigravity
except ImportError:
    try:
        from config.antigravity import antigravity  # type: ignore[assignment]
    except ImportError:
        # Fallback: 기본값 사용
        class MockAntigravity:
            AUTO_DEPLOY = True
            DRY_RUN_DEFAULT = True

        antigravity = MockAntigravity()  # type: ignore[assignment]

# Redis for Matrix Stream (Track B)
import json

from AFO.utils.redis_connection import get_shared_async_redis_client



# Import Modular Strategists & Tigers (Phase 3 Integration)
from strategists import zhuge_liang, sima_yi, zhou_yu
from tigers import guan_yu, zhang_fei, zhao_yun, ma_chao, huang_zhong
import asyncio

async def publish_thought(agent: str, message: str, type: str = "thought") -> None:
    """
    [Matrix Stream] Publish internal monologue to Redis for frontend visualization.
    """
    try:
        redis = await get_shared_async_redis_client()
        payload = {
            "source": agent,
            "message": message,
            "type": type,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
        await redis.publish("chancellor_thought_stream", json.dumps(payload))
    except Exception as e:
        print(f"⚠️ [Matrix Stream] Failed to publish: {e}")

async def o5_tigers_parallel_execution(query_data: dict[str, Any]) -> list[float | str]:
    """
    [O5 Tigers] Parallel Execution Engine (Phase 3)
    Executes the 5 Tigers in parallel for maximum efficiency.
    """
    print("🐯 [O5 Tigers] Executing 5-Pillar Parallel Operation...")
    await publish_thought("O5 Tigers", "Executing 5-Pillar Parallel Operation...", "thought")
    
    tasks = [
        asyncio.to_thread(guan_yu.guard, query_data),
        asyncio.to_thread(zhang_fei.gate, query_data.get("risk", 0.0), query_data),
        asyncio.to_thread(zhao_yun.craft, query_data.get("code", ""), 2),
        asyncio.to_thread(ma_chao.deploy, query_data),
        asyncio.to_thread(huang_zhong.log, "Parallel Execution", {"trinity": 100.0})
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"✅ [O5 Tigers] Execution Complete: {results}")
    return list(results)



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
    current_speaker: str  # "user", "chancellor", "zhuge_liang", "sima_yi", "zhou_yu"
    steps_taken: int
    complexity: str  # "Low", "Medium", "High"

    # Reducer for analysis results (Merge dicts)
    analysis_results: Annotated[dict[str, str], lambda a, b: {**(a or {}), **b}]
    next_step: str


def calculate_complexity(query: str) -> str:
    """
    Heuristic Complexity Analysis (Phase 4.1)
    TODO: Upgrade to LLM-based complexity classifier in Phase 5.
    """
    length = len(query)
    keywords = ["analyze", "compare", "strategy", "architecture", "solve", "design"]
    keyword_count = sum(1 for k in keywords if k in query.lower())

    if length > 200 or keyword_count >= 2:
        return "High"
    elif length > 50 or keyword_count >= 1:
        return "Medium"
    else:
        return "Low"


async def chancellor_router_node(state: ChancellorState) -> dict[str, Any]:
    """
    [Chancellor Node] - Async Upgrade for Matrix Stream
    """
    print("👑 [Chancellor] Analyzing state & Complexity...")
    await publish_thought("Chancellor", "Analyzing state & Complexity... [Rule #0]", "thought")

    messages = state["messages"]

    # Init State Variables
    steps = state.get("steps_taken", 0)
    state["steps_taken"] = steps + 1

    # Analyze Query Complexity - [논어] 지지위지지 = 아는 것과 모르는 것을 구분
    query_content = messages[0].content
    query_str: str = query_content if isinstance(query_content, str) else str(query_content)
    complexity = state.get("complexity")
    if not complexity:
        complexity = calculate_complexity(query_str)
        state["complexity"] = complexity
        print(f"🧠 [Chancellor] Query Complexity: {complexity}")

    # Antigravity Config
    context = state.get("kingdom_context", {}) or {}
    antigravity_config = context.get("antigravity", {})
    is_dry_run = antigravity_config.get("DRY_RUN_DEFAULT", antigravity.DRY_RUN_DEFAULT)

    # DRY_RUN 모드일 때는 auto_run_eligible을 False로 강제 (善: 안전 우선)
    if is_dry_run and state.get("auto_run_eligible", False):
        print("🛡️ [Chancellor] DRY_RUN 모드 감지 - auto_run_eligible을 False로 조정 (善)")
        state["auto_run_eligible"] = False

    analysis = state.get("analysis_results", {})

    # 1. Always start with Zhuge Liang (Truth)
    if "zhuge_liang" not in analysis:
        return {
            "next_step": "zhuge_liang",
            "current_speaker": "chancellor",
            "steps_taken": steps + 1,
            "complexity": complexity,
        }

    # 2. Complexity-based Paths
    if complexity == "Low":
        # simple: Truth -> Finalize
        return {"next_step": "finalize", "current_speaker": "chancellor"}

    elif complexity == "Medium":
        # standard: Truth -> Goodness -> Finalize
        if "sima_yi" not in analysis:
            return {"next_step": "sima_yi", "current_speaker": "chancellor"}
        return {"next_step": "finalize", "current_speaker": "chancellor"}

    elif complexity == "High":
        # complex: Truth -> Goodness -> Beauty -> Finalize (Sequential for V1 stability)
        # In V2, we can loop Truth <-> Goodness if disagreement is high.
        if "sima_yi" not in analysis:
            return {"next_step": "sima_yi", "current_speaker": "chancellor"}
        if "zhou_yu" not in analysis:
            return {"next_step": "zhou_yu", "current_speaker": "chancellor"}

        return {"next_step": "finalize", "current_speaker": "chancellor"}

    # Fallback
    return {"next_step": "finalize", "current_speaker": "chancellor"}


async def zhuge_liang_node(state: ChancellorState) -> dict[str, Any]:
    """
    [Zhuge Liang Node] - Truth (矛)
    Focus: Architecture, Strategy, Technical Certainty.
    """
    print("⚔️ [Zhuge Liang] Analyzing Truth...")
    await publish_thought("Zhuge Liang", "Analyzing Truth... (Checking Architecture)", "thought")
    query = state["messages"][-1].content

    # Use LLM Router to call a "Smart" model (Truth requires intelligence)
    # Context can be passed to select specific persona prompts if we had them loaded here.
    # For now, we simulate the persona via system context augmentation in a real implementation.

    # In a full implementation, we would inject the System Prompt from TRINITY-OS/docs/personas/STRATEGIST_ZHUGE_LIANG.md
    base_context = (state.get("kingdom_context") or {}).get("llm_context") or {}
    context = {
        **base_context,
        "quality_tier": base_context.get("quality_tier", QualityTier.PREMIUM),
        "max_tokens": base_context.get("max_tokens", 512),
    }

    response_data = await llm_router.execute_with_routing(
        f"당신은 제갈량(Zhuge Liang - Truth)입니다. 다음 질문을 기술적/구조적 관점에서 분석하시오: {query}",
        context=context,
    )

    content = response_data.get("response", "분석 실패")

    # Rely on Reducer to merge this delta
    return {
        "analysis_results": {"zhuge_liang": content},
        "messages": [AIMessage(content=f"[Zhuge Liang] {content}", name="zhuge_liang")],
    }


# Import Yeongdeok for Sage Consultations
from AFO.scholars.yeongdeok import yeongdeok


async def sima_yi_node(state: ChancellorState) -> dict[str, Any]:
    """
    [Sima Yi Node] - Goodness (盾)
    Focus: Ethics, Stability, Risk Management.
    Uses: Samahwi (Qwen3-30B Pure MoE)
    """
    print("🛡️ [Sima Yi] Consulting Samahwi (Backend/Risk)...")
    await publish_thought("Sima Yi", "Consulting Samahwi for Stability Check...", "thought")
    query = state["messages"][0].content
    truth_analysis = state["analysis_results"].get("zhuge_liang", "")

    # Construct rigid prompt for the Sage
    sage_prompt = (
        f"Original Query: {query}\n"
        f"Truth Analysis: {truth_analysis[:500]}...\n\n"
        "Analyze this from a Security & Stability (Goodness) perspective. "
        "Highlight any risks, side effects, or ethical concerns."
    )

    # Call Samahwi via Yeongdeok
    content = await yeongdeok.consult_samahwi(sage_prompt)

    return {
        "analysis_results": {"sima_yi": content},
        "messages": [AIMessage(content=f"[Sima Yi] {content}", name="sima_yi")],
    }


async def zhou_yu_node(state: ChancellorState) -> dict[str, Any]:
    """
    [Zhou Yu Node] - Beauty (橋)
    Focus: Narrative, UX, User Experience.
    Uses: Jwaja (DeepSeek-R1 Frontend) & Hwata (Qwen3-VL UX)
    """
    print("桥 [Zhou Yu] Consulting Jwaja (Frontend) & Hwata (UX)...")
    await publish_thought("Zhou Yu", "Consulting Jwaja & Hwata for Beauty & Serenity...", "thought")
    original_query = state["messages"][0].content
    truth = state["analysis_results"].get("zhuge_liang", "")

    # 1. Frontend Architecture (Jwaja)
    jwaja_prompt = (
        f"Query: {original_query}\n"
        f"Technical Context: {truth[:300]}\n"
        "Propose a UI/UX logic or Component structure that is Beautiful & Serene."
    )
    jwaja_content = await yeongdeok.consult_jwaja(jwaja_prompt)

    # 2. UX Tone/Copy (Hwata) - Optional but adds flavor
    # We can combine or append. For now, let's use Hwata to refine Jwaja's output.
    hwata_prompt = (
        f"Refine this UI logic into a user-friendly narrative:\n{jwaja_content[:500]}\n"
        "Focus on comfort (Serenity) and clear guidance."
    )
    hwata_content = await yeongdeok.consult_hwata(hwata_prompt)

    # Combine for final Zhou Yu output
    final_content = (
        f"**UI Strategy (Jwaja)**:\n{jwaja_content}\n\n**UX Narrative (Hwata)**:\n{hwata_content}"
    )

    return {
        "analysis_results": {"zhou_yu": final_content},
        "messages": [AIMessage(content=f"[Zhou Yu] {final_content}", name="zhou_yu")],
    }


async def chancellor_finalize_node(state: ChancellorState) -> dict[str, Any]:
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
    if analysis.get("zhuge_liang"):
        parts.append(f"[Zhuge Liang]: {analysis.get('zhuge_liang')}")
    if analysis.get("sima_yi"):
        parts.append(f"[Sima Yi]: {analysis.get('sima_yi')}")
    if analysis.get("zhou_yu"):
        parts.append(f"[Zhou Yu]: {analysis.get('zhou_yu')}")
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


def trinity_decision_gate(state: ChancellorState) -> dict[str, Any]:
    """
    [Decision Gate] - Trinity-Driven Routing (Phase 5)
    Evaluates Trinity Score to determine AUTO_RUN eligibility.

    Conditions for AUTO_RUN:
    - Trinity Score >= 0.9 (90%)
    - Risk Score <= 0.1 (10%)

    Otherwise: ASK_COMMANDER (Human-in-the-loop)
    """
    if trinity_manager:
        metrics = trinity_manager.get_current_metrics()
        trinity_score = metrics.trinity_score
        # Risk = inverse of Goodness (善 protects against risk)
        risk_score = 1.0 - metrics.goodness
    else:
        # Fallback if TrinityManager unavailable
        trinity_score = state.get("trinity_score", 0.85)
        risk_score = state.get("risk_score", 0.15)

    auto_run_eligible = trinity_score >= 0.9 and risk_score <= 0.1
    decision = "AUTO_RUN" if auto_run_eligible else "ASK_COMMANDER"

    print(f"⚖️ [Decision Gate] Trinity: {trinity_score:.2f}, Risk: {risk_score:.2f} → {decision}")

    return {
        "trinity_score": trinity_score,
        "risk_score": risk_score,
        "auto_run_eligible": auto_run_eligible,
    }


async def historian_node(state: ChancellorState) -> dict[str, Any]:
    """
    [Historian Node] - Autonomous Archiving (Genesis Project)
    Records the session state into the Royal Chronicles (Obsidian).
    """
    print("📜 [Historian] Recording Session Chronicle...")
    await publish_thought("Historian", "Recording Session Chronicle... (Project Genesis)", "info")

    # Extract essence
    messages = state["messages"]
    analysis = state["analysis_results"]

    # Format the content
    content = "# Royal Council Chronicle\n\n"
    content += f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    content += f"**Trinity Score**: {state.get('trinity_score', 0.0):.2f}\n"
    content += f"**Risk Score**: {state.get('risk_score', 0.0):.2f}\n\n"

    content += "## The Query\n"
    if messages:
        content += f"{messages[0].content}\n\n"

    content += "## The Council's Wisdom\n"
    for sage, advice in analysis.items():
        content += f"### {sage.capitalize()}\n{advice}\n\n"

    content += "## The Verdict\n"
    content += f"Final Decision: {state.get('next_step', 'Unknown')}\n"

    # Invoke Yeongdeok's Hand
    try:
        from AFO.scholars.yeongdeok import yeongdeok

        res = await yeongdeok.use_tool(
            "skill_013_obsidian_librarian",
            action="append_daily_log",
            content=f"Council Session Recorded.\nQuery: {messages[0].content[:50]}...",
            tag="chronicle",
        )
        # Also save full note
        full_note_path = f"journals/chronicles/session_{int(datetime.now().timestamp())}.md"
        await yeongdeok.use_tool(
            "skill_013_obsidian_librarian",
            action="write_note",
            note_path=full_note_path,
            content=content,
            metadata={"type": "chronicle", "participants": list(analysis.keys())},
        )
        print(f"✅ [Historian] Chronicle saved: {res}")
    except Exception as e:
        print(f"❌ [Historian] Failed to record: {e}")

    # Pass through state
    return {}


# --- 3. Graph Construction ---


def build_chancellor_graph(
    memory_saver: Any = None,
) -> Any:
    """眞 (Truth): 승상 오케스트레이션 그래프를 구축합니다."""
    # 1. 그래프 정의
    workflow = StateGraph(ChancellorState)

    # Add Nodes
    workflow.add_node("chancellor", chancellor_router_node)
    workflow.add_node("zhuge_liang", zhuge_liang_node)
    workflow.add_node("sima_yi", sima_yi_node)
    workflow.add_node("zhou_yu", zhou_yu_node)
    workflow.add_node("finalize", chancellor_finalize_node)
    workflow.add_node("decision_gate", trinity_decision_gate)  # Phase 5: Trinity Routing
    workflow.add_node("historian", historian_node)  # Genesis Project

    # Add Edges
    workflow.set_entry_point("chancellor")

    # Conditional Edge from Chancellor
    def route_logic(state: ChancellorState) -> str:
        """眞 (Truth): 상태에 따른 다음 단계 라우팅 로직"""
        return state["next_step"]

    workflow.add_conditional_edges(
        "chancellor",
        route_logic,
        {"zhuge_liang": "zhuge_liang", "sima_yi": "sima_yi", "zhou_yu": "zhou_yu", "finalize": "finalize"},
    )

    # Strategies return to Chancellor
    workflow.add_edge("zhuge_liang", "chancellor")
    workflow.add_edge("sima_yi", "chancellor")
    workflow.add_edge("zhou_yu", "chancellor")

    # Phase 5: Finalize → Decision Gate → Historian -> END
    workflow.add_edge("finalize", "decision_gate")
    workflow.add_edge("decision_gate", "historian")
    workflow.add_edge("historian", END)

    # Persistence Strategy (Dev: Memory, Prod: Postgres)
    # Using MemorySaver for current verification as per V2 Constitution (Dev Mode)
    checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)


# Singleton Instance
chancellor_graph = build_chancellor_graph()
