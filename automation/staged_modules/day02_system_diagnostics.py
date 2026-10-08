"""
Day 2 Staged Module: System Diagnostics & Health Inspector Tools
"""
import os
from pathlib import Path

CODE_DIAGNOSTICS = '''"""
System Diagnostics Tools for MCP Agent Hub.
Provides real-time hardware, platform, disk, and network connectivity diagnostics.
"""
import os
import platform
import shutil
import socket
import time
from typing import Dict, Any

def get_system_specs() -> Dict[str, Any]:
    """Retrieve system hardware and OS environment details."""
    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count() or 1,
    }

def get_disk_usage(path: str = "/") -> Dict[str, Any]:
    """Inspect disk capacity and remaining space for the specified path."""
    total, used, free = shutil.disk_usage(path)
    return {
        "path": path,
        "total_gb": round(total / (2**30), 2),
        "used_gb": round(used / (2**30), 2),
        "free_gb": round(free / (2**30), 2),
        "percent_used": round((used / total) * 100, 1),
    }

def check_network_latency(host: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> Dict[str, Any]:
    """Measure TCP network socket connect latency to a target host and port."""
    start = time.perf_counter()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        return {"host": host, "port": port, "status": "online", "latency_ms": elapsed_ms}
    except Exception as err:
        return {"host": host, "port": port, "status": "unreachable", "error": str(err)}
'''

CODE_TOOLS_INIT = '''"""
Tool registry and exports for MCP Agent Hub.
"""
from typing import Callable, Dict
from mcp_agent_hub.tools.weather import get_alerts_tool, get_forecast_tool
from mcp_agent_hub.tools.diagnostics import get_system_specs, get_disk_usage, check_network_latency

TOOL_REGISTRY: Dict[str, Callable] = {
    "get_weather_alerts": get_alerts_tool,
    "get_weather_forecast": get_forecast_tool,
    "get_system_specs": get_system_specs,
    "get_disk_usage": get_disk_usage,
    "check_network_latency": check_network_latency,
}

__all__ = [
    "TOOL_REGISTRY",
    "get_alerts_tool",
    "get_forecast_tool",
    "get_system_specs",
    "get_disk_usage",
    "check_network_latency",
]
'''

def apply(repo_root: Path):
    diag_file = repo_root / "mcp_agent_hub" / "tools" / "diagnostics.py"
    diag_file.write_text(CODE_DIAGNOSTICS.strip() + "\\n")

    init_file = repo_root / "mcp_agent_hub" / "tools" / "__init__.py"
    init_file.write_text(CODE_TOOLS_INIT.strip() + "\\n")
    return "Added diagnostics.py and updated tool registry with hardware, disk, and network tools."
