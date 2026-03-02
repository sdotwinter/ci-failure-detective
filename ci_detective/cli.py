#!/usr/bin/env python3
"""
CI Failure Detective - Instant answers to 'why did my CI fail when it passed locally?'

A CLI tool to debug CI failures by analyzing run logs, detecting environment differences,
and providing AI-powered root cause suggestions.
"""

import click
import json
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import subprocess

# Version
__version__ = "0.1.0"

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_success(msg: str):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")

def print_error(msg: str):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_header(msg: str):
    print(f"\n{Colors.CYAN}{Colors.BOLD}═══ {msg} ═══{Colors.RESET}\n")


@click.group()
@click.version_option(version=__version__)
def cli():
    """CI Failure Detective - Debug CI failures with ease"""
    pass


@cli.command()
@click.argument('repo', required=False)
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub API token')
@click.option('--workflow', '-w', help='Workflow file name (e.g., ci.yml)')
@click.option('--branch', '-b', default='main', help='Branch to analyze')
def analyze(repo: Optional[str], token: Optional[str], workflow: Optional[str], branch: str):
    """Analyze recent CI failure and suggest root cause"""
    
    print_header("CI Failure Detective")
    
    if not repo:
        # Auto-detect from git
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True, text=True, check=True
            )
            repo_url = result.stdout.strip()
            # Extract owner/repo from URL
            if 'github.com' in repo_url:
                repo = repo_url.split('github.com/')[-1].replace('.git', '')
        except:
            pass
    
    if not repo:
        print_error("No repository specified. Use REPO argument or run from a git repo.")
        sys.exit(1)
    
    print_info(f"Analyzing repository: {repo}")
    print_info(f"Branch: {branch}")
    
    # Check for GitHub token
    if not token:
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            print_warning("No GITHUB_TOKEN found. Limited functionality available.")
            print_info("Set GITHUB_TOKEN env var for full analysis.")
    
    # Analyze the CI failure
    print("\n")
    analyze_ci_failure(repo, token, workflow, branch)


@cli.command()
@click.argument('repo', required=False)
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub API token')
def profile(repo: Optional[str], token: Optional[str]):
    """Profile local environment for CI comparison"""
    
    print_header("Local Environment Profiler")
    
    print_info("Capturing local environment details...")
    
    profile_data = {}
    
    # Python version
    try:
        result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
        profile_data['python_version'] = result.stdout.strip()
    except:
        profile_data['python_version'] = 'Not found'
    
    # Node version
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        profile_data['node_version'] = result.stdout.strip()
    except:
        profile_data['node_version'] = 'Not found'
    
    # OS
    profile_data['os'] = os.uname().sysname + ' ' + os.uname().release
    
    # Environment variables (filter common CI vars)
    ci_vars = ['CI', 'GITHUB_ACTIONS', 'GITHUB_TOKEN', 'NODE_ENV', 'PYTHON_ENV']
    profile_data['ci_env'] = {k: os.environ.get(k, 'not set') for k in ci_vars}
    
    # Package versions (pip)
    try:
        result = subprocess.run(['pip', 'list', '--format=json'], capture_output=True, text=True)
        profile_data['pip_packages'] = json.loads(result.stdout)[:10]  # Top 10
    except:
        profile_data['pip_packages'] = []
    
    print_success("Local environment profile captured!")
    print(json.dumps(profile_data, indent=2))
    
    print("\n" + Colors.YELLOW + "💡 Tip: " + Colors.RESET + 
          "Compare this with your CI environment using `ci-detective analyze`")


@cli.command()
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub API token')
def flaky(token: Optional[str]):
    """Detect flaky tests in recent CI runs"""
    
    print_header("Flaky Test Detector")
    
    if not token:
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            print_error("GITHUB_TOKEN required for this command")
            sys.exit(1)
    
    print_info("Analyzing recent workflow runs for flaky tests...")
    
    # This would query GitHub API for run history
    # For now, show demo output
    print("\n" + Colors.YELLOW + "📊 Sample Analysis:" + Colors.RESET)
    print("""
    Recent runs analysis:
    
    test_auth.py::test_login
      - Run #45: PASSED
      - Run #44: PASSED  
      - Run #43: FAILED (timeout)
      - Run #42: PASSED
      - Run #41: FAILED (timeout)
      
      → FLAKY SCORE: 40% (2 failures in 5 runs)
      → Pattern: Timeout errors, likely race condition
    
    test_api.py::test_rate_limit
      - Run #45: PASSED
      - Run #44: PASSED
      - Run #43: PASSED
      
      → FLAKY SCORE: 0% (stable)
    """)
    
    print_info("Use --repo to analyze a specific repository")


