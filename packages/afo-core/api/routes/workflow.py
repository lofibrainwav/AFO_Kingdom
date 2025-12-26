"""
T28: Workflow Designer API
Endpoints for managing LangGraph workflows (CRUD + Execute)
"""
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# In-memory workflow storage (for MVP)
# Production: Use PostgreSQL or Redis
WORKFLOWS: dict[str, dict[str, Any]] = {}


class WorkflowNode(BaseModel):
    id: str
    type: str  # start, llm, tool, condition, end
    label: str
    x: float
    y: float
    config: dict[str, Any] | None = None


class WorkflowEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str | None = None


class WorkflowDefinition(BaseModel):
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]


class SaveWorkflowRequest(BaseModel):
    workflow: WorkflowDefinition
    name: str | None = None


class WorkflowResponse(BaseModel):
    id: str
    name: str
    workflow: WorkflowDefinition
    status: str


@router.get("/templates")
async def get_node_templates() -> dict[str, Any]:
    """Return available node templates for the workflow designer."""
    return {
        "templates": [
            {
                "type": "start",
                "label": "Start",
                "description": "Workflow entry point",
                "configSchema": {},
            },
            {
                "type": "llm",
                "label": "LLM Call",
                "description": "Invoke a language model",
                "configSchema": {
                    "model": {"type": "string", "default": "gpt-4"},
                    "temperature": {"type": "number", "default": 0.7},
                    "prompt": {"type": "string", "default": ""},
                },
            },
            {
                "type": "tool",
                "label": "Tool",
                "description": "Execute a registered tool/skill",
                "configSchema": {
                    "tool_name": {"type": "string", "default": ""},
                    "args": {"type": "object", "default": {}},
                },
            },
            {
                "type": "condition",
                "label": "Condition",
                "description": "Branch based on condition",
                "configSchema": {
                    "condition": {"type": "string", "default": ""},
                    "true_branch": {"type": "string", "default": ""},
                    "false_branch": {"type": "string", "default": ""},
                },
            },
            {
                "type": "end",
                "label": "End",
                "description": "Workflow exit point",
                "configSchema": {},
            },
        ]
    }


@router.post("/save", response_model=WorkflowResponse)
async def save_workflow(request: SaveWorkflowRequest) -> WorkflowResponse:
    """Save a workflow definition."""
    import time

    workflow_id = f"wf-{int(time.time())}"
    name = request.name or f"Workflow {workflow_id}"

    WORKFLOWS[workflow_id] = {
        "id": workflow_id,
        "name": name,
        "workflow": request.workflow.model_dump(),
        "status": "saved",
    }

    return WorkflowResponse(
        id=workflow_id,
        name=name,
        workflow=request.workflow,
        status="saved",
    )


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str) -> WorkflowResponse:
    """Get a workflow by ID."""
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")

    wf = WORKFLOWS[workflow_id]
    return WorkflowResponse(
        id=wf["id"],
        name=wf["name"],
        workflow=WorkflowDefinition(**wf["workflow"]),
        status=wf["status"],
    )


@router.get("/")
async def list_workflows() -> dict[str, Any]:
    """List all saved workflows."""
    return {
        "workflows": [
            {"id": wf["id"], "name": wf["name"], "status": wf["status"]}
            for wf in WORKFLOWS.values()
        ]
    }


@router.post("/execute/{workflow_id}")
async def execute_workflow(workflow_id: str) -> dict[str, Any]:
    """Execute a saved workflow (MVP: returns mock execution result)."""
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # MVP: Mock execution
    # Production: Convert to LangGraph StateGraph and execute
    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "result": {
            "message": "Workflow executed successfully (MVP simulation)",
            "steps": ["start", "llm", "end"],
        },
    }
