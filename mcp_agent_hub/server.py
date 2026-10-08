"""
Core MCP Server implementation for MCP Agent Hub.
Supports standard MCP protocol over stdio and standalone inspection.
"""
import asyncio
import json
import logging
import sys
from typing import Any, Dict, List

from mcp_agent_hub.config import config
from mcp_agent_hub.tools import TOOL_REGISTRY
from mcp_agent_hub.resources import RESOURCE_REGISTRY
from mcp_agent_hub.prompts import PROMPT_REGISTRY

logging.basicConfig(level=getattr(logging, config.log_level.upper(), logging.INFO))
logger = logging.getLogger("mcp_agent_hub.server")


class MCPAgentServer:
    """Production MCP Server managing tools, resources, and prompt templates."""

    def __init__(self, name: str = "mcp-agent-hub", version: str = "0.1.0"):
        self.name = name
        self.version = version
        self.tools = dict(TOOL_REGISTRY)
        self.resources = dict(RESOURCE_REGISTRY)
        self.prompts = dict(PROMPT_REGISTRY)

    def register_tool(self, name: str, func: Any):
        self.tools[name] = func
        logger.info(f"Registered tool: {name}")

    def register_resource(self, uri: str, handler: Any):
        self.resources[uri] = handler
        logger.info(f"Registered resource: {uri}")

    def register_prompt(self, name: str, handler: Any):
        self.prompts[name] = handler
        logger.info(f"Registered prompt: {name}")

    def list_capabilities(self) -> Dict[str, Any]:
        return {
            "server": {"name": self.name, "version": self.version},
            "tools": list(self.tools.keys()),
            "resources": list(self.resources.keys()),
            "prompts": list(self.prompts.keys()),
        }

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        if tool_name not in self.tools:
            raise KeyError(f"Tool '{tool_name}' not found. Available: {list(self.tools.keys())}")
        tool_func = self.tools[tool_name]
        if asyncio.iscoroutinefunction(tool_func):
            return await tool_func(**arguments)
        return tool_func(**arguments)

    async def read_resource(self, uri: str) -> str:
        if uri not in self.resources:
            raise KeyError(f"Resource '{uri}' not found. Available: {list(self.resources.keys())}")
        handler = self.resources[uri]
        if asyncio.iscoroutinefunction(handler):
            return await handler()
        return handler()

    async def get_prompt(self, name: str, arguments: Dict[str, Any]) -> str:
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' not found. Available: {list(self.prompts.keys())}")
        handler = self.prompts[name]
        if asyncio.iscoroutinefunction(handler):
            return await handler(**arguments)
        return handler(**arguments)

    async def run_stdio(self):
        """Runs JSON-RPC 2.0 stdio server loop conforming to MCP specification."""
        logger.info(f"Starting {self.name} v{self.version} on stdio...")
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
        writer_transport, writer_protocol = await asyncio.get_event_loop().connect_write_pipe(
            asyncio.streams.FlowControlMixin, sys.stdout
        )
        writer = asyncio.StreamWriter(writer_transport, writer_protocol, reader, asyncio.get_event_loop())

        while True:
            line = await reader.readline()
            if not line:
                break
            try:
                request = json.loads(line.decode().strip())
                req_id = request.get("id")
                method = request.get("method")
                params = request.get("params", {})

                if method == "initialize":
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {"listChanged": True},
                                "resources": {"subscribe": False, "listChanged": True},
                                "prompts": {"listChanged": True},
                            },
                            "serverInfo": {"name": self.name, "version": self.version},
                        },
                    }
                elif method == "tools/list":
                    tool_list = [
                        {"name": name, "description": getattr(func, "__doc__", "") or f"Tool {name}"}
                        for name, func in self.tools.items()
                    ]
                    response = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tool_list}}
                elif method == "tools/call":
                    tool_name = params.get("name")
                    args = params.get("arguments", {})
                    output = await self.execute_tool(tool_name, args)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"content": [{"type": "text", "text": str(output)}]},
                    }
                elif method == "resources/list":
                    res_list = [{"uri": uri, "name": uri} for uri in self.resources.keys()]
                    response = {"jsonrpc": "2.0", "id": req_id, "result": {"resources": res_list}}
                elif method == "resources/read":
                    uri = params.get("uri")
                    content = await self.read_resource(uri)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"contents": [{"uri": uri, "mimeType": "text/plain", "text": content}]},
                    }
                elif method == "prompts/list":
                    prompt_list = [{"name": p, "description": p} for p in self.prompts.keys()]
                    response = {"jsonrpc": "2.0", "id": req_id, "result": {"prompts": prompt_list}}
                elif method == "prompts/get":
                    p_name = params.get("name")
                    p_args = params.get("arguments", {})
                    text = await self.get_prompt(p_name, p_args)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"messages": [{"role": "user", "content": {"type": "text", "text": text}}]},
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Method '{method}' not implemented"},
                    }

                writer.write((json.dumps(response) + "\n").encode())
                await writer.drain()
            except Exception as e:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if "request" in locals() and isinstance(request, dict) else None,
                    "error": {"code": -32000, "message": str(e)},
                }
                writer.write((json.dumps(err_resp) + "\n").encode())
                await writer.drain()


server = MCPAgentServer(name=config.server_name, version=config.version)

if __name__ == "__main__":
    asyncio.run(server.run_stdio())
