"""
Unit and integration test suite for MCP Agent Hub.
Tests tools, resources, prompts, and security validation.
"""
import asyncio
import json
import pytest

from mcp_agent_hub.server import MCPAgentServer
from mcp_agent_hub.tools.weather import get_alerts_tool, get_forecast_tool

def test_server_initialization():
    server = MCPAgentServer(name="test-server", version="1.0.0")
    caps = server.list_capabilities()
    assert caps["server"]["name"] == "test-server"
    assert "get_weather_alerts" in caps["tools"]
    assert "get_weather_forecast" in caps["tools"]

def test_tool_execution_weather_alerts():
    server = MCPAgentServer()
    # Runs async tool execution
    result = asyncio.run(server.execute_tool("get_weather_alerts", {"state": "TX"}))
    assert isinstance(result, str)
    assert len(result) > 0

def test_nonexistent_tool_raises_key_error():
    server = MCPAgentServer()
    with pytest.raises(KeyError):
        asyncio.run(server.execute_tool("nonexistent_tool", {}))

def test_diagnostics_tools_if_available():
    server = MCPAgentServer()
    if "get_system_specs" in server.tools:
        specs = asyncio.run(server.execute_tool("get_system_specs", {}))
        assert "cpu_count" in specs
        assert "platform" in specs

def test_resources_if_available():
    server = MCPAgentServer()
    if "system://metrics" in server.resources:
        content = asyncio.run(server.read_resource("system://metrics"))
        data = json.loads(content)
        assert "cpu_count" in data

def test_prompts_if_available():
    server = MCPAgentServer()
    if "system_troubleshooting" in server.prompts:
        prompt_text = asyncio.run(server.get_prompt("system_troubleshooting", {"component": "database"}))
        assert "database" in prompt_text
