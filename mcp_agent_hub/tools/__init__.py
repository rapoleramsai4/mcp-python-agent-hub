"""
Tool registry and exports for MCP Agent Hub.
"""
from typing import Callable, Dict
from mcp_agent_hub.tools.weather import get_alerts_tool, get_forecast_tool

TOOL_REGISTRY: Dict[str, Callable] = {
    "get_weather_alerts": get_alerts_tool,
    "get_weather_forecast": get_forecast_tool,
}

__all__ = ["TOOL_REGISTRY", "get_alerts_tool", "get_forecast_tool"]
