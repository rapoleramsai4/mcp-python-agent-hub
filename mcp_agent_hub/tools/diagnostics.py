"""
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
