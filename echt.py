#!/usr/bin/env python3
"""
ECHTABLE Fast CLI - Quick command execution
Command-line interface for fast operations
"""

import sys
import os

# Add current directory to path for local development
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from cli.non_interactive import main

if __name__ == "__main__":
    sys.exit(main())
