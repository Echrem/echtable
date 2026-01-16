"""
ECHTABLE Load Manager
Manages load configurations
"""

import os
import json
from datetime import datetime
from core.utils import data_path
from core.executor import CommandExecutor

class LoadManager:
    """Manages load configurations"""
    
    def __init__(self):
        self.path = data_path("loads.json")
        self._ensure_file()
        self.active_load = None
    
    def _ensure_file(self):
        """Create loads file if missing"""
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({}, f)
    
    def create_load(self, name, slot_ids, mode="serial"):
        """Create a new load"""
        with open(self.path, "r") as f:
            loads = json.load(f)
        
        new_id = 1
        while str(new_id) in loads and not loads[str(new_id)].get("deleted", False):
            new_id += 1
        
        mode_map = {"s": "serial", "p": "parallel"}
        final_mode = mode_map.get(mode.lower(), mode)
        
        loads[str(new_id)] = {
            "id": new_id,
            "name": name,
            "slot_ids": slot_ids,
            "mode": final_mode,
            "created_at": datetime.now().isoformat(),
            "deleted": False
        }
        
        loads[name] = loads[str(new_id)]
        
        with open(self.path, "w") as f:
            json.dump(loads, f, indent=2)
        
        return new_id
    
    def get(self, identifier):
        """Get load information"""
        with open(self.path, "r") as f:
            loads = json.load(f)
        
        if str(identifier) in loads:
            return loads[str(identifier)]
        
        for key, data in loads.items():
            if isinstance(data, dict) and data.get("name") == identifier:
                return data
        
        return None
    
    def use(self, identifier):
        """Activate a load"""
        load = self.get(identifier)
        if load:
            self.active_load = load["id"]
            return load
        return None
    
    def execute_load(self, identifier, slot_manager):
        """Execute a load"""
        load = self.get(identifier)
        if not load:
            return {"success": False, "error": f"Load not found: {identifier}"}
        
        slot_ids = load["slot_ids"]
        mode = load["mode"]
        
        print(f"[*] Executing load [{load['id']}] {load['name']}")
        print(f"[*] Slots: {slot_ids}")
        print(f"[*] Mode: {mode}")
        
        commands = []
        for slot_id in slot_ids:
            cmd = slot_manager.prepare_command(slot_id)
            if cmd:
                commands.append(cmd)
        
        executor = CommandExecutor()
        if mode == "serial":
            results = executor.execute_serial(commands)
        elif mode == "parallel":
            results = executor.execute_parallel(commands)
        else:
            return {"success": False, "error": f"Unknown mode: {mode}"}
        
        return {"success": True, "results": results}
    
    def list_all(self):
        """List all loads"""
        with open(self.path, "r") as f:
            loads = json.load(f)
        
        result = []
        for key, data in loads.items():
            if key.isdigit() and not data.get("deleted", False):
                result.append({
                    "id": data["id"],
                    "name": data["name"],
                    "slots": data["slot_ids"],
                    "mode": data["mode"]
                })
        return result
    
    def list_sorted(self):
        """Get sorted load list"""
        loads = self.list_all()
        return sorted(loads, key=lambda x: x["id"])
    
    def edit_load(self, identifier, name=None, slot_ids=None, mode=None):
        """Edit a load"""
        load = self.get(identifier)
        if not load:
            return False
        
        load_id = load["id"]
        
        with open(self.path, "r") as f:
            loads = json.load(f)
        
        old_name = loads[str(load_id)]["name"]
        if old_name in loads:
            del loads[old_name]
        
        if name:
            loads[str(load_id)]["name"] = name
        if slot_ids:
            loads[str(load_id)]["slot_ids"] = slot_ids
        if mode:
            mode_map = {"s": "serial", "p": "parallel"}
            final_mode = mode_map.get(mode.lower(), mode)
            loads[str(load_id)]["mode"] = final_mode
        
        new_name = name or old_name
        loads[new_name] = loads[str(load_id)]
        
        with open(self.path, "w") as f:
            json.dump(loads, f, indent=2)
        
        return True
    
    def delete(self, identifier):
        """Delete a load"""
        load = self.get(identifier)
        if not load:
            return False
        
        with open(self.path, "r") as f:
            loads = json.load(f)
        
        load_id = str(load["id"])
        load_name = load["name"]
        
        loads[load_id] = {
            "id": load["id"],
            "name": f"_deleted_{load_id}",
            "slot_ids": [],
            "mode": "serial",
            "created_at": load.get("created_at"),
            "deleted": True
        }
        
        if load_name in loads:
            del loads[load_name]
        
        if self.active_load == load["id"]:
            self.active_load = None
        
        with open(self.path, "w") as f:
            json.dump(loads, f, indent=2)
        
        return True
    
    def sort_ids(self):
        """Renumber load IDs sequentially"""
        with open(self.path, "r") as f:
            loads = json.load(f)
        
        active_loads = []
        for load_id, data in loads.items():
            if load_id.isdigit() and not data.get("deleted", False):
                active_loads.append((int(load_id), data))
        
        active_loads.sort(key=lambda x: x[0])
        
        new_loads = {}
        new_id = 1
        for old_id, data in active_loads:
            data["id"] = new_id
            new_loads[str(new_id)] = data
            new_loads[data["name"]] = data
            new_id += 1
        
        with open(self.path, "w") as f:
            json.dump(new_loads, f, indent=2)
        
        return new_id - 1
