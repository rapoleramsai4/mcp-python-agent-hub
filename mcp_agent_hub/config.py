"""
Configuration management for MCP Agent Hub.
Supports environment variables and default runtime options.
"""
import os
from dataclasses import dataclass

@dataclass
class ServerConfig:
    server_name: str = os.getenv("MCP_SERVER_NAME", "mcp-agent-hub")
    version: str = os.getenv("MCP_SERVER_VERSION", "0.1.0")
    log_level: str = os.getenv("MCP_LOG_LEVEL", "INFO")
    host: str = os.getenv("MCP_HOST", "0.0.0.0")
    port: int = int(os.getenv("MCP_PORT", "8000"))
    user_agent: str = os.getenv("MCP_USER_AGENT", "mcp-agent-hub/1.0 (contact@rapoleramsai4.dev)")
    cache_ttl_seconds: int = int(os.getenv("MCP_CACHE_TTL", "300"))
    rate_limit_rpm: int = int(os.getenv("MCP_RATE_LIMIT_RPM", "60"))

config = ServerConfig()
