# Trinity Score: 90.0 (Prophecied)
"""
AFO Kingdom DSPy Optimizer (MIPROv2 Integration)
眞 (Truth) - 데이터 기반의 투명한 프롬프트 최적화
美 (Beauty) - 우아한 추상화 및 모듈 설계

Author: AFO Kingdom Development Team (Chancellor)
Date: 2026-01-01
Version: 1.0.0
"""

import logging
from typing import Any

import dspy

try:
    from dspy.teleprompt import MIPROv2
except ImportError:
    # Fallback to dspy.MIPROv2 if teleprompt locations change (robustness)
    try:
        from dspy import MIPROv2
    except ImportError:
        MIPROv2 = None

logger = logging.getLogger(__name__)


class MIPROOptimizer:
    """
    MIPROv2 (Multi-Input Prompt Optimization) Wrapper

    Attributes:
        model: DSPy language model (Teacher/Student)
        metric: Optimization metric function
    """

    def __init__(self, model: dspy.LM, metric: Any):
        """
        Initialize the optimizer.

        Args:
            model: The language model to use.
            metric: The metric function to optimize against.
        """
        if MIPROv2 is None:
            raise ImportError("DSPy MIPROv2 not found. Ensure dspy-ai is installed.")

        self.model = model
        self.metric = metric
        logger.info(f"Initialized MIPROOptimizer with model {model} and metric {metric}")

    def optimize(
        self,
        program: dspy.Module,
        trainset: list[dspy.Example],
        num_candidates: int = 10,
        num_threads: int = 4,
        max_bootstrapped_demos: int = 4,
        max_labeled_demos: int = 4,
    ) -> dspy.Module:
        """
        Optimize the given program using MIPROv2.

        Args:
            program: The DSPy program to optimize.
            trainset: Training dataset.
            num_candidates: Number of instruction candidates to generate.
            num_threads: Number of threads for parallel evaluation.

        Returns:
            Optimized DSPy program.
        """
        try:
            logger.info("Starting MIPROv2 optimization...")
            teleprompter = MIPROv2(
                prompt_model=self.model,
                task_model=self.model,
                metric=self.metric,
                num_candidates=num_candidates,
            )

            optimized_program = teleprompter.compile(
                program,
                trainset=trainset,
                num_trials=num_candidates,
                max_bootstrapped_demos=max_bootstrapped_demos,
                max_labeled_demos=max_labeled_demos,
                eval_kwargs={"num_threads": num_threads},
            )

            logger.info("MIPROv2 optimization completed successfully.")
            return optimized_program

        except Exception as e:
            logger.error(f"Optimization failed: {e!s}")
            raise

    def save_program(self, program: dspy.Module, path: str) -> None:
        """Save the optimized program."""
        program.save(path)
        logger.info(f"Saved optimized program to {path}")

    def load_program(self, program: dspy.Module, path: str) -> dspy.Module:
        """Load an optimized program."""
        program.load(path)
        logger.info(f"Loaded optimized program from {path}")
        return program
