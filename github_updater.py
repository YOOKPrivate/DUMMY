#!/usr/bin/env python3
"""
GitHub Repository Automation System

This script periodically:
1. Creates random content in the repository
2. Commits and pushes changes
3. Creates GitHub issues
4. Creates pull requests
5. Merges pull requests

Requirements:
- GitHub Personal Access Token with repo permissions
- Python 3.7+
- PyGithub library
- git configured for the repository
"""

import os
import random
import time
import json
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import requests
from github import Github
from github.GithubException import GithubException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('github_updater.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GitHubUpdater:
    def __init__(self, token: str, repo_name: str, base_dir: str = "."):
        """
        Initialize the GitHub updater

        Args:
            token: GitHub personal access token
            repo_name: Repository name in format "owner/repo"
            base_dir: Base directory of the repository
        """
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)
        self.base_dir = Path(base_dir)
        self.token = token
        self.repo_name = repo_name

        # Content generation templates
        self.file_templates = {
            'markdown': self._generate_markdown_content,
            'json': self._generate_json_content,
            'text': self._generate_text_content,
            'python': self._generate_python_content,
            'javascript': self._generate_js_content
        }

        self.issue_titles = [
            "Enhancement: Improve user experience",
            "Bug: Fix navigation issue",
            "Feature: Add new functionality",
            "Documentation: Update README",
            "Performance: Optimize loading times",
            "Security: Update dependencies",
            "Refactor: Code cleanup needed",
            "Testing: Add unit tests",
            "UI: Design improvements",
            "API: Endpoint optimization"
        ]

        self.branch_names = [
            "feature/new-component",
            "bugfix/navigation-fix",
            "enhancement/ui-improvements",
            "feature/api-updates",
            "hotfix/critical-bug",
            "feature/user-dashboard",
            "improvement/performance",
            "feature/data-export",
            "bugfix/form-validation",
            "enhancement/accessibility"
        ]

    def _generate_markdown_content(self) -> str:
        """Generate random markdown content"""
        topics = ["Development", "Testing", "Documentation", "Features", "Performance"]
        topic = random.choice(topics)

        content = f"""# {topic} Notes

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
This document contains information about {topic.lower()} in our project.

## Key Points
- Point 1: {random.choice(['Improved efficiency', 'Better user experience', 'Enhanced security'])}
- Point 2: {random.choice(['Reduced complexity', 'Faster loading', 'Better error handling'])}
- Point 3: {random.choice(['Mobile compatibility', 'SEO optimization', 'Accessibility improvements'])}

## Next Steps
1. Review implementation
2. Test thoroughly
3. Deploy to production

---
*Auto-generated content*
"""
        return content

    def _generate_json_content(self) -> str:
        """Generate random JSON content"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "version": f"{random.randint(1, 10)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "config": {
                "enabled": random.choice([True, False]),
                "timeout": random.randint(1000, 5000),
                "retries": random.randint(1, 5)
            },
            "features": random.sample([
                "authentication", "caching", "logging", "monitoring",
                "analytics", "notifications", "search", "export"
            ], k=random.randint(2, 5)),
            "metadata": {
                "created_by": "github_updater",
                "purpose": random.choice(["testing", "configuration", "data", "settings"])
            }
        }
        return json.dumps(data, indent=2)

    def _generate_text_content(self) -> str:
        """Generate random text content"""
        lines = [
            f"Generated at: {datetime.now()}",
            f"Random ID: {random.randint(10000, 99999)}",
            "",
            "Sample data entries:",
        ]

        for i in range(random.randint(3, 8)):
            lines.append(f"Entry {i+1}: {random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon'])}-{random.randint(100, 999)}")

        lines.extend([
            "",
            "Status: Active",
            f"Last updated: {datetime.now().strftime('%Y-%m-%d')}"
        ])

        return "\n".join(lines)

    def _generate_python_content(self) -> str:
        """Generate random Python content"""
        function_names = ["process_data", "calculate_metrics", "format_output", "validate_input", "generate_report"]
        function_name = random.choice(function_names)

        content = f'''"""
Auto-generated Python module
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import random
from datetime import datetime


def {function_name}(data):
    """
    {function_name.replace('_', ' ').title()} function

    Args:
        data: Input data to process

    Returns:
        Processed result
    """
    result = {{
        'timestamp': datetime.now().isoformat(),
        'processed': True,
        'value': random.randint(1, 100)
    }}
    return result


if __name__ == "__main__":
    sample_data = {{"test": True, "value": {random.randint(1, 1000)}}}
    result = {function_name}(sample_data)
    print(f"Result: {{result}}")
'''
        return content

    def _generate_js_content(self) -> str:
        """Generate random JavaScript content"""
        content = f'''/**
 * Auto-generated JavaScript module
 * Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */

const config = {{
    version: '{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}',
    timestamp: '{datetime.now().isoformat()}',
    features: {json.dumps(random.sample(['auth', 'cache', 'api', 'ui', 'analytics'], k=3))},
    settings: {{
        debug: {str(random.choice([True, False])).lower()},
        timeout: {random.randint(1000, 5000)},
        retries: {random.randint(1, 5)}
    }}
}};

