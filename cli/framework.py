"""
ECHTABLE Interactive Framework
Interactive command interface for ECHTABLE system
"""

import sys
import readline
import subprocess
import os
from core.slots import SlotManager
from core.variables import VariableManager
from core.loads import LoadManager
from core.executor import CommandExecutor

class ECHTableFramework:
    """Interactive framework class"""
    
    def __init__(self):
        self.slots = SlotManager()
        self.vars = VariableManager()
        self.loads = LoadManager()
        self.running = True
        self.current_dir = os.getcwd()
        
        # Simple prompts without colors
        self.PROMPT = "echtable > "
        self.INFO = "[+] "
        self.ERROR = "[!] "
        self.WARNING = "[*] "
        self.BANNER = """
    ______     __  ______      __    __   
   / ____/____/ /_/_  __/___ _/ /_  / /__ 
  / __/ / ___/ __ \\/ / / __ `/ __ \\/ / _ \\
 / /___/ /__/ / / / / / /_/ / /_/ / /  __/
/_____/\\___/_/ /_/_/  \\__,_/_.___/_/\\___/ 
                                          
              by Echrem
        """
    
    def start(self):
        """Start the interactive framework"""
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
        """Dispatch commands to appropriate handlers"""
        if command.startswith('+'):
            shell_cmd = command[1:].strip()
            self._execute_shell(shell_cmd)
            return
        
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == "show":
            self._cmd_show(args)
        elif cmd == "var":
            self._cmd_var(args)
        elif cmd in ["sorts", "sortl"]:
            self._cmd_sort(args, cmd)
        elif cmd == "sort":
            self._cmd_sort_id(args)
        elif cmd == "shell":
            self._cmd_shell(args)
        elif cmd == "runl":
            self._cmd_runl(args)
        elif cmd == "runs":
            self._cmd_runs(args)
        elif cmd == "edit":
            self._cmd_edit(args)
        elif cmd == "use":
            self._cmd_use(args)
        elif cmd == "create":
            self._cmd_create(args)
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
    
    def _execute_shell(self, command):
        """Execute shell commands starting with +"""
        print(f"{self.INFO}Executing: {command}")
        print("-" * 60)
        
        try:
            if command.startswith("cd "):
                new_dir = command[3:].strip()
                try:
                    os.chdir(new_dir)
                    self.current_dir = os.getcwd()
                    print(f"{self.INFO}Changed directory to: {self.current_dir}")
                except Exception as e:
                    print(f"{self.ERROR}cd failed: {e}")
                return
            
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.current_dir
            )
            
            stdout, stderr = process.communicate()
            
            if stdout:
                print(stdout)
            if stderr:
                print(f"{self.ERROR}{stderr}")
            
            if process.returncode == 0:
                print(f"{self.INFO}Command executed successfully")
            else:
                print(f"{self.ERROR}Command failed with code: {process.returncode}")
                
        except Exception as e:
            print(f"{self.ERROR}Shell execution error: {e}")
    
    def _cmd_show(self, args):
        """Show commands"""
        if not args:
            print(f"{self.ERROR}Usage: show slots|vars|loads|slot|var|load")
            return
        
        show_type = args[0].lower()
        
        if show_type == "slots":
            slots_list = self.slots.list_sorted()
            if not slots_list:
                print(f"{self.WARNING}No slots found")
            else:
                print(f"\n{self.INFO}Slots:")
                print("ID  Name            Command")
                print("-" * 60)
                for slot in slots_list:
                    cmd_preview = slot["command"][:40] + "..." if len(slot["command"]) > 40 else slot["command"]
                    print(f"{slot['id']:<3} {slot['name']:<15} {cmd_preview}")
        
        elif show_type == "vars":
            vars_list = self.vars.list_all()
            if not vars_list:
                print(f"{self.WARNING}No variables found")
            else:
                print(f"\n{self.INFO}Variables:")
                print("Variable       Value")
                print("-" * 40)
                for var in vars_list:
                    print(f"{var['name']:<15} {var['value']}")
        
        elif show_type == "loads":
            loads_list = self.loads.list_sorted()
            if not loads_list:
                print(f"{self.WARNING}No loads found")
            else:
                print(f"\n{self.INFO}Loads:")
                print("ID  Name            Slots           Mode")
                print("-" * 50)
                for load in loads_list:
                    slots_str = ', '.join(map(str, load['slots']))
                    print(f"{load['id']:<3} {load['name']:<15} {slots_str:<15} {load['mode']}")
        
        elif show_type == "slot":
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
    
    def _cmd_var(self, args):
        """Variable operations"""
        if not args:
            print(f"{self.ERROR}Usage: var @name value  or  var delete @name")
            return
        
        if args[0] == "delete":
            if len(args) < 2:
                print(f"{self.ERROR}Usage: var delete @name")
                return
            
            name = args[1]
            if self.vars.delete(name):
                clean_name = name.lstrip('@')
                print(f"{self.INFO}Variable deleted: @{clean_name}")
            else:
                print(f"{self.ERROR}Variable not found: {name}")
        
        else:
            if len(args) < 2:
                print(f"{self.ERROR}Usage: var @name value")
                return
            
            name = args[0]
            value = " ".join(args[1:])
            
            self.vars.set(name, value)
            clean_name = name.lstrip('@')
            print(f"{self.INFO}Variable set: @{clean_name} = {value}")
    
    def _cmd_sort(self, args, cmd_type):
        """Sorted slots or loads list"""
        if cmd_type == "sorts":
            self._cmd_show(["slots"])
        elif cmd_type == "sortl":
            self._cmd_show(["loads"])
    
    def _cmd_sort_id(self, args):
        """Sort IDs"""
        if not args:
            print(f"{self.ERROR}Usage: sort id slots|loads")
            return
        
        if len(args) < 2 or args[0] != "id":
            print(f"{self.ERROR}Usage: sort id slots|loads")
            return
        
        sort_type = args[1].lower()
        
        if sort_type == "slots":
            count = self.slots.sort_ids()
            print(f"{self.INFO}Slot IDs sorted: {count} slots renumbered")
        
        elif sort_type == "loads":
            count = self.loads.sort_ids()
            print(f"{self.INFO}Load IDs sorted: {count} loads renumbered")
        
        else:
            print(f"{self.ERROR}Unknown sort type: {sort_type}")
    
    def _cmd_shell(self, args):
        """Shell command execution"""
        if not args:
            print(f"{self.ERROR}Usage: shell <command>")
            return
        
        command = " ".join(args)
        self._execute_shell(command)
    
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
        if not args:
            print(f"{self.ERROR}Usage: edit slot|load <id|name>")
            return
        
        edit_type = args[0].lower()
        
        if edit_type == "slot":
            if len(args) < 2:
                print(f"{self.ERROR}Usage: edit slot <id|name>")
                return
            
            identifier = args[1]
            slot = self.slots.get(identifier) or self.slots.find_by_name(identifier)
            
            if not slot:
                print(f"{self.ERROR}Slot not found: {identifier}")
                return
            
            print(f"{self.INFO}Interactive slot edit")
            print(f"1. Name: {slot['name']}")
            print(f"2. Command: {slot['command']}")
            print(f"{self.INFO}Enter field number to edit (1-2) or 'c' to cancel:")
            
            try:
                choice = input("Choice> ").strip().lower()
                
                if choice == '1' or choice == 'name':
                    new_name = input(f"New name [{slot['name']}]> ").strip()
                    if new_name:
                        self.slots.delete(identifier)
                        new_id = self.slots.create(slot['command'], new_name)
                        print(f"{self.INFO}Slot updated: {new_id} ({new_name})")
                
                elif choice == '2' or choice == 'command':
                    new_command = input(f"New command [{slot['command']}]> ").strip()
                    if new_command:
                        self.slots.delete(identifier)
                        new_id = self.slots.create(new_command, slot['name'])
                        print(f"{self.INFO}Slot updated: {new_id} ({slot['name']})")
                
                elif choice == 'c' or choice == 'cancel':
                    print(f"{self.WARNING}Edit cancelled")
                
                else:
                    print(f"{self.ERROR}Invalid choice")
            
            except KeyboardInterrupt:
                print(f"\n{self.WARNING}Edit cancelled")
            except Exception as e:
                print(f"{self.ERROR}Edit failed: {e}")
        
        elif edit_type == "load":
            if len(args) < 2:
                print(f"{self.ERROR}Usage: edit load <id|name>")
                return
            
            identifier = args[1]
            load = self.loads.get(identifier)
            
            if not load:
                print(f"{self.ERROR}Load not found: {identifier}")
                return
            
            print(f"{self.INFO}Interactive load edit")
            print(f"1. Name: {load['name']}")
            print(f"2. Slots: {', '.join(map(str, load['slot_ids']))}")
            print(f"3. Mode: {load['mode']}")
            print(f"{self.INFO}Enter field number to edit (1-3) or 'c' to cancel:")
            
            try:
                choice = input("Choice> ").strip().lower()
                
                if choice == '1' or choice == 'name':
                    new_name = input(f"New name [{load['name']}]> ").strip()
                    if new_name:
                        self.loads.edit_load(identifier, name=new_name)
                        print(f"{self.INFO}Load name updated: {new_name}")
                
                elif choice == '2' or choice == 'slots':
                    new_slots = input(f"New slots (comma separated) [{', '.join(map(str, load['slot_ids']))}]> ").strip()
                    if new_slots:
                        slot_ids = [int(x.strip()) for x in new_slots.split(',')]
                        self.loads.edit_load(identifier, slot_ids=slot_ids)
                        print(f"{self.INFO}Load slots updated")
                
                elif choice == '3' or choice == 'mode':
                    new_mode = input(f"New mode (s=serial, p=parallel) [{load['mode']}]> ").strip().lower()
                    if new_mode:
                        mode_map = {"s": "serial", "p": "parallel"}
                        final_mode = mode_map.get(new_mode, new_mode)
                        self.loads.edit_load(identifier, mode=final_mode)
                        print(f"{self.INFO}Load mode updated: {final_mode}")
                
                elif choice == 'c' or choice == 'cancel':
                    print(f"{self.WARNING}Edit cancelled")
                
                else:
                    print(f"{self.ERROR}Invalid choice")
            
            except KeyboardInterrupt:
                print(f"\n{self.WARNING}Edit cancelled")
            except Exception as e:
                print(f"{self.ERROR}Edit failed: {e}")
        
        else:
            print(f"{self.ERROR}Unknown edit type: {edit_type}")
    
    def _cmd_use(self, args):
        """Use slot or load"""
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
        """Create slot or load"""
        if not args:
            print(f"{self.INFO}Interactive create menu")
            print("1. Create Slot")
            print("2. Create Load")
            print(f"{self.INFO}Enter choice (1-2) or 'c' to cancel:")
            
            try:
                choice = input("Choice> ").strip()
                
                if choice == '1':
                    self._interactive_create_slot()
                elif choice == '2':
                    self._interactive_create_load()
                elif choice == 'c' or choice.lower() == 'cancel':
                    print(f"{self.WARNING}Cancelled")
                else:
                    print(f"{self.ERROR}Invalid choice")
            except KeyboardInterrupt:
                print(f"\n{self.WARNING}Cancelled")
            except Exception as e:
                print(f"{self.ERROR}Create failed: {e}")
            return
        
        create_type = args[0].lower()
        
        if create_type == "slot":
            if len(args) < 2:
                self._interactive_create_slot()
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
                name = f"slot_{len(self.slots.list_all()) + 1}"
            
            slot_id = self.slots.create(command, name)
            print(f"{self.INFO}Slot created: {slot_id} ({name})")
        
        elif create_type == "load":
            if len(args) < 2:
                self._interactive_create_load()
                return
            
            slots_str = args[1]
            name = None
            mode = "serial"
            
            i = 2
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
            
            try:
                slot_ids = [int(x.strip()) for x in slots_str.split(',')]
                load_id = self.loads.create_load(name, slot_ids, mode)
                print(f"{self.INFO}Load created: {load_id} ({name}, mode: {mode})")
            except ValueError:
                print(f"{self.ERROR}Invalid slot IDs. Use format: 1,2,3")
        
        else:
            print(f"{self.ERROR}Unknown create type: {create_type}")
    
    def _interactive_create_slot(self):
        """Interactive slot creation"""
        print(f"{self.INFO}Interactive slot creation")
        
        name = input("Slot name: ").strip()
        if not name:
            name = f"slot_{len(self.slots.list_all()) + 1}"
        
        command = input("Command: ").strip()
        if not command:
            print(f"{self.WARNING}Cancelled - command required")
            return
        
        slot_id = self.slots.create(command, name)
        print(f"{self.INFO}Slot created: {slot_id} ({name})")
    
    def _interactive_create_load(self):
        """Interactive load creation"""
        print(f"{self.INFO}Interactive load creation")
        
        slots_list = self.slots.list_all()
        if not slots_list:
            print(f"{self.ERROR}No slots found. Create slots first.")
            return
        
        print(f"\n{self.INFO}Available slots:")
        for slot in slots_list:
            print(f"  [{slot['id']}] {slot['name']}: {slot['command'][:30]}...")
        
        name = input("\nLoad name: ").strip()
        if not name:
            print(f"{self.WARNING}Cancelled - name required")
            return
        
        slots_input = input("Slot IDs (comma separated, e.g., 1,2,3): ").strip()
        if not slots_input:
            print(f"{self.WARNING}Cancelled - slots required")
            return
        
        try:
            slot_ids = [int(x.strip()) for x in slots_input.split(',')]
        except ValueError:
            print(f"{self.ERROR}Invalid slot IDs")
            return
        
        mode = input("Mode (s=serial, p=parallel) [s]: ").strip().lower()
        if not mode:
            mode = "serial"
        elif mode == 's':
            mode = "serial"
        elif mode == 'p':
            mode = "parallel"
        
        load_id = self.loads.create_load(name, slot_ids, mode)
        print(f"{self.INFO}Load created: {load_id} ({name}, mode: {mode})")
    
    def _cmd_delete(self, args):
        """Delete slot, var, or load"""
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
{self.INFO}ECHTABLE Framework:

