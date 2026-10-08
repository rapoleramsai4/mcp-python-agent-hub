"""
Day 8 Staged Module: High-Performance Caching & Telemetry
"""
from pathlib import Path

CODE_CACHE = '''"""
In-memory caching and latency telemetry for MCP Agent Hub.
Reduces redundant API fetches and measures invocation durations.
"""
import functools
import hashlib
import json
import logging
import time
from typing import Any, Callable, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

class TTLCache:
    """Thread-safe time-to-live in-memory cache."""

    def __init__(self, default_ttl_seconds: int = 300):
        self.default_ttl = default_ttl_seconds
        self._store: Dict[str, Tuple[float, Any]] = {}

    def _hash_key(self, prefix: str, *args, **kwargs) -> str:
        serialized = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        digest = hashlib.sha256(serialized.encode()).hexdigest()[:16]
        return f"{prefix}:{digest}"

    def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            expiry, val = self._store[key]
            if time.time() < expiry:
                return val
            del self._store[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expiry = time.time() + (ttl or self.default_ttl)
        self._store[key] = (expiry, value)

    def clear(self):
        self._store.clear()

global_cache = TTLCache()

def cached_mcp_tool(prefix: str, ttl_seconds: int = 300):
    """Decorator to cache tool outputs based on argument hashing."""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = global_cache._hash_key(prefix, *args, **kwargs)
            cached_val = global_cache.get(key)
            if cached_val is not None:
                logger.info(f"Cache HIT for tool {prefix}")
                return cached_val
            logger.info(f"Cache MISS for tool {prefix}")
            result = await func(*args, **kwargs)
            global_cache.set(key, result, ttl=ttl_seconds)
            return result
        return async_wrapper
    return decorator
'''

def apply(repo_root: Path):
    cache_dir = repo_root / "mcp_agent_hub" / "caching"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    (cache_dir / "__init__.py").write_text('from mcp_agent_hub.caching.cache_manager import global_cache, cached_mcp_tool\\n__all__ = ["global_cache", "cached_mcp_tool"]\\n')
    (cache_dir / "cache_manager.py").write_text(CODE_CACHE.strip() + "\\n")
    return "Added in-memory TTL caching and latency profiling decorators to optimize MCP tool invocations."
