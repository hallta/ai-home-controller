#!/usr/bin/env python3
"""
Script to run 'cat garage.prompt | ollama run llava' in an infinite loop.
Runs in the foreground with a 30 second sleep between iterations.
"""

import os
import sys
import time
import signal
import subprocess
from datetime import datetime


def tlog(message):
    """Log a message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def signal_handler(signum, frame):
    """Handle termination signals."""
    tlog("Shutting down...")
    sys.exit(0)


def main():
    """Main loop to run the command repeatedly."""
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Get the script directory
    workdir = os.path.dirname(os.path.abspath(__file__))
    prompt_file = os.path.join(workdir, 'garage.prompt')
    
    tlog("Starting garage monitoring loop (Ctrl+C to stop)...")
    
    iteration = 0
    while True:
        iteration += 1
        tlog(f"Starting iteration {iteration}")
        
        try:
            tlog(f"Reading prompt file: {prompt_file}")
            # Run the command
            with open(prompt_file, 'r') as f:
                tlog(f"Executing: ollama run qwen3-vl:30b")
                process = subprocess.Popen(
                    ['ollama', 'run', 'qwen3-vl:30b'],
                    stdin=f,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=workdir
                )
                # Wait for completion (with timeout to prevent hanging)
                try:
                    tlog(f"Waiting for command to complete...")
                    stdout, stderr = process.communicate(timeout=120)
                    if process.returncode == 0:
                        tlog(f"Command completed successfully (exit code: {process.returncode})")
                    else:
                        tlog(f"Command completed with exit code: {process.returncode}", file=sys.stderr)
                        if stderr:
                            tlog(f"Stderr: {stderr.decode('utf-8', errors='ignore')}", file=sys.stderr)
                except subprocess.TimeoutExpired:
                    tlog(f"Command timed out after 60 seconds, killing process...", file=sys.stderr)
                    process.kill()
                    stdout, stderr = process.communicate()
                
        except FileNotFoundError as e:
            tlog(f"Error: ollama command not found or garage.prompt file missing: {e}", file=sys.stderr)
            tlog(f"Waiting 30 seconds before retry...")
            time.sleep(30)
            continue
        except KeyboardInterrupt:
            signal_handler(None, None)
        except Exception as e:
            tlog(f"Error: {e}", file=sys.stderr)
            tlog(f"Waiting 30 seconds before retry...")
            time.sleep(30)
            continue
        
        # Sleep for 30 seconds before next run
        tlog(f"Iteration {iteration} complete.")

        # INSERT_YOUR_CODE
        # Parse stdout (string) for JSON, load as object

        import json
        import re

        stdout_str = stdout.decode('utf-8', errors='ignore') if isinstance(stdout, bytes) else str(stdout)

        # Find the JSON substring - look for {...} pattern
        match = re.search(r'\{.*\}', stdout_str, re.DOTALL)
        if match:
            json_str = match.group()
            obj = json.loads(json_str)
            tlog(f"door opening: {obj['door_opening']['state']}")
        else:
            print("No JSON found")


            ## 
        
        tlog(f"Sleeping for 30 seconds...")
        time.sleep(30)


if __name__ == '__main__':
    main()