{self.WARNING}Basic:
  help                    Show this help
  exit, quit             Exit framework
  clear                  Clear screen
  shell <cmd>            Execute shell command
  +<cmd>                 Quick shell command (e.g., +ls, +cd)

{self.WARNING}Show Commands:
  show slots             List all slots
  show vars              List all variables
  show loads             List all loads
  show slot <id|name>    Show slot details
  show var <name>        Show variable value
  show load <id|name>    Show load details

{self.WARNING}Sort Commands:
  sorts                  Show sorted slots
  sortl                  Show sorted loads
  sort id slots         Reorder slot IDs (1,2,3...)
  sort id loads         Reorder load IDs

{self.WARNING}Variable Operations:
  var @name value        Set/update variable
  var delete @name       Delete variable

{self.WARNING}Slot Operations:
  use <id|name>          Activate slot
  runs <id|name>         Run slot
  create slot <cmd> --name <name>  Create new slot
  create                 Interactive create menu
  edit slot <id|name>    Edit slot (interactive)
  delete slot <id|name>  Delete slot

{self.WARNING}Load Operations:
  use load <id|name>     Activate load
  runl <id|name>         Run load
  create load <1,2,3> --name <name> --mode s|p
  create                 Interactive create menu
  edit load <id|name>    Edit load (interactive)
  delete load <id|name>  Delete load

{self.WARNING}Mode Shortcuts:
  s = serial, p = parallel

{self.WARNING}Examples:
  var @target 10.10.10.5
  create slot nmap -sV @target --name scan
  runs scan
  create load 1,2,3 --name fullscan --mode p
  runl fullscan
  +ls
  +cd /tmp
        """
        print(help_text)

def start_framework():
    """Start the framework"""
    framework = ECHTableFramework()
    framework.start()

if __name__ == "__main__":
    start_framework()
