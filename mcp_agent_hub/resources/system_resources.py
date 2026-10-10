"""
MCP Resource providers for system state, live metrics, and configuration.
Allows LLMs to inspect server internals via resource URIs.
"""
import json
import os
import platform
import time
from typing import Dict, Any

def get_system_metrics_resource() -> str:
    """Returns real-time system metrics as JSON."""
    metrics = {
        "timestamp": time.time(),
        "cpu_count": os.cpu_count() or 1,
        "load_avg": os.getloadavg() if hasattr(os, "getloadavg") else [0, 0, 0],
        "pid": os.getpid(),
    }
    return json.dumps(metrics, indent=2)

def get_system_logs_resource() -> str:
    """Returns simulated server operational event log."""
    return f"""[{time.strftime("%Y-%m-%d %H:%M:%S")}] INFO: MCP Agent Hub operational.
[{time.strftime("%Y-%m-%d %H:%M:%S")}] INFO: Tool registry synchronized with {platform.system()}.
[{time.strftime("%Y-%m-%d %H:%M:%S")}] INFO: Context resource providers loaded successfully.
"""

def get_active_config_resource() -> str:
    """Returns currently active server configuration in JSON format."""
    from mcp_agent_hub.config import config
    return json.dumps({
        "server_name": config.server_name,
        "version": config.version,
        "log_level": config.log_level,
        "cache_ttl": config.cache_ttl_seconds,
        "rate_limit_rpm": config.rate_limit_rpm,
    }, indent=2)
