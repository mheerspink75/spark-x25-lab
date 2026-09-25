"""
Pytest configuration for the GitHub Issue Triage project.

Adds the project root to sys.path so that the `src` package can be
imported by the test modules.
"""

import sys
from pathlib import Path

# Add the project root directory to the Python path.
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
