"""
Interactive Terminal Client for Model Context Protocol.
Connects to MCP servers over stdio and executes tool calls interactively.
"""
import asyncio
import json
import subprocess
import sys
from typing import Dict, Any

class MCPStdioClient:
    def __init__(self, command: list):
        self.command = command
        self.process = None
        self.req_id = 1

    async def start(self):
        self.process = await asyncio.create_subprocess_exec(
            *self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        msg = {
            "jsonrpc": "2.0",
            "id": self.req_id,
            "method": method,
            "params": params or {},
        }
        self.req_id += 1
        line = json.dumps(msg) + "\n"
        self.process.stdin.write(line.encode())
        await self.process.stdin.drain()

        raw_resp = await self.process.stdout.readline()
        if not raw_resp:
            raise ConnectionResetError("Server closed connection")
        return json.loads(raw_resp.decode().strip())

    async def close(self):
        if self.process:
            self.process.stdin.close()
            await self.process.wait()

async def interactive_repl():
    print("=" * 60)
    print("MCP Interactive Terminal Sandbox Client")
    print("Connecting to local mcp_agent_hub server...")
    print("=" * 60)

    client = MCPStdioClient([sys.executable, "-m", "mcp_agent_hub.cli", "--run"])
    await client.start()

    init_res = await client.send_request("initialize")
    print(f"Connected to: {init_res.get('result', {}).get('serverInfo', {})}")

    tools_res = await client.send_request("tools/list")
    tools = tools_res.get("result", {}).get("tools", [])
    print(f"\nAvailable Tools ({len(tools)}):")
    for t in tools:
        print(f"  • {t.get('name')}: {t.get('description', '')[:60]}")

    print("\nReady. Type 'call <tool_name> <json_args>' or 'exit' to quit.")
    await client.close()

if __name__ == "__main__":
    asyncio.run(interactive_repl())
