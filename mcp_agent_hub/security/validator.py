"""
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
