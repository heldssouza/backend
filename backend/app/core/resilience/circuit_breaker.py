from typing import Any, Callable
from functools import wraps
import time
import asyncio
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "CLOSED"  # Normal operation
    OPEN = "OPEN"     # Service unavailable
    HALF_OPEN = "HALF_OPEN"  # Testing if service is back


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        half_open_timeout: int = 30
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_timeout = half_open_timeout
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
        self.last_test_time = 0

    def can_execute(self) -> bool:
        """Check if the circuit breaker allows execution"""
        current_time = time.time()
        
        if self.state == CircuitState.CLOSED:
            return True
            
        if self.state == CircuitState.OPEN:
            if current_time - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.last_test_time = current_time
                return True
            return False
            
        if self.state == CircuitState.HALF_OPEN:
            if current_time - self.last_test_time >= self.half_open_timeout:
                return True
            return False
            
        return False

    def record_success(self):
        """Record a successful execution"""
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED

    def record_failure(self):
        """Record a failed execution"""
        current_time = time.time()
        
        if self.state == CircuitState.CLOSED:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                self.last_failure_time = current_time
                
        elif self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.last_failure_time = current_time


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: int = 60,
    half_open_timeout: int = 30
):
    """Circuit breaker decorator"""
    breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        half_open_timeout=half_open_timeout
    )
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            if not breaker.can_execute():
                logger.warning(f"Circuit breaker is {breaker.state.value} for {func.__name__}")
                raise Exception("Service is unavailable")
                
            try:
                result = await func(*args, **kwargs)
                breaker.record_success()
                return result
            except Exception as e:
                breaker.record_failure()
                logger.error(f"Circuit breaker recorded failure for {func.__name__}: {str(e)}")
                raise
                
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            if not breaker.can_execute():
                logger.warning(f"Circuit breaker is {breaker.state.value} for {func.__name__}")
                raise Exception("Service is unavailable")
                
            try:
                result = func(*args, **kwargs)
                breaker.record_success()
                return result
            except Exception as e:
                breaker.record_failure()
                logger.error(f"Circuit breaker recorded failure for {func.__name__}: {str(e)}")
                raise
                
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        
    return decorator
