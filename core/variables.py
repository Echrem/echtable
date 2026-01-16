"""
ECHTABLE Variable Manager
Manages dynamic variables with @ prefix
"""

import os
import re
import json
from core.utils import data_path
from datetime import datetime

class VariableManager:
    """Manages dynamic variables for command substitution"""
    
    def __init__(self):
        self.path = data_path("variables.json")
        self.prefix = "@"
        self._ensure_file()
    
    def _ensure_file(self):
        """Create variables file if missing"""
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({}, f)
    
    def set(self, name, value):
        """Set a variable value"""
        clean_name = name.lstrip(self.prefix)
        
        with open(self.path, "r") as f:
            vars = json.load(f)
        
        vars[clean_name] = {
            "value": value,
            "created_at": datetime.now().isoformat()
        }
        
        with open(self.path, "w") as f:
            json.dump(vars, f, indent=2)
        
        return True
    
    def get(self, name, default=None):
        """Get variable value"""
        clean_name = name.lstrip(self.prefix)
        
        with open(self.path, "r") as f:
            vars = json.load(f)
        
        var_data = vars.get(clean_name)
        return var_data["value"] if var_data else default
    
    def get_all(self):
        """Get all variables"""
        with open(self.path, "r") as f:
            vars = json.load(f)
        
        return {name: data["value"] for name, data in vars.items()}
    
    def substitute(self, text):
        """Substitute @variables in text with values"""
        variables = self.get_all()
        
        def replace_match(match):
            var_name = match.group(1)
            return str(variables.get(var_name, f"@{var_name}"))
        
        pattern = r'@(\w+)'
        return re.sub(pattern, replace_match, text)
    
    def list_all(self):
        """List all variables"""
        with open(self.path, "r") as f:
            vars = json.load(f)
        
        result = []
        for name, data in vars.items():
            result.append({
                "name": f"@{name}",
                "value": data["value"],
                "created": data.get("created_at", "unknown")
            })
        return result
    
    def delete(self, name):
        """Delete a variable"""
        clean_name = name.lstrip(self.prefix)
        
        with open(self.path, "r") as f:
            vars = json.load(f)
        
        if clean_name in vars:
            del vars[clean_name]
            
            with open(self.path, "w") as f:
                json.dump(vars, f, indent=2)
            return True
        
        return False