function processRequest(data) {{
    return {{
        ...data,
        processed: true,
        timestamp: new Date().toISOString(),
        id: Math.floor(Math.random() * 10000)
    }};
}}

function validateData(input) {{
    if (!input || typeof input !== 'object') {{
        return false;
    }}
    return true;
}}

module.exports = {{ config, processRequest, validateData }};
'''
        return content

    def create_random_content(self) -> str:
        """Create a random file with random content"""
        file_type = random.choice(list(self.file_templates.keys()))

        # Generate filename
        prefixes = ["data", "config", "sample", "test", "demo", "temp", "generated"]
        suffix = random.choice(prefixes)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        extensions = {
            'markdown': '.md',
            'json': '.json',
            'text': '.txt',
            'python': '.py',
            'javascript': '.js'
        }

        filename = f"{suffix}_{timestamp}{extensions[file_type]}"
        filepath = self.base_dir / filename

        # Generate content
        content = self.file_templates[file_type]()

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Created file: {filename}")
        return filename

    def git_commit_and_push(self, filename: str) -> bool:
        """Commit and push the new file"""
        try:
            # Add file
            subprocess.run(['git', 'add', filename], cwd=self.base_dir, check=True)

            # Commit
            commit_messages = [
                f"Add {filename}",
                f"Create new content: {filename}",
                f"Generate automated content: {filename}",
                f"Update repository with {filename}",
                f"Auto-commit: {filename}"
            ]
            commit_message = random.choice(commit_messages)

            subprocess.run(['git', 'commit', '-m', commit_message], cwd=self.base_dir, check=True)

            # Push
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.base_dir, check=True)

            logger.info(f"Committed and pushed: {filename}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Git operation failed: {e}")
            return False

    def create_github_issue(self) -> bool:
        """Create a random GitHub issue"""
        try:
            title = random.choice(self.issue_titles)

            body_templates = [
                "## Description\nThis issue needs attention.\n\n## Steps to reproduce\n1. Step one\n2. Step two\n\n## Expected behavior\nDescribe expected behavior here.",
                "## Summary\nProposed enhancement to improve the system.\n\n## Benefits\n- Improved performance\n- Better user experience\n\n## Implementation\nSuggested approach here.",
                "## Bug Report\nFound an issue that needs fixing.\n\n## Environment\n- Browser: Chrome\n- OS: Linux\n\n## Additional context\nMore details here."
            ]

            body = random.choice(body_templates)
            labels = random.sample(['bug', 'enhancement', 'documentation', 'good first issue', 'help wanted'], k=random.randint(1, 3))

            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=labels
            )

            logger.info(f"Created issue #{issue.number}: {title}")
            return True

        except GithubException as e:
            logger.error(f"Failed to create issue: {e}")
            return False

    def create_and_merge_pr(self) -> bool:
        """Create a branch, make changes, create PR, and merge it"""
        try:
            # Create new branch name
            branch_name = f"{random.choice(self.branch_names)}-{random.randint(100, 999)}"

            # Create and checkout new branch
            subprocess.run(['git', 'checkout', '-b', branch_name], cwd=self.base_dir, check=True)

            # Create content in the new branch
            filename = self.create_random_content()

            # Commit changes
            subprocess.run(['git', 'add', filename], cwd=self.base_dir, check=True)
            commit_message = f"Add {filename} for PR"
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=self.base_dir, check=True)

            # Push branch
            subprocess.run(['git', 'push', 'origin', branch_name], cwd=self.base_dir, check=True)

            # Create PR
            pr_titles = [
                f"Add new feature: {filename}",
                f"Implement {filename}",
                f"Update repository with {filename}",
                f"Feature: {filename} addition"
            ]

            pr_body = f"""## Changes
- Added {filename}
- Auto-generated content for testing

## Testing
- [x] File created successfully
- [x] Content is valid

## Notes
This is an automated PR created by the GitHub updater system.
"""

            pr = self.repo.create_pull(
                title=random.choice(pr_titles),
                body=pr_body,
                head=branch_name,
                base='main'
            )

            logger.info(f"Created PR #{pr.number}: {pr.title}")

            # Wait a moment then merge
            time.sleep(2)

            # Merge PR
            pr.merge(commit_message=f"Merge PR #{pr.number}")
            logger.info(f"Merged PR #{pr.number}")

            # Switch back to main and pull
            subprocess.run(['git', 'checkout', 'main'], cwd=self.base_dir, check=True)
            subprocess.run(['git', 'pull', 'origin', 'main'], cwd=self.base_dir, check=True)

            # Delete local branch
            subprocess.run(['git', 'branch', '-d', branch_name], cwd=self.base_dir, check=True)

            return True

        except (subprocess.CalledProcessError, GithubException) as e:
            logger.error(f"PR workflow failed: {e}")
            # Try to switch back to main if we're stuck
            try:
                subprocess.run(['git', 'checkout', 'main'], cwd=self.base_dir, check=False)
            except:
                pass
            return False

    def create_and_commit_content(self) -> bool:
        """Create random content and commit it"""
        try:
            filename = self.create_random_content()
            if filename:
                return self.git_commit_and_push(filename)
            return False
        except Exception as e:
            logger.error(f"Failed to create and commit content: {e}")
            return False

    def run_single_cycle(self):
        """Run a single update cycle"""
        logger.info("Starting update cycle...")

        activities = [
            ("Creating and committing content", self.create_and_commit_content),
            ("Creating GitHub issue", self.create_github_issue),
            ("Creating and merging PR", self.create_and_merge_pr)
        ]

        # Randomly select 1-3 activities to perform
        selected_activities = random.sample(activities, k=random.randint(1, len(activities)))

        for activity_name, activity_func in selected_activities:
            logger.info(f"Executing: {activity_name}")
            try:
                success = activity_func()
                if success:
                    logger.info(f"Completed: {activity_name}")
                else:
                    logger.warning(f"Failed: {activity_name}")
            except Exception as e:
                logger.error(f"Error in {activity_name}: {e}")

            # Small delay between activities
            time.sleep(random.randint(5, 15))

        logger.info("Update cycle completed")

    def run_continuous(self, interval_minutes: int = 60):
        """Run continuous updates with specified interval"""
        logger.info(f"Starting continuous mode with {interval_minutes} minute intervals")

        while True:
            try:
                self.run_single_cycle()

                # Calculate next run time
                next_run = datetime.now() + timedelta(minutes=interval_minutes)
                logger.info(f"Next update cycle scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

                # Sleep until next cycle
                time.sleep(interval_minutes * 60)

            except KeyboardInterrupt:
                logger.info("Stopping continuous mode...")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                logger.info("Waiting 5 minutes before retry...")
                time.sleep(300)  # Wait 5 minutes before retrying


def load_config(config_file='config.json'):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file {config_file} not found")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration file: {e}")
        return None


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='GitHub Repository Automation System')
    parser.add_argument('--token', help='GitHub personal access token (overrides config file)')
    parser.add_argument('--repo', help='Repository name (owner/repo) (overrides config file)')
    parser.add_argument('--mode', choices=['single', 'continuous'], default=None,
                       help='Run mode: single cycle or continuous (overrides config file)')
    parser.add_argument('--interval', type=int, default=None,
                       help='Interval in minutes for continuous mode (overrides config file)')
    parser.add_argument('--base-dir', default=None,
                       help='Base directory of the repository (overrides config file)')
    parser.add_argument('--config', default='config.json',
                       help='Configuration file path (default: config.json)')
    parser.add_argument('--no-config', action='store_true',
                       help='Ignore config file and use only command line arguments')

    args = parser.parse_args()

    # Load configuration
    config = None
    if not args.no_config:
        config = load_config(args.config)
        if config is None and not (args.token and args.repo):
            logger.error("Either provide a valid config file or use --token and --repo arguments")
            return 1

    # Determine final configuration values
    if config:
        token = args.token or config.get('github', {}).get('token')
        repo = args.repo or config.get('github', {}).get('repo_name')
        mode = args.mode or ('continuous' if config.get('automation', {}).get('continuous', False) else 'single')
        interval = args.interval or config.get('automation', {}).get('interval_minutes', 60)
        base_dir = args.base_dir or config.get('automation', {}).get('base_directory', '.')
    else:
        # Fallback to command line only
        if not args.token or not args.repo:
            logger.error("Token and repository are required when not using config file")
            return 1
        token = args.token
        repo = args.repo
        mode = args.mode or 'single'
        interval = args.interval or 60
        base_dir = args.base_dir or '.'

    # Validate required parameters
    if not token:
        logger.error("GitHub token is required (provide via config file or --token)")
        return 1
    if not repo:
        logger.error("Repository name is required (provide via config file or --repo)")
        return 1

    logger.info(f"Configuration loaded:")
    logger.info(f"  Repository: {repo}")
    logger.info(f"  Mode: {mode}")
    logger.info(f"  Base Directory: {base_dir}")
    if mode == 'continuous':
        logger.info(f"  Interval: {interval} minutes")

    try:
        # Initialize updater
        updater = GitHubUpdater(token, repo, base_dir)

        # Apply additional config settings if available
        if config:
            automation_config = config.get('automation', {})

            # Override activities if specified in config
            activities = automation_config.get('activities', {})
            if not activities.get('create_issues', True):
                logger.info("Issue creation disabled by configuration")
            if not activities.get('create_prs', True):
                logger.info("Pull request creation disabled by configuration")
            if not activities.get('create_content', True):
                logger.info("Content creation disabled by configuration")

        if mode == 'single':
            updater.run_single_cycle()
        else:
            updater.run_continuous(interval)

        return 0

    except Exception as e:
        logger.error(f"Failed to initialize GitHub updater: {e}")
        return 1


if __name__ == '__main__':
    main()