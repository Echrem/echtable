"""
ECHTABLE Storage Manager
Manages persistent storage for system data
"""

import os
import json
from pathlib import Path

class StorageManager:
    """Manages JSON file storage for ECHTABLE"""
    
    def __init__(self):
        self.base_dir = Path.home() / ".echtable"
        self.base_dir.mkdir(exist_ok=True)
        
        self.files = {
            "slots": self.base_dir / "slots.json",
            "variables": self.base_dir / "variables.json",
            "loads": self.base_dir / "loads.json",
            "config": self.base_dir / "config.json"
        }
    
    def ensure_files(self):
        """Create all JSON files if they don't exist"""
        default_data = {
            "slots.json": {},
            "variables.json": {},
            "loads.json": {},
            "config.json": {}
        }
        
        for file_name, default in default_data.items():
            file_path = self.base_dir / file_name
            if not file_path.exists():
                self._write_json(file_path, default)
    
    def _write_json(self, path, data):
        """Write JSON data to file"""
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _read_json(self, path):
        """Read JSON data from file"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def read_slots(self):
        """Read slots data"""
        return self._read_json(self.files["slots"])
    
    def write_slots(self, data):
        """Write slots data"""
        self._write_json(self.files["slots"], data)
    
    def read_variables(self):
        """Read variables data"""
        return self._read_json(self.files["variables"])
    
    def write_variables(self, data):
        """Write variables data"""
        self._write_json(self.files["variables"], data)
    
    def read_loads(self):
        """Read loads data"""
        return self._read_json(self.files["loads"])
    
    def write_loads(self, data):
        """Write loads data"""
        self._write_json(self.files["loads"], data)
