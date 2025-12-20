"""
Strategy Engine for AFO Kingdom
Provides memory context and workflow management for LLM interactions.
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class MemoryContext:
    """
    In-memory context manager for conversation history and state.
    Provides short-term memory for LLM interactions.
    """
    history: List[Dict[str, str]] = field(default_factory=list)
    state: Dict[str, Any] = field(default_factory=dict)
    max_turns: int = 20
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to conversation history."""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last N turns
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]
    
    def get_context(self, last_n: int = 5) -> List[Dict[str, str]]:
        """Get recent conversation context."""
        return self.history[-last_n * 2:] if self.history else []
    
    def set_state(self, key: str, value: Any) -> None:
        """Set a state variable."""
        self.state[key] = value
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a state variable."""
        return self.state.get(key, default)
    
    def clear(self) -> None:
        """Clear all memory."""
        self.history = []
        self.state = {}

@dataclass
class WorkflowStep:
    """A single step in a workflow."""
    name: str
    action: str
    params: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"  # pending, running, completed, failed
    result: Any = None

class Workflow:
    """
    Workflow manager for multi-step LLM operations.
    Supports sequential and parallel execution patterns.
    """
    def __init__(self, name: str = "default"):
        self.name = name
        self.steps: List[WorkflowStep] = []
        self.current_step: int = 0
        self.status: str = "idle"  # idle, running, completed, failed
    
    def add_step(self, name: str, action: str, **params) -> "Workflow":
        """Add a step to the workflow."""
        self.steps.append(WorkflowStep(name=name, action=action, params=params))
        return self
    
    def next_step(self) -> Optional[WorkflowStep]:
        """Get the next pending step."""
        for step in self.steps:
            if step.status == "pending":
                return step
        return None
    
    def mark_complete(self, step_name: str, result: Any = None) -> None:
        """Mark a step as complete."""
        for step in self.steps:
            if step.name == step_name:
                step.status = "completed"
                step.result = result
                break
    
    def is_complete(self) -> bool:
        """Check if all steps are complete."""
        return all(s.status == "completed" for s in self.steps)
    
    def reset(self) -> None:
        """Reset the workflow."""
        self.steps = []
        self.current_step = 0
        self.status = "idle"
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize workflow to dict."""
        return {
            "name": self.name,
            "status": self.status,
            "steps": [
                {"name": s.name, "action": s.action, "status": s.status}
                for s in self.steps
            ]
        }

# Global instances (exported for import)
memory_context = MemoryContext()
workflow = Workflow("afo_main")

# Convenience functions
def get_memory_context() -> MemoryContext:
    """Get the global memory context."""
    return memory_context

def get_workflow() -> Workflow:
    """Get the global workflow."""
    return workflow

def create_workflow(name: str) -> Workflow:
    """Create a new workflow."""
    return Workflow(name)
