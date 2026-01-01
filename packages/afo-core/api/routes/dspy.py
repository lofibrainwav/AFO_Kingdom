#!/usr/bin/env python3
"""
DSPy MIPROv2 API Routes for AFO Kingdom
Implements Bayesian prompt optimization with Chancellor Graph V2 integration
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

# Try to import DSPy components
try:
    import dspy
    from dspy.teleprompt import MIPROv2

    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False
    print("Warning: DSPy not available. Install with: pip install dspy-ai")

from afo.context7 import Context7Manager
from afo.skills.skill_registry import SkillRegistry

from afo.trinity_metric_wrapper import TrinityMetricWrapper

router = APIRouter(prefix="/dspy", tags=["DSPy Optimization"])


# Pydantic models for API
class OptimizationRequest(BaseModel):
    task: str
    dataset: list[dict[str, Any]]
    num_candidates: int = 10
    max_bootstrapped_demos: int = 4
    num_trials: int = 20
    use_context7: bool = True
    use_skills: bool = True


class OptimizationResponse(BaseModel):
    optimized_prompt: dict[str, Any]
    trinity_score: dict[str, float]
    execution_time: float
    trials_completed: int
    best_score: float


class MIPROv2Optimizer:
    """MIPROv2 Optimizer with AFO Kingdom integration"""

    def __init__(self):
        self.context7 = Context7Manager()
        self.skill_registry = SkillRegistry()
        self.trinity_metric = TrinityMetricWrapper()

        # Configure DSPy LLM (default to Ollama for cost efficiency)
        if DSPY_AVAILABLE:
            # Use local Ollama for cost efficiency
            try:
                self.lm = dspy.OllamaLocal(model="llama3.1:8b")
            except:
                # Fallback to OpenAI if Ollama not available
                try:
                    self.lm = dspy.OpenAI(model="gpt-4o-mini")
                except:
                    self.lm = None
        else:
            self.lm = None

    def create_task_module(self, task_description: str) -> Any:
        """Create DSPy task module based on description"""
        if not DSPY_AVAILABLE:
            raise HTTPException(status_code=503, detail="DSPy not available")

        # Simple ChainOfThought module for general tasks
        class TaskModule(dspy.Module):
            def __init__(self):
                super().__init__()
                self.predictor = dspy.ChainOfThought("question -> answer")

            def forward(self, question: str) -> str:
                return self.predictor(question=question).answer

        return TaskModule()

    def prepare_dataset(self, raw_dataset: list[dict[str, Any]]) -> list[Any]:
        """Prepare dataset for MIPROv2 optimization"""
        dataset = []

        for item in raw_dataset:
            if isinstance(item, dict) and "question" in item and "answer" in item:
                # Create DSPy Example
                example = dspy.Example(
                    question=item["question"], answer=item["answer"]
                ).with_inputs("question")
                dataset.append(example)
            elif isinstance(item, dict) and "text" in item:
                # Simple text example
                example = dspy.Example(
                    question=item["text"][:200] + "...",  # Truncate for question
                    answer=item["text"],
                ).with_inputs("question")
                dataset.append(example)

        return dataset

    def trinity_metric_function(self, example, prediction, trace=None):
        """Trinity Score based metric function for MIPROv2"""
        try:
            # Calculate Trinity Score
            scores = self.trinity_metric.calculate_trinity_score(
                {"input": example.question, "output": prediction.answer, "trace": trace}
            )

            # Return combined score (weighted average)
            weights = {
                "truth": 0.35,
                "goodness": 0.35,
                "beauty": 0.20,
                "serenity": 0.08,
                "eternity": 0.02,
            }
            combined_score = sum(scores.get(k, 0.5) * v for k, v in weights.items())

            return combined_score

        except Exception as e:
            print(f"Trinity metric calculation failed: {e}")
            return 0.5  # Neutral score

    def optimize_with_mipro(self, task_module, trainset, config: dict[str, Any]) -> dict[str, Any]:
        """Execute MIPROv2 optimization"""
        if not DSPY_AVAILABLE or self.lm is None:
            raise HTTPException(status_code=503, detail="DSPy LLM not configured")

        start_time = time.time()

        # Configure DSPy
        dspy.settings.configure(lm=self.lm)

        # Create MIPROv2 teleprompter
        teleprompter = MIPROv2(
            num_candidates=config.get("num_candidates", 10),
            max_bootstrapped_demos=config.get("max_bootstrapped_demos", 4),
            num_trials=config.get("num_trials", 20),
            metric=self.trinity_metric_function,
        )

        # Execute optimization
        try:
            optimized_module = teleprompter.compile(student=task_module, trainset=trainset)

            execution_time = time.time() - start_time

            # Extract optimized prompt/program
            optimized_state = optimized_module.dump_state()

            return {
                "optimized_module": optimized_state,
                "execution_time": execution_time,
                "trials_completed": config.get("num_trials", 20),
                "teleprompter_config": {
                    "num_candidates": config.get("num_candidates", 10),
                    "max_bootstrapped_demos": config.get("max_bootstrapped_demos", 4),
                    "num_trials": config.get("num_trials", 20),
                },
            }

        except Exception as e:
            execution_time = time.time() - start_time
            raise HTTPException(
                status_code=500,
                detail=f"MIPROv2 optimization failed after {execution_time:.2f}s: {e!s}",
            )


# Global optimizer instance
optimizer = MIPROv2Optimizer()


@router.post("/optimize", response_model=OptimizationResponse)
async def optimize_prompt(request: OptimizationRequest, background_tasks: BackgroundTasks):
    """
    Execute MIPROv2 prompt optimization with AFO Kingdom integration

    - **task**: Task description for optimization
    - **dataset**: Training dataset for optimization
    - **num_candidates**: Number of candidates per trial (default: 10)
    - **max_bootstrapped_demos**: Max bootstrapped demonstrations (default: 4)
    - **num_trials**: Number of optimization trials (default: 20)
    - **use_context7**: Integrate Context7 data (default: true)
    - **use_skills**: Use Skills registry for evaluation (default: true)
    """
    try:
        # Enhance dataset with Context7 if requested
        enhanced_dataset = request.dataset
        if request.use_context7:
            try:
                context7_data = await optimizer.context7.get_relevant_context(
                    request.task, limit=50
                )
                # Add context7 data to dataset
                for item in context7_data:
                    enhanced_dataset.append(
                        {
                            "question": f"Context: {item.get('content', '')[:200]}...",
                            "answer": item.get("content", ""),
                        }
                    )
            except Exception as e:
                print(f"Context7 integration failed: {e}")

        # Create task module
        task_module = optimizer.create_task_module(request.task)

        # Prepare dataset
        trainset = optimizer.prepare_dataset(enhanced_dataset)

        if len(trainset) < 5:
            raise HTTPException(
                status_code=400, detail="Insufficient training data. Need at least 5 examples."
            )

        # Configure optimization
        config = {
            "num_candidates": request.num_candidates,
            "max_bootstrapped_demos": request.max_bootstrapped_demos,
            "num_trials": request.num_trials,
        }

        # Execute optimization
        result = optimizer.optimize_with_mipro(task_module, trainset, config)

        # Calculate final Trinity Score
        trinity_scores = optimizer.trinity_metric.calculate_trinity_score(
            {
                "task": request.task,
                "dataset_size": len(request.dataset),
                "optimization_result": result,
            }
        )

        # Background task: Save optimization result
        background_tasks.add_task(save_optimization_result, request.task, result, trinity_scores)

        return OptimizationResponse(
            optimized_prompt=result["optimized_module"],
            trinity_score=trinity_scores,
            execution_time=result["execution_time"],
            trials_completed=result["trials_completed"],
            best_score=max(trinity_scores.values()) if trinity_scores else 0.5,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {e!s}")


@router.get("/status")
async def get_optimization_status():
    """Get current DSPy optimization status"""
    return {
        "dspy_available": DSPY_AVAILABLE,
        "llm_configured": optimizer.lm is not None,
        "context7_available": True,
        "skills_available": True,
        "trinity_metric_available": True,
    }


@router.get("/examples")
async def get_example_requests():
    """Get example optimization requests for testing"""
    return {
        "examples": [
            {
                "task": "Answer questions about AFO Kingdom Trinity Score methodology",
                "dataset": [
                    {
                        "question": "What is Trinity Score?",
                        "answer": "Trinity Score evaluates AI systems across Truth, Goodness, Beauty, Serenity, and Eternity dimensions.",
                    },
                    {
                        "question": "How does LoRA work?",
                        "answer": "LoRA fine-tunes large language models by training only low-rank matrices instead of all parameters.",
                    },
                ],
                "num_candidates": 5,
                "max_bootstrapped_demos": 2,
                "num_trials": 10,
            }
        ]
    }


async def save_optimization_result(
    task: str, result: dict[str, Any], trinity_scores: dict[str, float]
):
    """Save optimization result to artifacts"""
    try:
        timestamp = int(time.time())
        filename = f"artifacts/dspy_optimization_{timestamp}.json"

        data = {
            "timestamp": timestamp,
            "task": task,
            "result": result,
            "trinity_scores": trinity_scores,
            "model_dump": result.get("optimized_module", {}),
        }

        Path("artifacts").mkdir(exist_ok=True)
        with open(filename, "w") as f:
            json.dump(data, f, indent=2, default=str)

        print(f"DSPy optimization result saved: {filename}")

    except Exception as e:
        print(f"Failed to save optimization result: {e}")


# Export for Chancellor Graph integration
__all__ = ["MIPROv2Optimizer", "optimize_prompt", "router"]
