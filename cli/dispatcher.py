"""
ECHTABLE Command Dispatcher
Routes commands to appropriate handlers
"""

from core.slots import SlotManager
from core.variables import VariableManager
from core.loads import LoadManager
from core.executor import CommandExecutor

class Dispatcher:
    """Command dispatcher class"""
    
    def __init__(self):
        self.slots = SlotManager()
        self.vars = VariableManager()
        self.loads = LoadManager()
        self.executor = CommandExecutor()
    
    def handle_command(self, cmd, *args):
        """Dispatch command to handler"""
        if cmd == "slot":
            return self.handle_slot(*args)
        elif cmd == "var":
            return self.handle_variable(*args)
        elif cmd == "load":
            return self.handle_load(*args)
        elif cmd == "run":
            return self.handle_run(*args)
        else:
            return f"Unknown command: {cmd}"
    
    def handle_slot(self, subcmd, *args):
        """Handle slot commands"""
        if subcmd == "create":
            return self.slots.create(*args)
        elif subcmd == "list":
            return self.slots.list_all()
        elif subcmd == "show":
            return self.slots.get(*args)
    
    def handle_variable(self, subcmd, *args):
        """Handle variable commands"""
        if subcmd == "set":
            return self.vars.set(*args)
        elif subcmd == "get":
            return self.vars.get(*args)
    
    def handle_load(self, subcmd, *args):
        """Handle load commands"""
        if subcmd == "create":
            return self.loads.create_load(*args)
        elif subcmd == "execute":
            return self.loads.execute_load(*args)
