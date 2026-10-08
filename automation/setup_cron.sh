#!/usr/bin/env bash
# Helper script to install a daily crontab entry for local execution
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAILY_SCRIPT="$SCRIPT_DIR/daily_push.sh"
LOG_FILE="$SCRIPT_DIR/cron.log"

CRON_TIME="0 12 * * *" # Every day at 12:00 local time
CRON_JOB="$CRON_TIME $DAILY_SCRIPT >> $LOG_FILE 2>&1"

echo "Configuring local crontab for daily push automation..."
echo "Cron job command: $CRON_JOB"

# Check if job already exists
if crontab -l 2>/dev/null | grep -Fq "$DAILY_SCRIPT"; then
    echo "✓ Cron job is already installed in crontab."
else
    (crontab -l 2>/dev/null || true; echo "$CRON_JOB") | crontab -
    echo "✓ Successfully installed daily cron job into crontab!"
fi

echo "Current crontab entries:"
crontab -l | grep -F "$DAILY_SCRIPT" || true
