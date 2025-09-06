#!/usr/bin/env python3
"""
Script to run all linting tools on the Cinetica project.
Usage: python lint.py [--fix]
"""

import subprocess
import sys
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return True if successful."""
    print(f"\n[*] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[+] {description} passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Run linting tools on Cinetica project")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues where possible")
    args = parser.parse_args()

    project_root = Path(__file__).parent
    
    print("Running linting tools on Cinetica project...")
    
    success = True
    
    # Run Black (formatter)
    if args.fix:
        success &= run_command("black cinetica/ tests/ usage/", "Black formatting (auto-fix)")
    else:
        success &= run_command("black --check cinetica/ tests/ usage/", "Black formatting check")
    
    # Run Flake8 (linter)
    success &= run_command("flake8 cinetica/ tests/ usage/", "Flake8 linting")
    
    # Run MyPy (type checker)
    success &= run_command("mypy cinetica/", "MyPy type checking")
    
    if success:
        print("\nAll linting checks passed!")
        return 0
    else:
        print("\nSome linting checks failed. Run with --fix to auto-fix formatting issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
