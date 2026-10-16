FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV MCP_SERVER_NAME="mcp-agent-hub"
ENV MCP_LOG_LEVEL="INFO"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

COPY . .

ENTRYPOINT ["python3", "-m", "mcp_agent_hub.cli", "--run"]
