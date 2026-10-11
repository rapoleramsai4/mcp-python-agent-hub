# Changelog

All notable changes to this project are documented in this file across the 10-day progressive development lifecycle.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

<!-- CHANGELOG_ENTRIES -->
## [Day 4] - 2026-10-11
### Added
- **Interactive Prompt Templates & Troubleshooting Workflows**: Added templates.py and registered system_troubleshooting and code_review prompt templates.
## [Day 3] - 2026-10-10
### Added
- **Dynamic MCP Context Resources & System Log Streams**: Added system_resources.py and registered system://metrics, logs://system, and config://active MCP resources.
## [Day 2] - 2026-10-10
### Added
- **System Diagnostics & Real-time Health Inspector Tools**: Added diagnostics.py and updated tool registry with hardware, disk, and network tools.

## [Day 1] - 2026-10-08
### Added
- **Core MCP Architecture**: JSON-RPC 2.0 stdio server loop conforming to Model Context Protocol standards.
- **Weather Tool Suite**: Integrated NWS alert and forecast tools with standard library fallbacks.
- **Unified CLI**: Command-line interface with `--list-all`, `--list-tools`, `--call-tool`, and `--run`.
- **10-Day Automated Staging Engine**: GitHub Actions workflow and local runners for daily feature releases.
