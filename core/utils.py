"""
ECHTABLE Utilities Module
Utility functions for file path management
"""

import os

BASE_DIR = os.path.expanduser("~/.echtable")

def data_path(filename):
    """Get absolute path for data files in ECHTABLE directory"""
    os.makedirs(BASE_DIR, exist_ok=True)
    return os.path.join(BASE_DIR, filename)
