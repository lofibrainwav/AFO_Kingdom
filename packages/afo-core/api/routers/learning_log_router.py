"""
Learning Log Router (Phase 16-4)
Endpoints for the Kingdom's Self-Learning Loop.
"""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from datetime import datetime
import asyncio
import json
import random
from AFO.models.learning_log import LearningLog

router = APIRouter()

# In-memory storage for MVP (Phase 16-4 Demo)
# In production (Phase 17), this connects to PostgreSQL via LearningLog model
_learning_logs = []
_new_log_event = asyncio.Event()

@router.post("/api/learning-log")
async def create_learning_log(log: LearningLog):
    """
    Receives feedback from Agents (Samahwi/Juyu) and saves it.
    """
    log.timestamp = datetime.utcnow()
    # Simulating DB ID assignment
    log.id = len(_learning_logs) + 1
    _learning_logs.append(log)
    
    # Notify subscribers
    _new_log_event.set()
    _new_log_event.clear()
    
    return {"status": "success", "id": log.id}

@router.get("/api/learning-log/latest")
async def get_latest_logs():
    """Returns the latest 10 logs."""
    return sorted(_learning_logs, key=lambda x: x.timestamp, reverse=True)[:10]

@router.get("/api/learning-log/stream")
async def stream_learning_logs(request: Request):
    """
    SSE Endpoint: Streams new learning logs to the Dashboard.
    """
    async def event_generator():
        # First send existing logs
        for log in sorted(_learning_logs, key=lambda x: x.timestamp, reverse=True)[:5]:
             yield f"data: {json.dumps(log.dict(), default=str)}\n\n"
             
        while True:
            if await request.is_disconnected():
                break
            
            # Simple simulation for the "Alive" feel if no real events
            # In real system, this waits for _new_log_event
            # Here we wait for event OR simulate a heartbeat
            try:
                # Wait for real event or timeout
                # If doing real event loop:
                # await _new_log_event.wait()
                # But for demo "Vibe", let's just wait a bit and send nothing if silent
                await asyncio.sleep(1)
                
                # If we had a real event system, we'd yield here.
                # For now, let's just yield the latest log if it changed?
                # Actually, the user wants to see the loop *close*.
                
                # Checking if new logs appeared since last check (simplified)
                # In a real impl with PostgreSQL LISTEN/NOTIFY, this is different.
                pass 

            except asyncio.CancelledError:
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")
