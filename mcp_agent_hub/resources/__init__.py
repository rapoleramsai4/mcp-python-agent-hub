"""
Resource registry and exports for MCP Agent Hub.
"""
from typing import Callable, Dict
from mcp_agent_hub.resources.system_resources import (
    get_system_metrics_resource,
    get_system_logs_resource,
    get_active_config_resource,
)

RESOURCE_REGISTRY: Dict[str, Callable] = {
    "system://metrics": get_system_metrics_resource,
    "logs://system": get_system_logs_resource,
    "config://active": get_active_config_resource,
}

__all__ = [
    "RESOURCE_REGISTRY",
    "get_system_metrics_resource",
    "get_system_logs_resource",
    "get_active_config_resource",
]
