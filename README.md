# GitHub Repository Automation System

This repository contains an automated system that periodically performs various GitHub activities including creating content, committing changes, raising issues, and managing pull requests.

## Features

- **Random Content Generation**: Creates various types of files (Markdown, JSON, Python, JavaScript, text)
- **Automatic Git Operations**: Commits and pushes changes automatically
- **GitHub Issue Management**: Creates random issues with realistic content
- **Pull Request Workflow**: Creates branches, makes changes, creates PRs, and merges them
- **Configurable Scheduling**: Run once or continuously with customizable intervals
- **Comprehensive Logging**: Detailed logs of all operations

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Git configured with push access to the repository
- GitHub Personal Access Token with repository permissions

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your GitHub token:
```bash
cp .env.example .env
# Edit .env and add your GitHub token and repository name
```

### Usage

#### Method 1: Using the convenience script

```bash
# Single run
./run_updater.sh --token your_github_token --repo owner/repo-name

# Continuous mode (runs every 60 minutes)
./run_updater.sh --token your_github_token --repo owner/repo-name --mode continuous

# Custom interval (every 30 minutes)
./run_updater.sh --token your_github_token --repo owner/repo-name --mode continuous --interval 30
```

#### Method 2: Direct Python execution

```bash
# Single run
python3 github_updater.py --token your_github_token --repo owner/repo-name

# Continuous mode
python3 github_updater.py --token your_github_token --repo owner/repo-name --mode continuous --interval 60
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
GITHUB_TOKEN=your_personal_access_token
GITHUB_REPO=owner/repository-name
UPDATE_INTERVAL_MINUTES=60
```

### Configuration File

Customize behavior using `config.json`:

```json
{
  "automation": {
    "interval_minutes": 60,
    "activities": {
      "create_content": true,
      "create_issues": true,
      "create_prs": true
    }
  },
  "limits": {
    "max_files_per_cycle": 3,
    "max_issues_per_day": 5,
    "max_prs_per_day": 3
  }
}
```

## What It Does

### Content Generation
- Creates random files in various formats (`.md`, `.json`, `.txt`, `.py`, `.js`)
- Generates realistic content with timestamps and metadata
- Uses templates to ensure variety and authenticity

### Git Operations
- Automatically stages and commits new files
- Pushes changes to the main branch
- Uses descriptive commit messages

### GitHub Integration
- Creates issues with realistic titles and descriptions
- Applies appropriate labels to issues
- Creates feature branches for pull requests
- Generates PR descriptions with checklists
- Automatically merges PRs after creation

### Branch Management
- Creates temporary feature branches
- Pushes changes to branches
- Cleans up branches after merging
- Handles conflicts and errors gracefully

## File Structure

```
.
├── github_updater.py      # Main automation script
├── requirements.txt       # Python dependencies
├── config.json           # Configuration settings
├── .env.example          # Environment variables template
├── run_updater.sh        # Convenience runner script
├── setup.py              # Package setup
└── README.md             # This file
```

## Command Line Options

```
python3 github_updater.py [OPTIONS]

Options:
  --token TOKEN            GitHub personal access token (required)
  --repo REPO             Repository name in format owner/repo (required)
  --mode {single,continuous}  Run mode (default: single)
  --interval MINUTES      Interval for continuous mode (default: 60)
  --base-dir DIR          Repository base directory (default: .)
```

## GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with these permissions:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
3. Copy the token and use it with the `--token` parameter

## Safety Features

- Comprehensive error handling and logging
- Graceful fallback when operations fail
- Automatic cleanup of temporary branches
- Configurable limits to prevent spam
- Dry-run mode available in configuration

## Logging

All operations are logged to:
- Console output (real-time)
- `github_updater.log` file (persistent)

Log levels: INFO, WARNING, ERROR

## Troubleshooting

### Common Issues

1. **Permission denied**: Ensure your GitHub token has sufficient permissions
2. **Git authentication failed**: Configure git with your credentials
3. **Branch conflicts**: Script automatically handles most conflicts
4. **Rate limiting**: GitHub API has rate limits; continuous mode respects these

### Debug Mode

Enable verbose logging by modifying the logging configuration in the script.

## Contributing

This is an automation tool designed for testing and development. Use responsibly and ensure you have permission to modify the target repository.

## License

MIT License - see individual files for details.

## Warning

This tool will make real changes to your GitHub repository. Use with caution and test in a development repository first.
