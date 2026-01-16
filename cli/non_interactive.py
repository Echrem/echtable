"""
ECHTABLE Non-Interactive CLI
Fast command-line interface for quick operations
"""

import sys
import json
from core.slots import SlotManager
from core.variables import VariableManager
from core.loads import LoadManager
from core.executor import CommandExecutor
from cli.parser import parse_echt_args

def main():
    """
    Main entry point for non-interactive CLI
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    args = parse_echt_args()
    
    if not args.command:
        print("Error: No command specified. Use 'echt --help' for usage.")
        return 1
    
    try:
        # === SLOT COMMANDS ===
        if args.command == "slot":
            slots = SlotManager()
            
            if args.slot_cmd == "create":
                slot_id = slots.create(args.command, args.name)
                print(f"[+] Slot created: {slot_id} ({args.name})")
                
            elif args.slot_cmd == "run":
                # Find slot
                slot = slots.get(args.identifier) or slots.find_by_name(args.identifier)
                if not slot:
                    print(f"[!] Slot not found: {args.identifier}")
                    return 1
                
                # Prepare and execute command
                command = slots.prepare_command(slot["id"], args.params)
                if not command:
                    print(f"[!] Could not prepare command for slot {args.identifier}")
                    return 1
                
                result = CommandExecutor.execute(command)
                if not result["success"]:
                    print(f"[!] Command failed")
                    return 1
                
            elif args.slot_cmd == "list":
                slots_list = slots.list_all()
                if not slots_list:
                    print("[*] No slots found")
                else:
                    print("\nID  Name            Command")
                    print("-" * 50)
                    for slot in slots_list:
                        cmd_preview = slot["command"][:30] + "..." if len(slot["command"]) > 30 else slot["command"]
                        print(f"{slot['id']:<3} {slot['name']:<15} {cmd_preview}")
                
            elif args.slot_cmd == "delete":
                if slots.delete(args.identifier):
                    print(f"[+] Slot deleted: {args.identifier}")
                else:
                    print(f"[!] Slot not found: {args.identifier}")
                    return 1
        
        # === VARIABLE COMMANDS ===
        elif args.command == "var":
            vars = VariableManager()
            
            if args.var_cmd == "set":
                vars.set(args.name, args.value)
                clean_name = args.name.lstrip('@')
                print(f"[+] Variable set: @{clean_name} = {args.value}")
                
            elif args.var_cmd == "get":
                value = vars.get(args.name)
                clean_name = args.name.lstrip('@')
                print(f"@{clean_name} = {value}")
                
            elif args.var_cmd == "list":
                vars_list = vars.list_all()
                if not vars_list:
                    print("[*] No variables found")
                else:
                    print("\nVariable       Value")
                    print("-" * 40)
                    for var in vars_list:
                        print(f"{var['name']:<15} {var['value']}")
                
            elif args.var_cmd == "delete":
                if vars.delete(args.name):
                    clean_name = args.name.lstrip('@')
                    print(f"[+] Variable deleted: @{clean_name}")
                else:
                    print(f"[!] Variable not found: {args.name}")
                    return 1
        
        # === LOAD COMMANDS ===
        elif args.command == "load":
            loads = LoadManager()
            
            if args.load_cmd == "create":
                # Parse slot IDs
                slot_ids = [int(x.strip()) for x in args.slots.split(',')]
                loads.create_load(args.name, slot_ids, args.mode)
                print(f"[+] Load created: {args.name} (slots: {slot_ids}, mode: {args.mode})")
                
            elif args.load_cmd == "run":
                load = loads.get(args.name)
                if not load:
                    print(f"[!] Load not found: {args.name}")
                    return 1
                
                print(f"[+] Running load: {args.name}")
                print(f"[*] Slots: {load['slot_ids']}")
                print(f"[*] Mode: {load['mode']}")
                
                # TODO: Implement load execution
                print("[*] Load execution coming soon...")
                
            elif args.load_cmd == "list":
                loads_list = loads.list_all()
                if not loads_list:
                    print("[*] No loads found")
                else:
                    print("\nName            Slots           Mode")
                    print("-" * 50)
                    for load in loads_list:
                        slots_str = ', '.join(map(str, load['slots']))
                        print(f"{load['name']:<15} {slots_str:<15} {load['mode']}")
        
        # === QUICK RUN ALIAS ===
        elif args.command == "run":
            slots = SlotManager()
            
            # Find slot
            slot = slots.get(args.identifier) or slots.find_by_name(args.identifier)
            if not slot:
                print(f"[!] Slot not found: {args.identifier}")
                return 1
            
            # Prepare and execute command
            command = slots.prepare_command(slot["id"], args.params)
            if not command:
                print(f"[!] Could not prepare command for slot {args.identifier}")
                return 1
            
            print(f"[+] Running slot: {slot['name']}")
            result = CommandExecutor.execute(command)
            if not result["success"]:
                print(f"[!] Command failed")
                return 1
        
        # === QUICK SET ALIAS ===
        elif args.command == "set":
            vars = VariableManager()
            vars.set(args.name, args.value)
            clean_name = args.name.lstrip('@')
            print(f"[+] Set: @{clean_name} = {args.value}")
        
        return 0
        
    except Exception as e:
        print(f"[!] Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
