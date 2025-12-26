from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any, Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse

router = APIRouter(prefix="/chancellor", tags=["chancellor"])


class ChancellorRequest(BaseModel):
    input: str
    engine: str | None = None


def _sse(event: str, data_obj: Any) -> bytes:
    return (
        f"event: {event}\n" f"data: {json.dumps(data_obj, ensure_ascii=False)}\n\n"
    ).encode()


async def _stream_echo(text: str) -> AsyncIterator[bytes]:
    yield _sse("start", {"engine": "echo"})
    for i, ch in enumerate(text):
        yield _sse("token", {"i": i, "t": ch})
    yield _sse("done", {"ok": True})


async def _stream_langgraph(text: str) -> AsyncIterator[bytes]:
    try:
        import langgraph

        yield _sse("info", {"engine": "langgraph", "status": "installed"})
    except Exception:
        yield _sse("info", {"engine": "langgraph", "status": "missing"})
        async for b in _stream_echo(text):
            yield b
        return
    async for b in _stream_echo(text):
        yield b


async def _stream_crewai(text: str) -> AsyncIterator[bytes]:
    try:
        import crewai

        yield _sse("info", {"engine": "crewai", "status": "installed"})
    except Exception:
        yield _sse("info", {"engine": "crewai", "status": "missing"})
        async for b in _stream_echo(text):
            yield b
        return
    async for b in _stream_echo(text):
        yield b


async def _stream_autogen(text: str) -> AsyncIterator[bytes]:
    try:
        import autogen

        yield _sse("info", {"engine": "autogen", "status": "installed"})
    except Exception:
        yield _sse("info", {"engine": "autogen", "status": "missing"})
        async for b in _stream_echo(text):
            yield b
        return
    async for b in _stream_echo(text):
        yield b


@router.get("/ping")
async def chancellor_ping():
    return {"ok": True}


@router.get("/ping_v2")
async def chancellor_ping_v2():
    return {"ok": True}


@router.get("/engines")
async def chancellor_engines():
    installed = {}
    try:
        import langgraph

        installed["langgraph"] = True
    except Exception:
        installed["langgraph"] = False
    try:
        import crewai

        installed["crewai"] = True
    except Exception:
        installed["crewai"] = False
    try:
        import autogen

        installed["autogen"] = True
    except Exception:
        try:
            import autogen_agentchat

            installed["autogen"] = True
        except Exception:
            installed["autogen"] = False
    return {"installed": installed}


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


@router.post("/stream_v2")
async def chancellor_stream_v2(req: ChancellorRequest):
    from typing import TypedDict

    class _LGState(TypedDict, total=False):
        input: str
        tokens: list[str]

    def _lg_tokenize(state: _LGState) -> _LGState:
        s = state.get("input") or ""
        return {"tokens": list(s)}

    async def _stream_langgraph_real(text: str):
        try:
            from langgraph.graph import END, StateGraph  # type: ignore
        except Exception:
            yield _sse("info", {"engine": "langgraph_real", "status": "missing"})
            async for b in _stream_echo(text):
                yield b
            return

        yield _sse("info", {"engine": "langgraph_real", "status": "installed"})

        g = StateGraph(_LGState)
        g.add_node("tokenize", _lg_tokenize)
        g.set_entry_point("tokenize")
        g.add_edge("tokenize", END)
        compiled = g.compile()

        out = await compiled.ainvoke({"input": text})
        tokens = out.get("tokens") or []

        yield _sse("start", {"engine": "langgraph_real"})
        for i, ch in enumerate(tokens):
            yield _sse("token", {"i": i, "t": ch})
        yield _sse("done", {"ok": True})

    engine = (req.engine or "langgraph_real").lower()
    if engine in ("langgraph_real", "langgraph"):
        gen = _stream_langgraph_real(req.input)
    else:
        gen = _stream_echo(req.input)
    return StreamingResponse(gen, media_type="text/event-stream")


from importlib.util import find_spec


def _is_installed(mod: str) -> bool:
    return find_spec(mod) is not None


@router.get("/ping_v3")
async def chancellor_ping_v3():
    return {"ok": True}


@router.post("/stream_v3")
async def chancellor_stream_v3(req: ChancellorRequest):
    async def _stream_langgraph_real_v3(text: str):
        yield _sse(
            "info",
            {"engine": "langgraph_real", "installed": _is_installed("langgraph")},
        )
        try:
            from typing import TypedDict

            from langgraph.graph import END, StateGraph  # type: ignore

            class _LGState(TypedDict, total=False):
                input: str
                tokens: list[str]

            def _lg_tokenize(state: _LGState) -> _LGState:
                return {"tokens": list(state.get("input") or "")}

            g = StateGraph(_LGState)
            g.add_node("tokenize", _lg_tokenize)
            g.set_entry_point("tokenize")
            g.add_edge("tokenize", END)
            compiled = g.compile()

            yield _sse("start", {"engine": "langgraph_real"})
            out = await compiled.ainvoke({"input": text})
            tokens = out.get("tokens") or []
            for i, ch in enumerate(tokens):
                yield _sse("token", {"i": i, "t": ch})
            yield _sse("done", {"ok": True})
        except Exception as e:
            yield _sse("error", {"engine": "langgraph_real", "error": str(e)})
            async for b in _stream_echo(text):
                yield b

    engine = (req.engine or "langgraph_real").lower()
    installed = {
        "langgraph": _is_installed("langgraph"),
        "crewai": _is_installed("crewai"),
        "autogen": _is_installed("autogen_agentchat") or _is_installed("autogen"),
    }
    yield_headers = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}

    if engine in ("langgraph_real", "langgraph"):
        gen = _stream_langgraph_real_v3(req.input)
    elif engine == "crewai":

        async def _gen():
            yield _sse("info", {"engine": "crewai", "installed": installed["crewai"]})
            async for b in _stream_echo(req.input):
                yield b

        gen = _gen()
    elif engine == "autogen":

        async def _gen():
            yield _sse("info", {"engine": "autogen", "installed": installed["autogen"]})
            async for b in _stream_echo(req.input):
                yield b

        gen = _gen()
    else:
        gen = _stream_echo(req.input)

    return StreamingResponse(gen, media_type="text/event-stream", headers=yield_headers)
