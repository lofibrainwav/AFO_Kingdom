from __future__ import annotations

from fastapi import APIRouter
from starlette.responses import StreamingResponse

router = APIRouter()


@router.get("/query/stream")
def query_stream():
    def gen():
        yield "event: ping\ndata: ok\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")
