"""
Prompt registry and exports for MCP Agent Hub.
"""
from typing import Callable, Dict
from mcp_agent_hub.prompts.templates import (
    system_troubleshooting_prompt,
    code_review_prompt,
)

PROMPT_REGISTRY: Dict[str, Callable] = {
    "system_troubleshooting": system_troubleshooting_prompt,
    "code_review": code_review_prompt,
}

__all__ = [
    "PROMPT_REGISTRY",
    "system_troubleshooting_prompt",
    "code_review_prompt",
]
