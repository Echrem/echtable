"""
ECHTABLE Slot Manager
Manages command slots
"""

import os
import json
from datetime import datetime
from core.utils import data_path
from core.variables import VariableManager

class SlotManager:
    """Manages command slots"""
    
    def __init__(self):
        self.path = data_path("slots.json")
        self.variables = VariableManager()
        self._ensure_file()
        self.active_slot = None
    
    def _ensure_file(self):
        """Create slots file if missing"""
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({}, f)
    
    def create(self, command, name=None):
        """Create a new slot"""
        with open(self.path, "r") as f:
            slots = json.load(f)
        
        new_id = 1
        while str(new_id) in slots and not slots[str(new_id)].get("deleted", False):
            new_id += 1
        
        slots[str(new_id)] = {
            "id": new_id,
            "name": name or f"slot_{new_id}",
            "command": command,
            "created_at": datetime.now().isoformat(),
            "last_used": None,
            "usage_count": 0,
            "deleted": False
        }
        
        with open(self.path, "w") as f:
            json.dump(slots, f, indent=2)
        
        return new_id
    
    def get(self, slot_id):
        """Get slot information"""
        with open(self.path, "r") as f:
            slots = json.load(f)
        return slots.get(str(slot_id))
    
    def find_by_name(self, name):
        """Find slot by name"""
        with open(self.path, "r") as f:
            slots = json.load(f)
        
        for slot_id, data in slots.items():
            if data.get("name") == name and not data.get("deleted", False):
                return data
        
        return None
    
    def use(self, identifier):
        """Activate a slot"""
        slot = self.get(identifier) or self.find_by_name(identifier)
        if slot:
            self.active_slot = slot["id"]
            return slot
        return None
    
    def prepare_command(self, slot_id=None, extra_params=None):
        """Prepare slot command for execution"""
        if not slot_id and self.active_slot:
            slot_id = self.active_slot
        elif not slot_id:
            return None
        
        slot = self.get(slot_id)
        if not slot:
            return None
        
        command = slot["command"]
        command = self.variables.substitute(command)
        
        if extra_params and "@target" in command:
            command = command.replace("@target", extra_params[0])
        
        self._increment_usage(slot_id)
        return command
    
    def _increment_usage(self, slot_id):
        """Increment usage counter"""
        with open(self.path, "r") as f:
            slots = json.load(f)
        
        if str(slot_id) in slots:
            slots[str(slot_id)]["usage_count"] = slots[str(slot_id)].get("usage_count", 0) + 1
            slots[str(slot_id)]["last_used"] = datetime.now().isoformat()
            
            with open(self.path, "w") as f:
                json.dump(slots, f, indent=2)
    
    def list_all(self):
        """List all slots"""
        with open(self.path, "r") as f:
            slots = json.load(f)
        
        result = []
        for slot_id, data in slots.items():
            if not data.get("deleted", False):
                result.append({
                    "id": data["id"],
                    "name": data["name"],
                    "command": data["command"],
                    "usage": data.get("usage_count", 0)
                })
        return result
    
    def list_sorted(self):
        """Get sorted slot list"""
        slots = self.list_all()
        return sorted(slots, key=lambda x: x["id"])
    
    def delete(self, identifier):
        """Delete a slot"""
        slot = self.get(identifier) or self.find_by_name(identifier)
        if not slot:
            return False
        
        slot_id = slot["id"]
        
        with open(self.path, "r") as f:
            slots = json.load(f)
        
        slots[str(slot_id)] = {
            "id": slot_id,
            "name": f"_deleted_{slot_id}",
            "command": "",
            "created_at": slot.get("created_at"),
            "last_used": None,
            "usage_count": 0,
            "deleted": True
        }
        
        with open(self.path, "w") as f:
            json.dump(slots, f, indent=2)
        
        if self.active_slot == slot_id:
            self.active_slot = None
        
        return True
    
    def sort_ids(self):
        """Renumber slot IDs sequentially"""
        with open(self.path, "r") as f:
            slots = json.load(f)
        
        active_slots = []
        for slot_id, data in slots.items():
            if not data.get("deleted", False):
                active_slots.append((int(slot_id), data))
        
        active_slots.sort(key=lambda x: x[0])
        
        new_slots = {}
        new_id = 1
        for old_id, data in active_slots:
            data["id"] = new_id
            new_slots[str(new_id)] = data
            new_id += 1
        
        with open(self.path, "w") as f:
            json.dump(new_slots, f, indent=2)
        
        return new_id - 1
