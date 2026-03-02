"""
CI Failure Detective - Debug CI failures with ease

A CLI tool to debug CI failures by analyzing run logs, detecting environment differences,
and providing AI-powered root cause suggestions.
"""

__version__ = "0.1.0"
__author__ = "CI Failure Detective Team"

from ci_detective.cli import cli, analyze, profile, flaky, suggest, init

__all__ = ['cli', 'analyze', 'profile', 'flaky', 'suggest', 'init', '__version__']
