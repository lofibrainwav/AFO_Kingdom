#!/usr/bin/env python3
"""
GoT (Graph of Thought) Example Implementation for AFO Kingdom Chancellor V2

This module demonstrates Graph of Thought implementation using LangGraph,
integrated with AFO Kingdom's Chancellor Graph V2 architecture.

Features:
- Node-based thought generation and evaluation
- Redis checkpointing for state persistence
- Conditional edges for branching logic
- Trinity Score integration for decision making
- Context7 knowledge injection

Author: AFO Kingdom Chancellor System
Date: 2026-01-01
"""

import json
import os
import time
from datetime import datetime
from typing import Annotated

import redis
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict as TypedDictExt

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Initialize Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


class GoTState(TypedDictExt):
    """Graph of Thought state definition"""

    messages: Annotated[list, add_messages]  # Thought chain messages
    thoughts: list[str]  # GoT vertices (thought units)
    best_thought: str  # Final aggregated thought
    checkpoint: str  # Redis checkpoint key
    trinity_score: dict  # Trinity Score for decision making
    context7_data: dict  # Context7 injected knowledge


def generate_thoughts(state: GoTState) -> dict:
    """
    Generate thoughts node (aggregation → generation)

    This represents the initial thought generation phase in GoT,
    where multiple ideas are generated from the input.
    """
    input_message = state["messages"][-1].content
    prompt = f"AFO 왕국 철학 기반으로 '{input_message}' 문제 해결을 위한 3가지 아이디어 생성"

    # Simulate LLM call with Trinity Score consideration
    base_ideas = [
        "眞: 기술적 정확성 기반 해결 방안",
        "善: 윤리적 안정성 우선 해결 방안",
        "美: 우아한 구조적 해결 방안",
    ]

    # Enhance with Context7 knowledge if available
    if state.get("context7_data"):
        context_knowledge = state["context7_data"].get("technical_patterns", [])
        if context_knowledge:
            base_ideas.extend([f"Context7 기반: {k}" for k in context_knowledge[:2]])

    # Create checkpoint
    checkpoint_key = f"got_generate_{int(time.time())}"
    checkpoint_data = {
        "timestamp": datetime.now().isoformat(),
        "input": input_message,
        "generated_thoughts": base_ideas,
        "trinity_score": state.get("trinity_score", {}),
    }

    redis_client.set(checkpoint_key, json.dumps(checkpoint_data))

    return {"thoughts": state["thoughts"] + base_ideas, "checkpoint": checkpoint_key}


def evaluate_thoughts(state: GoTState) -> dict:
    """
    Evaluate thoughts node (scoring and selection)

    This represents the evaluation phase where thoughts are scored
    and the best one is selected based on Trinity Score criteria.
    """
    thoughts = state["thoughts"]
    trinity_weights = {
        "truth": 0.35,
        "goodness": 0.35,
        "beauty": 0.20,
        "serenity": 0.08,
        "eternity": 0.02,
    }

    # Simulate scoring based on Trinity Score
    scores = []
    for thought in thoughts:
        # Simple scoring based on keywords (眞善美 keywords)
        score = 0.5  # Base score
        if "眞" in thought or "기술" in thought:
            score += 0.2
        if "善" in thought or "안정" in thought:
            score += 0.2
        if "美" in thought or "우아" in thought:
            score += 0.15
        scores.append(min(score, 1.0))  # Cap at 1.0

    # Select best thought
    best_idx = scores.index(max(scores))
    best_thought = thoughts[best_idx]

    # Create checkpoint
    checkpoint_key = f"got_evaluate_{int(time.time())}"
    checkpoint_data = {
        "timestamp": datetime.now().isoformat(),
        "thoughts": thoughts,
        "scores": scores,
        "best_thought": best_thought,
        "trinity_score": state.get("trinity_score", {}),
    }

    redis_client.set(checkpoint_key, json.dumps(checkpoint_data))

    return {
        "best_thought": best_thought,
        "messages": state["messages"]
        + [AIMessage(content=f"최고 아이디어 선택: {best_thought} (점수: {max(scores):.2f})")],
        "checkpoint": checkpoint_key,
    }


