import json
from collections.abc import AsyncIterator

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse

router = APIRouter(prefix="/chancellor", tags=["chancellor"])


class ChancellorRequest(BaseModel):
    input: str
    engine: str | None = None


def _sse(event: str, data_obj) -> bytes:
    return f"event: {event}\ndata: {json.dumps(data_obj, ensure_ascii=False)}\n\n".encode()


async def _stream_echo(text: str) -> AsyncIterator[bytes]:
    yield _sse("delta", {"type": "delta", "text": text})
    yield _sse("done", {"type": "done"})


async def _stream_langgraph(text: str) -> AsyncIterator[bytes]:
    try:
        from langgraph.graph import END, StateGraph
    except Exception:
        async for b in _stream_echo("[langgraph 미설치/임포트 실패] " + text):
            yield b
        return

    class State(dict):
        pass

    async def respond(state: State) -> State:
        state["output"] = state.get("input", "")
        return state

    g = StateGraph(State)
    g.add_node("respond", respond)
    g.set_entry_point("respond")
    g.add_edge("respond", END)
    app = g.compile()

    out = await app.ainvoke({"input": text})
    msg = out.get("output", "")

    yield _sse("delta", {"type": "delta", "text": msg})
    yield _sse("done", {"type": "done", "engine": "langgraph"})


async def _stream_crewai(text: str) -> AsyncIterator[bytes]:
    try:
        from crewai import Agent, Crew, Process, Task
    except Exception:
        async for b in _stream_echo("[crewai 미설치/임포트 실패] " + text):
            yield b
        return

    agent = Agent(
        role="Chancellor",
        goal="입력을 간단히 정리해 1문장으로 출력",
        backstory="AFO Chancellor",
        verbose=False,
        allow_delegation=False,
    )
    task = Task(description=f"다음을 1문장으로 요약: {text}", agent=agent)
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)

    try:
        result = crew.kickoff()
        msg = str(result)
    except Exception:
        msg = "[crewai 실행 실패] " + text

    yield _sse("delta", {"type": "delta", "text": msg})
    yield _sse("done", {"type": "done", "engine": "crewai"})


async def _stream_autogen(text: str) -> AsyncIterator[bytes]:
    try:
        from autogen_agentchat.agents import AssistantAgent
    except Exception:
        async for b in _stream_echo("[autogen-agentchat 미설치/임포트 실패] " + text):
            yield b
        return

    try:
        AssistantAgent(name="Chancellor")
        msg = f"[autogen-agentchat 기본 에코] {text}"
    except Exception:
        msg = "[autogen-agentchat 실행 실패] " + text

    yield _sse("delta", {"type": "delta", "text": msg})
    yield _sse("done", {"type": "done", "engine": "autogen"})


@router.post("/stream")
async def chancellor_stream(req: ChancellorRequest):
    engine = (req.engine or "langgraph").lower()

    if engine == "langgraph":
        gen = _stream_langgraph(req.input)
    elif engine == "crewai":
        gen = _stream_crewai(req.input)
    elif engine == "autogen":
        gen = _stream_autogen(req.input)
    else:
        gen = _stream_echo(req.input)

    return StreamingResponse(gen, media_type="text/event-stream")
