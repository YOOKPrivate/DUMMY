#!/bin/bash

# GitHub Updater Runner Script
# This script helps run the GitHub updater with common configurations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Default values
MODE="single"
INTERVAL=60
BASE_DIR="."
CONFIG_FILE=""

# Function to show usage
show_usage() {
    echo "GitHub Updater Runner"
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -t, --token TOKEN        GitHub personal access token (required)"
    echo "  -r, --repo REPO          Repository name in format owner/repo (required)"
    echo "  -m, --mode MODE          Run mode: single or continuous (default: single)"
    echo "  -i, --interval MINUTES   Interval for continuous mode in minutes (default: 60)"
    echo "  -d, --dir DIRECTORY      Base directory (default: current directory)"
    echo "  -c, --config FILE        Configuration file (optional)"
    echo "  -h, --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --token ghp_xxx --repo owner/repo"
    echo "  $0 --token ghp_xxx --repo owner/repo --mode continuous --interval 30"
    echo "  $0 --token ghp_xxx --repo owner/repo --config config.json"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--token)
            GITHUB_TOKEN="$2"
            shift 2
            ;;
        -r|--repo)
            GITHUB_REPO="$2"
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
        -d|--dir)
            BASE_DIR="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG_FILE="$2"
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

# Check for required parameters
if [[ -z "$GITHUB_TOKEN" ]]; then
    echo -e "${RED}Error: GitHub token is required${NC}"
    echo "Use --token or set GITHUB_TOKEN environment variable"
    exit 1
fi

if [[ -z "$GITHUB_REPO" ]]; then
    echo -e "${RED}Error: Repository name is required${NC}"
    echo "Use --repo or set GITHUB_REPO environment variable"
    exit 1
fi

# Check if Python and pip are available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed${NC}"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is required but not installed${NC}"
    exit 1
fi

# Install requirements if not already installed
echo -e "${YELLOW}Checking Python dependencies...${NC}"
if [[ -f "requirements.txt" ]]; then
    pip3 install -r requirements.txt
else
    echo -e "${YELLOW}requirements.txt not found, installing basic dependencies...${NC}"
    pip3 install PyGithub requests python-dotenv
fi

# Check if git is configured
if ! git config user.name &> /dev/null; then
    echo -e "${YELLOW}Warning: Git user.name is not configured${NC}"
    echo "Consider running: git config user.name 'Your Name'"
fi

if ! git config user.email &> /dev/null; then
    echo -e "${YELLOW}Warning: Git user.email is not configured${NC}"
    echo "Consider running: git config user.email 'your@email.com'"
fi

# Build command
CMD="python3 github_updater.py"
CMD="$CMD --token $GITHUB_TOKEN"
CMD="$CMD --repo $GITHUB_REPO"
CMD="$CMD --mode $MODE"
CMD="$CMD --interval $INTERVAL"
CMD="$CMD --base-dir $BASE_DIR"

if [[ -n "$CONFIG_FILE" ]]; then
    CMD="$CMD --config $CONFIG_FILE"
fi

# Show configuration
echo -e "${GREEN}GitHub Updater Configuration:${NC}"
echo "Repository: $GITHUB_REPO"
echo "Mode: $MODE"
echo "Base Directory: $BASE_DIR"
if [[ "$MODE" == "continuous" ]]; then
    echo "Interval: $INTERVAL minutes"
fi
echo ""

# Ask for confirmation if running in continuous mode
if [[ "$MODE" == "continuous" ]]; then
    echo -e "${YELLOW}Warning: Continuous mode will run indefinitely and make regular changes to your repository.${NC}"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Run the updater
echo -e "${GREEN}Starting GitHub Updater...${NC}"
echo "Command: $CMD"
echo ""

# Execute the command
exec $CMD