"""
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
