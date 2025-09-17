#!/bin/bash

# Setup cron job for GitHub updater to run every hour
# This script will add a cron job that runs the GitHub updater every hour

SCRIPT_DIR="/home/oyyk/projects/dummy"
PYTHON_PATH=$(which python3)
LOG_FILE="$SCRIPT_DIR/github_updater.log"

echo "Setting up hourly cron job for GitHub updater..."

# Create the cron job entry
CRON_JOB="0 * * * * cd $SCRIPT_DIR && $PYTHON_PATH github_updater.py --mode single >> $LOG_FILE 2>&1"

# Add the cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "Cron job added successfully!"
echo "The GitHub updater will now run every hour at minute 0"
echo "Logs will be written to: $LOG_FILE"
echo ""
echo "To verify the cron job was added, run: crontab -l"
echo "To remove the cron job later, run: crontab -e and delete the line"