"""
Interactive Prompt Templates for MCP Agent Hub.
Exposes structured workflows for LLMs to diagnose issues and review code.
"""
from typing import Dict, Any

def system_troubleshooting_prompt(component: str = "all", urgency: str = "normal") -> str:
    """Prompt template guiding an LLM through systematic server troubleshooting."""
    return f"""You are an expert Site Reliability Engineer analyzing the {component} subsystem.
Urgency Level: {urgency.upper()}

Please execute the following investigation workflow:
1. Call `get_system_specs` to inspect current host architecture and CPU capacity.
2. Call `get_disk_usage` with path="/" to detect storage exhaustion.
3. Call `check_network_latency` to verify upstream gateway connectivity.
4. Read the `system://metrics` and `logs://system` resources to inspect runtime state.
5. Formulate a root-cause hypothesis and provide actionable remediation commands.
"""

def code_review_prompt(language: str = "python", focus: str = "security") -> str:
    """Prompt template for automated code review focusing on security and performance."""
    return f"""You are a Principal Software Engineer performing a {focus} review for a {language} codebase.

Follow these strict review principles:
- Validate input sanitization and boundary checks.
- Identify potential resource exhaustion (memory leaks, unclosed handles).
- Verify conformance to Model Context Protocol (MCP) standards.
- Propose concrete diffs with explanatory reasoning.
"""
