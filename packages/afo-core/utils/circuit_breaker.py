"""
Circuit Breaker Pattern for AFO Kingdom
Prevents cascading failures by temporarily blocking calls to failing services.

States:
- CLOSED: Normal operation, requests pass through
- OPEN: Service failing, requests blocked immediately
- HALF_OPEN: Testing recovery, limited requests allowed
"""
from __future__ import annotations

import asyncio
import time
from enum import Enum
from functools import wraps
from typing import Any, Callable, Optional, TypeVar
from dataclasses import dataclass, field

T = TypeVar('T')


class CircuitState(Enum):
    """Circuit Breaker states."""
    CLOSED = "closed"      # Normal: requests pass through
    OPEN = "open"          # Failing: requests blocked
    HALF_OPEN = "half_open"  # Recovery: testing with limited requests


@dataclass
class CircuitStats:
    """Statistics for a circuit breaker."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None
    state_changes: int = 0


class CircuitBreaker:
    """
    Circuit Breaker implementation for async functions.
    
    Usage:
        circuit = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=30,
            service_name="ollama"
        )
        
        @circuit
        async def call_ollama(prompt: str):
            return await ollama_client.chat(prompt)
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        half_open_max_calls: int = 3,
        expected_exceptions: tuple = (Exception,),
        service_name: str = "unknown",
        on_open: Optional[Callable] = None,
        on_close: Optional[Callable] = None,
    ):
        """
        Initialize Circuit Breaker.
        
        Args:
            failure_threshold: Number of consecutive failures before opening
            recovery_timeout: Seconds to wait before attempting recovery
            half_open_max_calls: Max calls allowed in half-open state
            expected_exceptions: Exception types to count as failures
            service_name: Name for logging/metrics
            on_open: Callback when circuit opens (optional)
            on_close: Callback when circuit closes (optional)
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.expected_exceptions = expected_exceptions
        self.service_name = service_name
        self.on_open = on_open
        self.on_close = on_close
        
        # Internal state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: Optional[float] = None
        self._half_open_calls = 0
        self._lock = asyncio.Lock()
        self._stats = CircuitStats()

    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        return self._state

    @property
    def stats(self) -> CircuitStats:
        """Get circuit statistics."""
        return self._stats

    def _should_attempt_reset(self) -> bool:
        """Check if recovery timeout has passed."""
        if self._last_failure_time is None:
            return False
        return time.time() - self._last_failure_time >= self.recovery_timeout

    def _record_success(self) -> None:
        """Record a successful call."""
        self._stats.total_calls += 1
        self._stats.successful_calls += 1
        self._stats.last_success_time = time.time()

    def _record_failure(self) -> None:
        """Record a failed call."""
        self._stats.total_calls += 1
        self._stats.failed_calls += 1
        self._stats.last_failure_time = time.time()
        self._failure_count += 1
        self._last_failure_time = time.time()

    def _trip(self) -> None:
        """Open the circuit breaker."""
        self._state = CircuitState.OPEN
        self._stats.state_changes += 1
        print(f"🚨 [Circuit Breaker] {self.service_name}: OPEN (연속 {self._failure_count}회 실패)")
        if self.on_open:
            self.on_open(self)

    def _reset(self) -> None:
        """Close the circuit breaker."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._half_open_calls = 0
        self._stats.state_changes += 1
        print(f"✅ [Circuit Breaker] {self.service_name}: CLOSED (복구 완료)")
        if self.on_close:
            self.on_close(self)

    async def _enter_half_open(self) -> None:
        """Transition to half-open state."""
        self._state = CircuitState.HALF_OPEN
        self._half_open_calls = 0
        self._stats.state_changes += 1
        print(f"🔄 [Circuit Breaker] {self.service_name}: HALF_OPEN (복구 시도 중)")

    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute a function through the circuit breaker.
        
        Raises:
            CircuitBreakerOpenError: If circuit is open
            Original exception: If call fails
        """
        async with self._lock:
            # Check if we should transition from OPEN to HALF_OPEN
            if self._state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    await self._enter_half_open()
                else:
                    self._stats.rejected_calls += 1
                    remaining = self.recovery_timeout - (time.time() - self._last_failure_time)
                    raise CircuitBreakerOpenError(
                        f"[{self.service_name}] 서비스 일시 불가 (복구까지 {remaining:.0f}초)"
                    )
            
            # Check half-open call limit
            if self._state == CircuitState.HALF_OPEN:
                if self._half_open_calls >= self.half_open_max_calls:
                    self._stats.rejected_calls += 1
                    raise CircuitBreakerOpenError(
                        f"[{self.service_name}] 복구 테스트 진행 중 (잠시 대기)"
                    )
                self._half_open_calls += 1

        # Execute the call
        try:
            result = await func(*args, **kwargs)
            
            async with self._lock:
                self._record_success()
                if self._state == CircuitState.HALF_OPEN:
                    self._reset()
            
            return result
            
        except self.expected_exceptions as e:
            async with self._lock:
                self._record_failure()
                
                if self._state == CircuitState.HALF_OPEN:
                    # Failed during recovery - back to open
                    self._state = CircuitState.OPEN
                    print(f"❌ [Circuit Breaker] {self.service_name}: 복구 실패, 다시 OPEN")
                elif self._failure_count >= self.failure_threshold:
                    self._trip()
            
            raise

    def __call__(self, func: Callable) -> Callable:
        """Decorator interface for the circuit breaker."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await self.call(func, *args, **kwargs)
        
        # Attach circuit breaker info to the wrapper
        wrapper.circuit_breaker = self
        return wrapper

    def get_status(self) -> dict:
        """Get current status for monitoring."""
        return {
            "service": self.service_name,
            "state": self._state.value,
            "failure_count": self._failure_count,
            "failure_threshold": self.failure_threshold,
            "stats": {
                "total_calls": self._stats.total_calls,
                "successful": self._stats.successful_calls,
                "failed": self._stats.failed_calls,
                "rejected": self._stats.rejected_calls,
            },
            "recovery_timeout": self.recovery_timeout,
            "time_until_reset": max(
                0, 
                self.recovery_timeout - (time.time() - self._last_failure_time)
            ) if self._last_failure_time and self._state == CircuitState.OPEN else None
        }


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open and rejecting calls."""
    pass


# Pre-configured circuit breakers for AFO Kingdom services
ollama_circuit = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=60,
    service_name="ollama",
    expected_exceptions=(asyncio.TimeoutError, ConnectionError, Exception),
)

qdrant_circuit = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30,
    service_name="qdrant",
    expected_exceptions=(asyncio.TimeoutError, ConnectionError),
)

redis_circuit = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=15,
    service_name="redis",
    expected_exceptions=(ConnectionError,),
)


# Convenience functions
def get_all_circuit_statuses() -> dict:
    """Get status of all circuit breakers."""
    return {
        "ollama": ollama_circuit.get_status(),
        "qdrant": qdrant_circuit.get_status(),
        "redis": redis_circuit.get_status(),
    }


def reset_all_circuits() -> None:
    """Reset all circuit breakers (for testing/manual recovery)."""
    for circuit in [ollama_circuit, qdrant_circuit, redis_circuit]:
        circuit._reset()
    print("🔄 All circuit breakers reset")
