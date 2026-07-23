from collections.abc import Callable
from functools import wraps
from threading import RLock
from time import monotonic
from typing import Any, TypeVar

from schemas.weather import ServiceError


T = TypeVar("T")


def ttl_cache(ttl_seconds: int) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Cache successful service results in memory for a fixed duration."""
    def decorator(function: Callable[..., T]) -> Callable[..., T]:
        cache: dict[tuple[Any, ...], tuple[float, T]] = {}
        lock = RLock()

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = args + tuple(sorted(kwargs.items()))
            now = monotonic()
            with lock:
                cached = cache.get(key)
                if cached and now - cached[0] < ttl_seconds:
                    return cached[1]

            result = function(*args, **kwargs)
            if not isinstance(result, ServiceError):
                with lock:
                    cache[key] = (now, result)
            return result

        def cache_clear() -> None:
            with lock:
                cache.clear()

        wrapper.cache_clear = cache_clear  # type: ignore[attr-defined]
        return wrapper

    return decorator
