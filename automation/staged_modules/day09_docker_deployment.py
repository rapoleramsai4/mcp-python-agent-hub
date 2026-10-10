"""
Day 9 Staged Module: Containerization & Desktop Integration
"""
from pathlib import Path

DOCKERFILE = '''FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV MCP_SERVER_NAME="mcp-agent-hub"
ENV MCP_LOG_LEVEL="INFO"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

COPY . .

ENTRYPOINT ["python3", "-m", "mcp_agent_hub.cli", "--run"]
'''

DOCKER_COMPOSE = '''version: "3.8"

services:
  mcp-server:
    build: .
    container_name: mcp-agent-hub
    stdin_open: true
    tty: true
    restart: unless-stopped
    environment:
      - MCP_LOG_LEVEL=INFO
      - MCP_PORT=8000
'''

CLAUDE_CONFIG = '''{
  "mcpServers": {
    "mcp-agent-hub": {
      "command": "python3",
      "args": ["-m", "mcp_agent_hub.cli", "--run"],
      "env": {
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
'''

def apply(repo_root: Path):
    (repo_root / "Dockerfile").write_text(DOCKERFILE.strip() + "\n")
    (repo_root / "docker-compose.yml").write_text(DOCKER_COMPOSE.strip() + "\n")
    (repo_root / "claude_desktop_config.json").write_text(CLAUDE_CONFIG.strip() + "\n")
    return "Added Dockerfile, docker-compose.yml, and claude_desktop_config.json for instant Claude Desktop & Cursor integration."
