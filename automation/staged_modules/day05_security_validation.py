"""
Day 5 Staged Module: Security Layer & Input Validation
"""
from pathlib import Path

CODE_VALIDATOR = '''"""
Input sanitization and validation guards for MCP Agent Hub.
"""
import re
from pathlib import Path

class SecurityValidationError(ValueError):
    """Raised when user or agent input violates security boundaries."""
    pass

def sanitize_state_code(state: str) -> str:
    """Validate and sanitize US state postal code."""
    cleaned = state.strip().upper()
    if not re.match(r"^[A-Z]{2}$", cleaned):
        raise SecurityValidationError(f"Invalid state code '{state}'. Must be exactly 2 letters.")
    return cleaned

def validate_safe_path(path_str: str, allowed_base: str = "/") -> str:
    """Prevent directory traversal attacks."""
    resolved = Path(path_str).resolve()
    base = Path(allowed_base).resolve()
    if not str(resolved).startswith(str(base)):
        raise SecurityValidationError(f"Path traversal detected: '{path_str}' is outside base '{allowed_base}'.")
    return str(resolved)

def sanitize_hostname(host: str) -> str:
    """Validate hostname or IP to prevent injection."""
    cleaned = host.strip()
    if not re.match(r"^[a-zA-Z0-9.-]+$", cleaned):
        raise SecurityValidationError(f"Invalid hostname characters: '{host}'")
    return cleaned
'''

CODE_RATE_LIMITER = '''"""
Sliding window rate limiter for MCP tool calls.
"""
import time
from collections import defaultdict
from typing import Dict, List

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_id: str = "default") -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        # Clean older entries
        self.requests[client_id] = [t for t in self.requests[client_id] if t > window_start]
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        self.requests[client_id].append(now)
        return True

rate_limiter = SlidingWindowRateLimiter()
'''

CODE_SECURITY_INIT = '''"""
Security and validation package for MCP Agent Hub.
"""
from mcp_agent_hub.security.validator import (
    sanitize_state_code,
    validate_safe_path,
    sanitize_hostname,
    SecurityValidationError,
)
from mcp_agent_hub.security.rate_limiter import rate_limiter, SlidingWindowRateLimiter

__all__ = [
    "sanitize_state_code",
    "validate_safe_path",
    "sanitize_hostname",
    "SecurityValidationError",
    "rate_limiter",
    "SlidingWindowRateLimiter",
]
'''

def apply(repo_root: Path):
    sec_dir = repo_root / "mcp_agent_hub" / "security"
    sec_dir.mkdir(parents=True, exist_ok=True)
    
    (sec_dir / "validator.py").write_text(CODE_VALIDATOR.strip() + "\\n")
    (sec_dir / "rate_limiter.py").write_text(CODE_RATE_LIMITER.strip() + "\\n")
    (sec_dir / "__init__.py").write_text(CODE_SECURITY_INIT.strip() + "\\n")
    return "Added security validation package with path guards, input sanitizers, and sliding-window rate limiter."
