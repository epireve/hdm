#!/usr/bin/env python3
"""
Test runner script for HDM project.
"""

import sys
import subprocess
from pathlib import Path


def run_tests(test_type="all", verbose=True):
    """Run tests with specified configuration."""
    
    cmd = [sys.executable, "-m", "pytest"]
    
    if test_type == "unit":
        cmd.extend(["tests/unit/"])
    elif test_type == "integration":
        cmd.extend(["tests/integration/"])
    elif test_type == "all":
        cmd.extend(["tests/"])
    else:
        print(f"Unknown test type: {test_type}")
        return 1
    
    if verbose:
        cmd.extend(["-v"])
    
    # Add coverage if available
    try:
        import pytest_cov
        cmd.extend(["--cov=scripts.refactored", "--cov-report=term-missing"])
    except ImportError:
        pass
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="HDM Test Runner")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "all"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Run tests quietly"
    )
    
    args = parser.parse_args()
    
    # Ensure we're in the project root
    if not Path("scripts/refactored").exists():
        print("Error: Must run from project root directory")
        return 1
    
    return run_tests(args.type, not args.quiet)


if __name__ == "__main__":
    sys.exit(main())