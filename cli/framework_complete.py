"""
ECHTABLE Complete Framework
Extended interactive framework with additional features
"""

import sys
import readline
from core.slots import SlotManager
from core.variables import VariableManager
from core.loads import LoadManager
from core.executor import CommandExecutor

class ECHTableFramework:
    """Extended framework with additional commands"""
    
    def __init__(self):
        self.slots = SlotManager()
        self.vars = VariableManager()
        self.loads = LoadManager()
        self.running = True
        
        # Prompt colors
        self.PROMPT = "\033[94mechtable >\033[0m "
        self.INFO = "\033[92m[+]\033[0m "
        self.ERROR = "\033[91m[!]\033[0m "
        self.WARNING = "\033[93m[*]\033[0m "
        self.BANNER = r"""
\033[96m    ______     __  ______      __    __   
   / ____/____/ /_/_  __/___ _/ /_  / /__ 
  / __/ / ___/ __ \/ / / __ `/ __ \/ / _ \
 / /___/ /__/ / / / / / /_/ / /_/ / /  __/
/_____/\___/_/ /_/_/  \__,_/_.___/_/\___/ 
                                          
\033[93m              by Echrem\033[0m
        """
    
    def start(self):
        """Start the framework"""
        print(self.BANNER)
        print(f"{self.INFO}Type 'help' for commands, 'exit' to quit")
        print(f"{self.WARNING}Active slot: {self.slots.active_slot or 'None'}")
        print(f"{self.WARNING}Active load: {self.loads.active_load or 'None'}")
        print()
        
        while self.running:
            try:
                user_input = input(self.PROMPT).strip()
                if not user_input:
                    continue
                
                self._dispatch_command(user_input)
                
            except KeyboardInterrupt:
                print(f"\n{self.INFO}Exiting...")
                break
            except EOFError:
                print(f"\n{self.INFO}Exiting...")
                break
            except Exception as e:
                print(f"{self.ERROR}Error: {e}")
    
    def _dispatch_command(self, command):
        """Dispatch commands to handlers"""
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        # New commands
        if cmd == "runl":
            self._cmd_runl(args)
        elif cmd == "runs":
            self._cmd_runs(args)
        elif cmd == "edit":
            self._cmd_edit(args)
        elif cmd == "use":
            self._cmd_use(args)
        elif cmd == "run":
            print(f"{self.WARNING}'run' is deprecated. Use 'runs' for slots or 'runl' for loads")
            print(f"{self.INFO}Example: runs 1  or  runl myload")
        elif cmd == "create":
            self._cmd_create(args)
        elif cmd == "set":
            self._cmd_set(args)
        elif cmd == "show":
            self._cmd_show(args)
        elif cmd == "list":
            self._cmd_list(args)
        elif cmd == "delete":
            self._cmd_delete(args)
        elif cmd == "help":
            self._cmd_help()
        elif cmd == "clear":
            import os
            os.system('clear' if os.name == 'posix' else 'cls')
        elif cmd in ["exit", "quit"]:
            print(f"{self.INFO}Goodbye!")
            self.running = False
        else:
            print(f"{self.ERROR}Unknown command: {cmd}")
            print(f"{self.WARNING}Type 'help' for available commands")
    
    def _cmd_runl(self, args):
        """Run load"""
        if not args:
            print(f"{self.ERROR}Usage: runl <load_id|load_name>")
            return
        
        load_name = args[0]
        result = self.loads.execute_load(load_name, self.slots)
        
        if result["success"]:
            print(f"{self.INFO}Load execution completed: {load_name}")
        else:
            print(f"{self.ERROR}Load execution failed: {result.get('error', 'Unknown error')}")
    
    def _cmd_runs(self, args):
        """Run slot"""
        if not args:
            print(f"{self.ERROR}Usage: runs <slot_id|slot_name>")
            return
        
        identifier = args[0]
        extra_params = args[1:] if len(args) > 1 else None
        
        slot = self.slots.get(identifier) or self.slots.find_by_name(identifier)
        if not slot:
            print(f"{self.ERROR}Slot not found: {identifier}")
            return
        
        command = self.slots.prepare_command(slot["id"], extra_params)
        if not command:
            print(f"{self.ERROR}Could not prepare command")
            return
        
        print(f"{self.INFO}Running slot [{slot['id']}] {slot['name']}")
        result = CommandExecutor.execute(command)
        
        if not result["success"]:
            print(f"{self.ERROR}Command failed")
    
    def _cmd_edit(self, args):
        """Edit slot or load"""
        if len(args) < 3:
            print(f"{self.ERROR}Usage: edit slot|load <id|name> --command|--name|--mode <value>")
            return
        
        edit_type = args[0].lower()
        identifier = args[1]
        
        if edit_type == "slot":
            if "--command" in args:
                cmd_index = args.index("--command")
                if cmd_index + 1 < len(args):
                    new_command = " ".join(args[cmd_index+1:])
                    slot = self.slots.get(identifier) or self.slots.find_by_name(identifier)
                    if slot:
                        old_name = slot["name"]
                        self.slots.delete(identifier)
                        new_id = self.slots.create(new_command, old_name)
                        print(f"{self.INFO}Slot edited: {new_id} ({old_name})")
                    else:
                        print(f"{self.ERROR}Slot not found: {identifier}")
                else:
                    print(f"{self.ERROR}Missing command after --command")
            
            elif "--name" in args:
                name_index = args.index("--name")
                if name_index + 1 < len(args):
                    new_name = args[name_index+1]
                    print(f"{self.WARNING}Slot name edit coming soon")
                else:
                    print(f"{self.ERROR}Missing name after --name")
        
        elif edit_type == "load":
            load = self.loads.get(identifier)
            if not load:
                print(f"{self.ERROR}Load not found: {identifier}")
                return
            
            if "--name" in args:
                name_index = args.index("--name")
                if name_index + 1 < len(args):
                    new_name = args[name_index+1]
                    self.loads.edit_load(identifier, name=new_name)
                    print(f"{self.INFO}Load name edited: {load['id']} -> {new_name}")
                else:
                    print(f"{self.ERROR}Missing name after --name")
            
            elif "--slots" in args:
                slots_index = args.index("--slots")
                if slots_index + 1 < len(args):
                    slots_str = args[slots_index+1]
                    slot_ids = [int(x.strip()) for x in slots_str.split(',')]
                    self.loads.edit_load(identifier, slot_ids=slot_ids)
                    print(f"{self.INFO}Load slots edited: {slot_ids}")
                else:
                    print(f"{self.ERROR}Missing slots after --slots")
            
            elif "--mode" in args:
                mode_index = args.index("--mode")
                if mode_index + 1 < len(args):
                    mode = args[mode_index+1]
                    self.loads.edit_load(identifier, mode=mode)
                    print(f"{self.INFO}Load mode edited: {mode}")
                else:
                    print(f"{self.ERROR}Missing mode after --mode")
            else:
                print(f"{self.ERROR}Specify what to edit: --name, --slots, or --mode")
        else:
            print(f"{self.ERROR}Unknown edit type: {edit_type}")
    
    def _cmd_use(self, args):
        """Activate slot or load"""
        if not args:
            print(f"{self.ERROR}Usage: use <slot_id|slot_name|load_id|load_name>")
            return
        
        identifier = args[0]
        
        slot = self.slots.use(identifier)
        if slot:
            print(f"{self.INFO}Using slot [{slot['id']}] {slot['name']}")
            print(f"{self.WARNING}Command: {slot['command']}")
            self.loads.active_load = None
            return
        
        load = self.loads.use(identifier)
        if load:
            print(f"{self.INFO}Using load [{load['id']}] {load['name']}")
            print(f"{self.WARNING}Slots: {', '.join(map(str, load['slot_ids']))}")
            print(f"{self.WARNING}Mode: {load['mode']}")
            self.slots.active_slot = None
            return
        
        print(f"{self.ERROR}Not found: {identifier}")
    
    def _cmd_create(self, args):
        """Create new slot or load"""
        if not args:
            print(f"{self.ERROR}Usage: create slot|load ...")
            return
        
        create_type = args[0].lower()
        
        if create_type == "slot":
            if len(args) < 2:
                print(f"{self.ERROR}Usage: create slot \"command\" --name name")
                return
            
            cmd_parts = args[1:]
            name = None
            
            if "--name" in cmd_parts:
                name_index = cmd_parts.index("--name")
                if name_index + 1 < len(cmd_parts):
                    name = cmd_parts[name_index + 1]
                    command = " ".join(cmd_parts[:name_index])
                else:
                    print(f"{self.ERROR}Missing name after --name")
                    return
            else:
                command = " ".join(cmd_parts)
                name = f"slot_{self.slots.storage.get_next_id('slots')}"
            
            slot_id = self.slots.create(command, name)
            print(f"{self.INFO}Slot created: {slot_id} ({name})")
        
        elif create_type == "load":
            if len(args) < 4 or args[1] != "slots":
                print(f"{self.ERROR}Usage: create load slots \"1,2,3\" --name loadname --mode s|p|serial|parallel")
                return
            
            slots_str = args[2]
            slot_ids = [int(x.strip()) for x in slots_str.split(',')]
            
            name = None
            mode = "serial"
            
            i = 3
            while i < len(args):
                if args[i] == "--name" and i + 1 < len(args):
                    name = args[i + 1]
                    i += 2
                elif args[i] == "--mode" and i + 1 < len(args):
                    mode = args[i + 1]
                    i += 2
                else:
                    i += 1
            
            if not name:
                print(f"{self.ERROR}Missing --name parameter")
                return
            
            load_id = self.loads.create_load(name, slot_ids, mode)
            print(f"{self.INFO}Load created: {load_id} ({name}, mode: {mode})")
        
        else:
            print(f"{self.ERROR}Unknown create type: {create_type}")
    
    def _cmd_set(self, args):
        """Set variable"""
        if len(args) < 2:
            print(f"{self.ERROR}Usage: set @name value")
            return
        
        name = args[0]
        value = " ".join(args[1:])
        
        self.vars.set(name, value)
        clean_name = name.lstrip('@')
        print(f"{self.INFO}Variable set: @{clean_name} = {value}")
    
    def _cmd_show(self, args):
        """Show detailed information"""
        if not args:
            print(f"{self.ERROR}Usage: show slot|var|load <id|name>")
            return
        
        show_type = args[0].lower()
        
        if show_type == "slot":
            if len(args) < 2:
                print(f"{self.ERROR}Usage: show slot <id|name>")
                return
            
            identifier = args[1]
            slot = self.slots.get(identifier) or self.slots.find_by_name(identifier)
            
            if not slot:
                print(f"{self.ERROR}Slot not found: {identifier}")
                return
            
            print(f"\n{self.INFO}Slot Details:")
            print(f"  ID: {slot['id']}")
            print(f"  Name: {slot['name']}")
            print(f"  Command: {slot['command']}")
            print(f"  Created: {slot.get('created_at', 'unknown')}")
            print(f"  Last Used: {slot.get('last_used', 'never')}")
            print(f"  Usage Count: {slot.get('usage_count', 0)}")
            
            substituted = self.vars.substitute(slot['command'])
            if substituted != slot['command']:
                print(f"\n{self.WARNING}With current variables:")
                print(f"  {substituted}")
        
        elif show_type == "var":
            if len(args) < 2:
                print(f"{self.ERROR}Usage: show var <name>")
                return
            
            name = args[1]
            value = self.vars.get(name)
            
            if value is None:
                print(f"{self.ERROR}Variable not found: {name}")
            else:
                clean_name = name.lstrip('@')
                print(f"{self.INFO}@{clean_name} = {value}")
        
        elif show_type == "load":
            if len(args) < 2:
                print(f"{self.ERROR}Usage: show load <id|name>")
                return
            
            name = args[1]
            load = self.loads.get(name)
            
            if not load:
                print(f"{self.ERROR}Load not found: {name}")
                return
            
            print(f"\n{self.INFO}Load Details:")
            print(f"  ID: {load['id']}")
            print(f"  Name: {load['name']}")
            print(f"  Slots: {', '.join(map(str, load['slot_ids']))}")
            print(f"  Mode: {load['mode']}")
            print(f"  Created: {load.get('created_at', 'unknown')}")
        
        else:
            print(f"{self.ERROR}Unknown show type: {show_type}")
    
    def _cmd_list(self, args):
        """List items"""
        if not args:
            print(f"{self.ERROR}Usage: list slots|vars|loads")
            return
        
        list_type = args[0].lower()
        
        if list_type == "slots":
            slots_list = self.slots.list_all()
            if not slots_list:
                print(f"{self.WARNING}No slots found")
            else:
                print(f"\n{self.INFO}Slots:")
                print("ID  Name            Command")
                print("-" * 60)
                for slot in slots_list:
                    cmd_preview = slot["command"][:40] + "..." if len(slot["command"]) > 40 else slot["command"]
                    print(f"{slot['id']:<3} {slot['name']:<15} {cmd_preview}")
        
        elif list_type == "vars":
            vars_list = self.vars.list_all()
            if not vars_list:
                print(f"{self.WARNING}No variables found")
            else:
                print(f"\n{self.INFO}Variables:")
                print("Variable       Value")
                print("-" * 40)
                for var in vars_list:
                    print(f"{var['name']:<15} {var['value']}")
        
        elif list_type == "loads":
            loads_list = self.loads.list_all()
            if not loads_list:
                print(f"{self.WARNING}No loads found")
            else:
                print(f"\n{self.INFO}Loads:")
                print("ID  Name            Slots           Mode")
                print("-" * 50)
                for load in loads_list:
                    slots_str = ', '.join(map(str, load['slots']))
                    print(f"{load['id']:<3} {load['name']:<15} {slots_str:<15} {load['mode']}")
        
        else:
            print(f"{self.ERROR}Unknown list type: {list_type}")
    
    def _cmd_delete(self, args):
        """Delete items"""
        if len(args) < 2:
            print(f"{self.ERROR}Usage: delete slot|var|load <id|name>")
            return
        
        delete_type = args[0].lower()
        
        if delete_type == "slot":
            identifier = args[1]
            if self.slots.delete(identifier):
                print(f"{self.INFO}Slot deleted: {identifier}")
            else:
                print(f"{self.ERROR}Slot not found: {identifier}")
        
        elif delete_type == "var":
            name = args[1]
            if self.vars.delete(name):
                clean_name = name.lstrip('@')
                print(f"{self.INFO}Variable deleted: @{clean_name}")
            else:
                print(f"{self.ERROR}Variable not found: {name}")
        
        elif delete_type == "load":
            name = args[1]
            if self.loads.delete(name):
                print(f"{self.INFO}Load deleted: {name}")
            else:
                print(f"{self.ERROR}Load not found: {name}")
        
        else:
            print(f"{self.ERROR}Unknown delete type: {delete_type}")
    
    def _cmd_help(self):
        """Help menu"""
        help_text = f"""
{self.INFO}ECHTABLE Framework Commands:

{self.WARNING}Basic:
  help                    Show this help
  exit, quit             Exit framework
  clear                  Clear screen

{self.WARNING}Slot Operations:
  use <id|name>          Activate slot
  runs <id|name>         Run slot
  create slot "cmd" --name name  Create new slot
  show slot <id|name>    Show slot details
  list slots             List all slots
  delete slot <id|name>  Delete slot
  edit slot <id|name> --command "new cmd"  Edit slot

{self.WARNING}Variable Operations:
  set @name value        Set variable
  show var <name>        Show variable
  list vars              List all variables
  delete var <name>      Delete variable

{self.WARNING}Load Operations:
  use load <id|name>     Activate load
  runl <id|name>         Run load
  create load slots "1,2,3" --name name --mode s|p
  show load <id|name>    Show load details
  list loads             List all loads
  delete load <id|name>  Delete load
  edit load <id|name> --name newname --slots "1,2" --mode s|p

{self.WARNING}Mode Shortcuts:
  s = serial, p = parallel

{self.WARNING}Examples:
  set @target 10.10.10.5
  create slot nmap -sV @target --name scan
  runs 1
  create load slots 1,2,3 --name fullscan --mode p
  runl fullscan
        """
        print(help_text)

def start_framework():
    """Start the framework"""
    framework = ECHTableFramework()
    framework.start()

if __name__ == "__main__":
    start_framework()
