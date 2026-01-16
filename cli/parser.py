"""
ECHTABLE Argument Parser
Parses command-line arguments
"""

import argparse

def parse_echt_args():
    """Parse command-line arguments for echt command"""
    parser = argparse.ArgumentParser(
        prog="echt",
        description="ECHTABLE Fast CLI - Execute stored commands quickly",
        epilog="Example: echt run 1 10.10.10.1"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Slot commands
    slot_parser = subparsers.add_parser("slot", help="Slot operations")
    slot_sub = slot_parser.add_subparsers(dest="slot_cmd")
    
    create_slot = slot_sub.add_parser("create", help="Create new slot")
    create_slot.add_argument("command", help="Command to store")
    create_slot.add_argument("--name", required=True, help="Slot name")
    
    run_slot = slot_sub.add_parser("run", help="Run slot")
    run_slot.add_argument("identifier", help="Slot ID or name")
    run_slot.add_argument("params", nargs="*", help="Extra parameters")
    
    slot_sub.add_parser("list", help="List all slots")
    
    delete_slot = slot_sub.add_parser("delete", help="Delete slot")
    delete_slot.add_argument("identifier", help="Slot ID or name")
    
    # Variable commands
    var_parser = subparsers.add_parser("var", help="Variable operations")
    var_sub = var_parser.add_subparsers(dest="var_cmd")
    
    set_var = var_sub.add_parser("set", help="Set variable")
    set_var.add_argument("name", help="Variable name")
    set_var.add_argument("value", help="Variable value")
    
    get_var = var_sub.add_parser("get", help="Get variable value")
    get_var.add_argument("name", help="Variable name")
    
    var_sub.add_parser("list", help="List all variables")
    
    delete_var = var_sub.add_parser("delete", help="Delete variable")
    delete_var.add_argument("name", help="Variable name")
    
    # Load commands
    load_parser = subparsers.add_parser("load", help="Load operations")
    load_sub = load_parser.add_subparsers(dest="load_cmd")
    
    create_load = load_sub.add_parser("create", help="Create load")
    create_load.add_argument("slots", help="Comma-separated slot IDs")
    create_load.add_argument("--name", required=True, help="Load name")
    create_load.add_argument("--mode", choices=["serial", "parallel"], default="serial", help="Execution mode")
    
    run_load = load_sub.add_parser("run", help="Run load")
    run_load.add_argument("name", help="Load name")
    
    load_sub.add_parser("list", help="List all loads")
    
    # Quick aliases
    run_parser = subparsers.add_parser("run", help="Quick run slot")
    run_parser.add_argument("identifier", help="Slot ID or name")
    run_parser.add_argument("params", nargs="*", help="Extra parameters")
    
    set_parser = subparsers.add_parser("set", help="Quick set variable")
    set_parser.add_argument("name", help="Variable name")
    set_parser.add_argument("value", help="Variable value")
    
    return parser.parse_args()
