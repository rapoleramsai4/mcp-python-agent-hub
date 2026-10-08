# 🌐 MCP Agent Hub

[![10-Day Automation](https://img.shields.io/badge/Progressive%20Automation-Active%20(10%20Days)-brightgreen.svg)](PROGRESS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Production-ready **Model Context Protocol (MCP)** server and agent client suite built in Python. Designed with a modular architecture supporting tools, dynamic context resources, structured prompt templates, and automated multi-day progressive feature deployments.

---

## 📖 Table of Contents
- [Architecture](#architecture)
- [10-Day Automated Progression](#10-day-automated-progression)
- [Quick Start](#quick-start)
- [Available Capabilities](#available-capabilities)
- [Claude Desktop Integration](#claude-desktop-integration)
- [Automation Runners](#automation-runners)

---

## 🏛️ Architecture

```
mcp-python-agent-hub/
├── .github/workflows/
│   └── daily-push.yml             # Cloud cron runner (12:00 UTC daily)
├── automation/
│   ├── daily_push.py              # Incremental release automation engine
│   ├── daily_push.sh              # Local shell execution runner
│   ├── setup_cron.sh              # Local Linux crontab installer
│   └── staged_modules/            # Features for Days 2 to 10
├── mcp_agent_hub/
│   ├── server.py                  # Core MCP Server (JSON-RPC 2.0 stdio loop)
│   ├── cli.py                     # CLI management and inspection entry point
│   ├── config.py                  # Runtime configuration and environment settings
│   ├── tools/                     # Modular tool registry (Weather, Diagnostics)
│   ├── resources/                 # Dynamic context providers (system://, logs://)
│   └── prompts/                   # Structured prompt templates
├── PROGRESS.md                    # 10-day live roadmap and completion status
└── CHANGELOG.md                   # Chronological version changes
```

---

## 📅 10-Day Automated Progression

This repository is powered by an automated progressive deployment engine that commits and pushes one major feature module each day for 10 days:

| Day | Feature Milestone | Status |
| :---: | :--- | :---: |
| **01** | Baseline MCP Multi-Service Architecture, Weather Suite & CLI | ✅ Completed |
| **02** | System Diagnostics & Real-time Health Inspector Tools | ⏳ Scheduled |
| **03** | Dynamic MCP Context Resources & System Log Streams | ⏳ Scheduled |
| **04** | Interactive Prompt Templates & Troubleshooting Workflows | ⏳ Scheduled |
| **05** | Enterprise Security Layer: Input Sanitization, Guardrails & Rate Limiting | ⏳ Scheduled |
| **06** | Comprehensive Pytest Suite & Automated Conformance Testing | ⏳ Scheduled |
| **07** | Interactive Terminal MCP Client & Autonomous Agent Sandbox | ⏳ Scheduled |
| **08** | High-Performance In-Memory Cache with TTL & Latency Telemetry | ⏳ Scheduled |
| **09** | Production Containerization (Docker/Compose) & Claude Desktop Integration | ⏳ Scheduled |
| **10** | Full Benchmark Suite, Architecture Diagrams & Release v1.0.0 | ⏳ Scheduled |

See [PROGRESS.md](PROGRESS.md) for live timestamps and details.

---

## 🚀 Quick Start

### 1. Inspect Server Capabilities
```bash
python3 -m mcp_agent_hub.cli --list-all
```

### 2. Test Tool Invocation
```bash
# Query active weather alerts
python3 -m mcp_agent_hub.cli --call-tool get_weather_alerts --args '{"state":"CA"}'

# Query forecast coordinates
python3 -m mcp_agent_hub.cli --call-tool get_weather_forecast --args '{"latitude": 37.7749, "longitude": -122.4194}'
```

### 3. Run MCP Server (stdio mode for AI agents / Claude)
```bash
python3 -m mcp_agent_hub.cli --run
```

---

## 🤖 Claude Desktop / Cursor IDE Integration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-agent-hub": {
      "command": "python3",
      "args": ["-m", "mcp_agent_hub.cli", "--run"],
      "cwd": "/path/to/mcp-python-agent-hub"
    }
  }
}
```

---

## 🔄 Daily Push Automation

The automation runs automatically via **GitHub Actions** every day at `12:00 UTC` without needing your machine to remain online.

### Manual / Local Execution
To trigger the next day's module release locally:
```bash
./automation/daily_push.sh
```

To view current automation status:
```bash
python3 automation/daily_push.py --status
```

To install local daily crontab scheduling:
```bash
./automation/setup_cron.sh
```