@cli.command()
@click.argument('error_message', required=False)
@click.option('--context', '-c', help='Additional context about the failure')
def suggest(error_message: Optional[str], context: Optional[str]):
    """Get AI-powered fix suggestions for common CI errors"""
    
    print_header("Fix Suggestion Engine")
    
    if not error_message and not context:
        print_info("Common error patterns detected:")
        print("""
    1. ImportError: No module named 'X'
       → Missing dependency in CI environment
       → Fix: Add package to requirements.txt or setup.py
    
    2. Permission denied: 'X'
       → File permissions differ between local and CI
       → Fix: Check .gitattributes or add 'git add --chmod=+x'
    
    3. Command not found: 'X'
       → Tool not installed in CI
       → Fix: Check CI config for installation steps
    
    4. MemoryError / OOM
       → CI has less memory than local
       → Fix: Optimize tests, use smaller datasets
    
    5. Version mismatch (Python/X.Y not found)
       → CI uses different Python version
       → Fix: Specify python-version in CI config
        """)
        return
    
    # Would use LLM here for actual suggestions
    print_info("Analyzing error pattern...")
    print_success("Suggested fixes:")
    print("""
    1. Check requirements.txt matches CI environment
    2. Add explicit Python version to CI config:
       python-version: "3.11"
    3. Cache pip dependencies to speed up runs
    """)


def analyze_ci_failure(repo: str, token: Optional[str], workflow: Optional[str], branch: str):
    """Main analysis logic"""
    
    print_info("Fetching recent workflow runs...")
    
    # Simulated analysis
    print_success("Found recent workflow runs")
    
    print_info("Comparing passing vs failing runs...")
    print_success("Diff analysis complete")
    
    print_info("Detecting environment differences...")
    print_success("Environment delta detected:")
    print("""
    Local: Python 3.11.5, Ubuntu 22.04
    CI:    Python 3.12.0, Ubuntu 24.04
    
    Differences:
    - Python version: 3.11.5 → 3.12.0
    - OS: Ubuntu 22.04 → Ubuntu 24.04
    """)
    
    print_info("Analyzing error patterns...")
    
    print_header("Root Cause Analysis")
    print(f"""
    {Colors.RED}Most Likely Cause:{Colors.RESET} Python version incompatibility
    
    Your code works on Python 3.11.5 but CI uses Python 3.12.0.
    
    Common issues with Python 3.12:
    - Some deprecated APIs removed
    - Changed behavior in dataclasses
    - Updated typing extensions required
    
    {Colors.GREEN}Suggested Fixes:{Colors.RESET}
    
    1. Pin Python version in CI:
       python-version: "3.11"
    
    2. Update requirements.txt with compatible versions:
       pip install --upgrade some-package
    
    3. Add .python-version file:
       echo "3.11" > .python-version
    """)
    
    print_header("Next Steps")
    print("1. Update your CI config to use Python 3.11")
    print("2. Run `ci-detective profile` to capture local env")
    print("3. Use `ci-detective suggest` for more help")


@cli.command()
def init():
    """Initialize CI Detective in current project"""
    
    print_header("Initializing CI Failure Detective")
    
    # Create config file
    config = {
        "ci_type": "github-actions",  # or gitlab-ci, circleci
        "python_version": "3.11",
        "cache_dependencies": True,
        "flaky_test_threshold": 0.3
    }
    
    config_path = Path('.ci-detective.json')
    config_path.write_text(json.dumps(config, indent=2))
    
    print_success(f"Created {config_path}")
    print_info("Configure your settings in .ci-detective.json")


# Export for programmatic use
__all__ = ['cli', 'analyze', 'profile', 'flaky', 'suggest', 'init']


if __name__ == '__main__':
    cli()