def improve_thought(state: GoTState) -> dict:
    """
    Improve thought node (feedback loop and enhancement)

    This represents the improvement phase where the selected thought
    is enhanced with additional context and Trinity Score optimization.
    """
    best_thought = state["best_thought"]

    # Enhance with AFO Kingdom philosophy
    enhanced_thought = f"{best_thought} + 眞善美孝永 철학 통합 최적화"

    # Add Context7 insights if available
    if state.get("context7_data"):
        insights = state["context7_data"].get("insights", [])
        if insights:
            enhanced_thought += f" + Context7 인사이트: {insights[0]}"

    # Create checkpoint
    checkpoint_key = f"got_improve_{int(time.time())}"
    checkpoint_data = {
        "timestamp": datetime.now().isoformat(),
        "original_thought": best_thought,
        "enhanced_thought": enhanced_thought,
        "trinity_score": state.get("trinity_score", {}),
    }

    redis_client.set(checkpoint_key, json.dumps(checkpoint_data))

    return {
        "thoughts": [enhanced_thought],
        "messages": state["messages"]
        + [AIMessage(content=f"개선된 해결 방안: {enhanced_thought}")],
        "checkpoint": checkpoint_key,
    }


def create_got_graph() -> StateGraph:
    """
    Create the Graph of Thought workflow

    This implements the core GoT structure with nodes and conditional edges,
    following AFO Kingdom Chancellor Graph V2 patterns.
    """
    # Initialize workflow
    workflow = StateGraph(GoTState)

    # Add nodes (GoT operations)
    workflow.add_node("generate", generate_thoughts)
    workflow.add_node("evaluate", evaluate_thoughts)
    workflow.add_node("improve", improve_thought)

    # Define edges (GoT flow)
    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", "evaluate")

    # Conditional edge: improve if we have fewer than optimal thoughts
    workflow.add_conditional_edges(
        "evaluate",
        lambda state: "improve" if len(state["thoughts"]) < 5 else END,
        {"improve": "improve", END: END},
    )

    # Feedback loop for iterative improvement
    workflow.add_edge("improve", "generate")

    return workflow


def run_got_example(problem: str = "2026년 AFO 왕국 AI 시스템 최적화 방안") -> dict:
    """
    Execute Graph of Thought example

    Args:
        problem: The problem to solve using GoT

    Returns:
        Final result with thoughts and checkpoints
    """
    print("🏰 AFO 왕국 GoT (Graph of Thought) 실행 시작")
    print(f"문제: {problem}")
    print("-" * 50)

    # Test Redis connection
    try:
        redis_client.ping()
        print("✅ Redis 연결 성공")
    except redis.ConnectionError:
        print("❌ Redis 연결 실패 - Redis 서버가 실행 중인지 확인하세요")
        return {"error": "Redis connection failed"}

    # Create workflow
    workflow = create_got_graph()
    graph = workflow.compile()

    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=problem)],
        "thoughts": [],
        "best_thought": "",
        "checkpoint": f"got_start_{int(time.time())}",
        "trinity_score": {
            "truth": 0.9,
            "goodness": 0.85,
            "beauty": 0.8,
            "serenity": 0.95,
            "eternity": 0.9,
        },
        "context7_data": {
            "technical_patterns": ["병렬 처리", "캐싱 최적화"],
            "insights": ["트리니티 스코어 기반 의사결정"],
        },
    }

    # Execute
    print("🚀 GoT 그래프 실행 중...")
    result = graph.invoke(initial_state)

    print("✅ GoT 실행 완료")
    print(f"최종 결과: {result['best_thought']}")
    print(f"생성된 생각 수: {len(result['thoughts'])}")
    print(f"최종 체크포인트: {result['checkpoint']}")

    # Show checkpoints
    print("\n📋 Redis 체크포인트 확인:")
    for key in redis_client.keys("got_*"):
        if "start" not in key:  # Skip start checkpoint
            data = json.loads(redis_client.get(key))
            print(f"  {key}: {data.get('timestamp', 'N/A')}")

    return result


if __name__ == "__main__":
    # Execute example
    result = run_got_example()

    if "error" not in result:
        print("\n🎯 GoT 실행 성공! AFO 왕국 Chancellor Graph V2 기반 Graph of Thought 구현 확인")
        print(f"Trinity Score: {result.get('trinity_score', {})}")
    else:
        print(f"\n❌ 실행 실패: {result['error']}")
