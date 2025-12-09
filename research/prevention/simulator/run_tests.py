"""
Test runner script.

This script runs all tests in the simulator package.
Can be executed from any directory.
"""

import sys
from pathlib import Path

# Add research/prevention directory to path
current_file = Path(__file__).resolve()
parent_dir = current_file.parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import pytest

if __name__ == "__main__":
    # Run all tests in the current directory
    test_dir = current_file.parent
    pytest.main([str(test_dir), "-v"])

