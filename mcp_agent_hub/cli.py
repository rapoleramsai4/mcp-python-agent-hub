"""
CLI Entry point for MCP Agent Hub.
Allows running the server, listing capabilities, and inspecting tools.
"""
import argparse
import asyncio
import json
import sys

from mcp_agent_hub.server import server


def main():
    parser = argparse.ArgumentParser(description="MCP Agent Hub - Model Context Protocol Server & Agent")
    parser.add_argument("--list-tools", action="store_true", help="List all registered tools")
    parser.add_argument("--list-all", action="store_true", help="List all capabilities (tools, resources, prompts)")
    parser.add_argument("--call-tool", type=str, help="Call a tool by name (provide JSON arguments with --args)")
    parser.add_argument("--args", type=str, default="{}", help="JSON arguments for tool call")
    parser.add_argument("--run", action="store_true", help="Run MCP server over stdio")

    args = parser.parse_args()

    if args.list_tools:
        print(f"Registered Tools ({len(server.tools)}):")
        for name in server.tools:
            print(f"  • {name}")
        return

    if args.list_all:
        caps = server.list_capabilities()
        print(json.dumps(caps, indent=2))
        return

    if args.call_tool:
        try:
            kwargs = json.loads(args.args)
        except json.JSONDecodeError as err:
            print(f"Error parsing --args JSON: {err}", file=sys.stderr)
            sys.exit(1)
        result = asyncio.run(server.execute_tool(args.call_tool, kwargs))
        print(result)
        return

    # Default to running stdio server if --run or no args
    asyncio.run(server.run_stdio())


if __name__ == "__main__":
    main()
