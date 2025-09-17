#!/bin/bash

# Simple GitHub Updater Runner using config.json
# This script runs the GitHub updater using configuration from config.json

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Default values
CONFIG_FILE="config.json"
MODE=""
INTERVAL=""

# Function to show usage
show_usage() {
    echo "GitHub Updater Config Runner"
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "This script uses config.json for configuration by default."
    echo ""
    echo "Options:"
    echo "  -c, --config FILE        Configuration file path (default: config.json)"
    echo "  -m, --mode MODE          Override mode: single or continuous"
    echo "  -i, --interval MINUTES   Override interval for continuous mode"
    echo "  -h, --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                       # Use config.json with default settings"
    echo "  $0 --mode continuous     # Force continuous mode"
    echo "  $0 --mode single         # Force single run mode"
    echo "  $0 --config custom.json  # Use custom config file"
    echo ""
    echo "Config file format (config.json):"
    echo '  {'
    echo '    "github": {'
    echo '      "repo_name": "owner/repo",'
    echo '      "token": "your_github_token"'
    echo '    },'
    echo '    "automation": {'
    echo '      "interval_minutes": 60'
    echo '    }'
    echo '  }'
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -i|--interval)
            INTERVAL="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
done

# Check if config file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo -e "${RED}Error: Configuration file '$CONFIG_FILE' not found${NC}"
    echo "Create a config.json file or specify a different config file with --config"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed${NC}"
    exit 1
fi

# Install requirements if not already installed
echo -e "${YELLOW}Checking Python dependencies...${NC}"
if [[ -f "requirements.txt" ]]; then
    pip3 install -r requirements.txt > /dev/null 2>&1
fi

# Check if git is configured
if ! git config user.name &> /dev/null; then
    echo -e "${YELLOW}Warning: Git user.name is not configured${NC}"
fi

if ! git config user.email &> /dev/null; then
    echo -e "${YELLOW}Warning: Git user.email is not configured${NC}"
fi

# Build command
CMD="python3 github_updater.py --config $CONFIG_FILE"

if [[ -n "$MODE" ]]; then
    CMD="$CMD --mode $MODE"
fi

if [[ -n "$INTERVAL" ]]; then
    CMD="$CMD --interval $INTERVAL"
fi

# Show configuration
echo -e "${GREEN}GitHub Updater Starting...${NC}"
echo "Config file: $CONFIG_FILE"
if [[ -n "$MODE" ]]; then
    echo "Mode override: $MODE"
fi
if [[ -n "$INTERVAL" ]]; then
    echo "Interval override: $INTERVAL minutes"
fi
echo ""

# Run the updater
echo -e "${GREEN}Command: $CMD${NC}"
echo ""

# Execute the command
exec $CMD