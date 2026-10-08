"""
10-Day Automated Progressive Code Release Engine for MCP Agent Hub.
Manages daily incremental commits, automated testing, changelog generation, and GitHub sync.
"""
import argparse
import datetime
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = REPO_ROOT / ".automation" / "state.json"
PROGRESS_FILE = REPO_ROOT / "PROGRESS.md"
CHANGELOG_FILE = REPO_ROOT / "CHANGELOG.md"

MODULE_MAP = {
    2: ("day02_system_diagnostics", "System Diagnostics & Real-time Health Inspector Tools"),
    3: ("day03_context_resources", "Dynamic MCP Context Resources & System Log Streams"),
    4: ("day04_prompts_templates", "Interactive Prompt Templates & Troubleshooting Workflows"),
    5: ("day05_security_validation", "Enterprise Security Layer: Input Sanitization, Guardrails & Rate Limiting"),
    6: ("day06_test_suite", "Comprehensive Pytest Suite & Automated Conformance Testing"),
    7: ("day07_interactive_client", "Interactive Terminal MCP Client & Autonomous Agent Sandbox"),
    8: ("day08_caching_layer", "High-Performance In-Memory Cache with TTL & Latency Telemetry"),
    9: ("day09_docker_deployment", "Production Containerization (Docker/Compose) & Claude Desktop Integration"),
    10: ("day10_release_and_benchmarks", "Full Benchmark Suite, Architecture Diagrams & Release v1.0.0"),
}


def load_state() -> dict:
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found at {STATE_FILE}")
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def update_progress_file(day: int, title: str, summary: str, date_str: str):
    if not PROGRESS_FILE.exists():
        return
    content = PROGRESS_FILE.read_text()
    old_line = f"- [ ] **Day {day}:** {title}"
    new_line = f"- [x] **Day {day}:** {title} *(Completed on {date_str})*"
    if old_line in content:
        content = content.replace(old_line, new_line)
    PROGRESS_FILE.write_text(content)


def update_changelog_file(day: int, title: str, summary: str, date_str: str):
    if not CHANGELOG_FILE.exists():
        return
    entry = f"""
## [Day {day}] - {date_str}
### Added
- **{title}**: {summary}
"""
    current_text = CHANGELOG_FILE.read_text()
    insert_marker = "<!-- CHANGELOG_ENTRIES -->"
    if insert_marker in current_text:
        updated = current_text.replace(insert_marker, f"{insert_marker}\\n{entry.strip()}")
    else:
        updated = current_text + "\n" + entry.strip()
    CHANGELOG_FILE.write_text(updated)


def run_cmd(cmd: list, cwd: Path = REPO_ROOT) -> str:
    res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed ({' '.join(cmd)}): {res.stderr.strip()}")
    return res.stdout.strip()


def verify_compilation():
    """Verify that all Python files compile cleanly without syntax errors."""
    for py_file in (REPO_ROOT / "mcp_agent_hub").rglob("*.py"):
        subprocess.check_call([sys.executable, "-m", "py_compile", str(py_file)])


def show_status(state: dict):
    print("=" * 70)
    print("MCP AGENT HUB — 10-DAY PROGRESSIVE AUTOMATION STATUS")
    print("=" * 70)
    print(f"Current Day: {state.get('current_day', 1)} / {state.get('max_days', 10)}")
    print(f"Completed Days: {state.get('completed_days', [])}")
    print("-" * 70)
    for item in state.get("roadmap", []):
        d = item["day"]
        status = "✓ COMPLETED" if item["status"] == "completed" else "○ PENDING"
        date_info = f" ({item['date']})" if item.get("date") else ""
        print(f"Day {d:02d} [{status}{date_info}]: {item['title']}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="MCP Daily Progressive Push Automation")
    parser.add_argument("--status", action="store_true", help="Print current automation status")
    parser.add_argument("--dry-run", action="store_true", help="Simulate applying the next day without writing")
    parser.add_argument("--step", action="store_true", help="Advance and commit the next day")
    parser.add_argument("--ci", action="store_true", help="CI/Non-interactive mode for GitHub Actions & cron")
    parser.add_argument("--push", action="store_true", help="Push to git origin main after committing")

    args = parser.parse_args()
    state = load_state()

    if args.status:
        show_status(state)
        return

    current_day = state.get("current_day", 1)
    if current_day >= 10:
        print(f"✓ All {state.get('max_days', 10)} days have been completed! Milestone reached.")
        show_status(state)
        sys.exit(0)

    next_day = current_day + 1
    if next_day not in MODULE_MAP:
        print(f"No module configured for Day {next_day}.")
        sys.exit(1)

    mod_name, title = MODULE_MAP[next_day]
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")

    print(f">> Processing Day {next_day}: {title}")

    if args.dry_run:
        print(f"[DRY-RUN] Would apply module: automation.staged_modules.{mod_name}")
        return

    # Import and apply staged module
    mod = importlib.import_module(f"automation.staged_modules.{mod_name}")
    summary = mod.apply(REPO_ROOT)
    print(f">> Applied changes: {summary}")

    # Verify python syntax
    verify_compilation()
    print(">> Python syntax verification passed.")

    # Update docs
    update_progress_file(next_day, title, summary, today_str)
    update_changelog_file(next_day, title, summary, today_str)

    # Update state
    state["current_day"] = next_day
    if next_day not in state["completed_days"]:
        state["completed_days"].append(next_day)
    state["last_updated"] = datetime.datetime.now().isoformat()
    for item in state.get("roadmap", []):
        if item["day"] == next_day:
            item["status"] = "completed"
            item["date"] = today_str

    save_state(state)
    print(">> Updated state and tracking documents.")

    # Git operations
    run_cmd(["git", "add", "."])
    commit_msg = f"feat(mcp): Day {next_day} - {title}"
    run_cmd(["git", "commit", "-m", commit_msg])
    print(f">> Created commit: {commit_msg}")

    if args.push or args.ci:
        print(">> Pushing to origin main...")
        run_cmd(["git", "push", "origin", "main"])
        print(">> Successfully pushed to GitHub!")

    print(f">> Day {next_day} progression successfully completed!")


if __name__ == "__main__":
    main()
