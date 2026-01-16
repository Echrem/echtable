"""
ECHTABLE Command Executor
Executes shell commands
"""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

class CommandExecutor:
    """Executes shell commands"""
    
    @staticmethod
    def execute(command, capture_output=False):
        """Execute a single command"""
        try:
            print(f"\n[→] Executing: {command}")
            print("-" * 60)
            
            if capture_output:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    executable="/bin/bash"
                )
                
                print(result.stdout)
                if result.stderr:
                    print(f"STDERR: {result.stderr}", file=sys.stderr)
                
                return {
                    "success": result.returncode == 0,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "command": command
                }
            else:
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    executable="/bin/bash"
                )
                
                process.wait()
                
                return {
                    "success": process.returncode == 0,
                    "returncode": process.returncode,
                    "command": command
                }
                
        except Exception as e:
            print(f"[!] Execution error: {e}", file=sys.stderr)
            return {
                "success": False,
                "error": str(e),
                "command": command
            }
    
    @staticmethod
    def execute_serial(commands):
        """Execute commands sequentially"""
        results = []
        for cmd in commands:
            result = CommandExecutor.execute(cmd, capture_output=False)
            results.append(result)
            
            if not result["success"]:
                print(f"[!] Command failed: {cmd}")
        
        return results
    
    @staticmethod
    def execute_parallel(commands, max_workers=3):
        """Execute commands in parallel"""
        results = []
        
        def run_command(cmd):
            return CommandExecutor.execute(cmd, capture_output=True)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(run_command, cmd) for cmd in commands]
            for future in futures:
                results.append(future.result())
        
        return results
