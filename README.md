# CI Failure Detective 🔍

> Instant answers to "why did my CI fail when it passed locally?"

CI Failure Detective is a CLI tool that helps developers quickly diagnose and fix CI failures by analyzing run logs, detecting environment differences, and providing AI-powered root cause suggestions.

## Features

- **GitHub Actions/GitLab CI Integration** - Fetch failing and passing run logs
- **Diff Analysis** - Compare passing vs failing test runs to identify what changed
- **Environment Delta Detection** - Detect Python version, OS, environment variables, and installed package differences
- **Flaky Test Detection** - Historical pass/fail pattern analysis
- **AI-Powered Suggestions** - Root cause analysis based on error patterns and environment differences
- **Local Environment Profiler** - Capture local runtime config for comparison
- **Fix Suggestion Engine** - Code snippets and config changes to resolve issues

## Installation

```bash
# From source
pip install -e .

# Or install directly
pip install ci-failure-detective
```

## Quick Start

```bash
# Analyze CI failure in current repo
ci-detective analyze

# Analyze specific repository
ci-detective analyze owner/repo

# Profile local environment
ci-detective profile

# Detect flaky tests
ci-detective flaky --token YOUR_GITHUB_TOKEN

# Get fix suggestions
ci-detective suggest "ImportError: No module named 'requests'"

# Initialize in project
ci-detective init
```

## Configuration

Create a `.ci-detective.json` in your project root:

```json
{
  "ci_type": "github-actions",
  "python_version": "3.11",
  "cache_dependencies": true,
  "flaky_test_threshold": 0.3
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub API token for fetching workflow runs |
| `GITLAB_TOKEN` | GitLab API token (for GitLab CI) |
| `CIRCLECI_TOKEN` | CircleCI API token |

## Commands

| Command | Description |
|---------|-------------|
| `analyze` | Analyze CI failure and suggest root cause |
| `profile` | Profile local environment for CI comparison |
| `flaky` | Detect flaky tests in recent runs |
| `suggest` | Get AI-powered fix suggestions |
| `init` | Initialize CI Detective in current project |

## Example Output

```
═══ CI Failure Detective ═══

ℹ Analyzing repository: owner/my-project
ℹ Branch: main

✓ Found recent workflow runs
✓ Diff analysis complete  
✓ Environment delta detected:

Local: Python 3.11.5, Ubuntu 22.04
CI:    Python 3.12.0, Ubuntu 24.04

Differences:
- Python version: 3.11.5 → 3.12.0
- OS: Ubuntu 22.04 → Ubuntu 24.04

═══ Root Cause Analysis ═══

Most Likely Cause: Python version incompatibility

Your code works on Python 3.11.5 but CI uses Python 3.12.0.

Suggested Fixes:

1. Pin Python version in CI:
   python-version: "3.11"

2. Update requirements.txt with compatible versions:
   pip install --upgrade some-package
```

## Supported CI Systems

- ✅ GitHub Actions
- ✅ GitLab CI
- ⏳ CircleCI
- ⏳ Jenkins
- ⏳ Travis CI

## Tech Stack

- Python 3.8+
- Click (CLI framework)
- GitHub API
- Optional: LLM for advanced suggestions

## Development

```bash
# Clone the repo
git clone https://github.com/ci-failure-detective/ci-detective.git
cd ci-detective

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black ci_detective/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

### How to Sponsor

[![Sponsor via GitHub Sponsors](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/ci-failure-detective)

Your sponsorship helps maintain this project and keeps it free for everyone!

---

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) first.

## Support

- 📖 [Documentation](https://ci-failure-detective.dev/docs)
- 🐛 [Issue Tracker](https://github.com/ci-failure-detective/ci-detective/issues)
- 💬 [Discussions](https://github.com/ci-failure-detective/ci-detective/discussions)

## Sponsorship

This project follows the App Factory sponsorship model:

### $5/month - Supporter
- Sponsor badge on your GitHub profile
- Monthly sponsor update

### $25/month - Builder Circle
- Everything in Supporter
- Name listed in project Sponsors section (monthly refresh)
- Access to private sponsor Discord channel

### $100/month - Priority Maintainer
- Everything in Builder Circle
- Priority bug triage for your reports (max 2 issues/month)
- Response target: within 5 business days

### $1,000/month - Operator Advisory
- Everything in Priority Maintainer
- Dedicated async advisory support
- Service boundary: guidance and review only (no custom development included)

### $5,000 one-time - Custom Project Engagement
- Custom contract engagement
- Discovery required before kickoff
- Scope, timeline, and deliverables agreed in writing

Sponsor: https://github.com/sponsors/sdotwinter

