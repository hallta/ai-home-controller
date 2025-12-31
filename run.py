#!/usr/bin/env python3
"""
Script to run 'cat garage.prompt | ollama run llava' in an infinite loop.
Runs in the foreground with a 30 second sleep between iterations.
"""

import json
import os
import re
import signal
import subprocess
import sys
import time
from datetime import datetime


LLM_TIMEOUT = 600  # seconds

class GarageState:
    def __init__(self, obj: dict):
        self.door_opening = obj['door_opening']['state']
        self.car_moving = obj['car_moving']['state']
        self.person_moving = obj['person_moving']['state']
        self.car_moving_direction = obj['car_moving']['direction']
        self.reasoning = obj['door_opening']['reasoning']

    def __eq__(self, other):
        return (self.door_opening == other.door_opening and
                self.car_moving == other.car_moving and
                self.person_moving == other.person_moving and
                self.car_moving_direction == other.car_moving_direction and
                self.reasoning == other.reasoning)

    def __str__(self):
        return f"GarageState(door_opening={self.door_opening}, car_moving={self.car_moving}, person_moving={self.person_moving}, direction={self.car_moving_direction})"

    def should_act(self):
        return self.car_moving or self.person_moving

    def act(self):
        if self.should_act():
            tlog(f"Acting..., {self.reasoning}")
            if self.car_moving:
                tlog(f"Car moving..., {self.reasoning}")

                # When we spot a car moving, we will want to turn the lights on
                # when they are entering, but turn them off when they are exiting.
                if self.car_moving_direction == "Entering":
                    tlog(f"Car entering..., {self.reasoning}")
                else:
                    tlog(f"Car exiting..., {self.reasoning}")

            # When we spot a person moving, we will want to turn the lights on
            # and keep them on a bit longer than if a car is moving. 
            if self.person_moving:
                tlog(f"Person moving..., {self.reasoning}")
        else:
            tlog("Not acting...")


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
                    stdout, stderr = process.communicate(timeout=LLM_TIMEOUT)
                    if process.returncode == 0:
                        tlog(f"Command completed successfully (exit code: {process.returncode})")
                    else:
                        tlog(f"Command completed with exit code: {process.returncode}", file=sys.stderr)
                        if stderr:
                            tlog(f"Stderr: {stderr.decode('utf-8', errors='ignore')}", file=sys.stderr)
                except subprocess.TimeoutExpired:
                    tlog(f"Command timed out after {LLM_TIMEOUT} seconds, killing process...", file=sys.stderr)
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

        try:
            stdout_str = stdout.decode('utf-8', errors='ignore') if isinstance(stdout, bytes) else str(stdout)

            # find the json substring - look for {...} pattern
            match = re.search(r'\{.*\}', stdout_str, re.DOTALL)
            if match:
                json_str = match.group()
                try:
                    obj = json.loads(json_str)
                    garage_state = GarageState(obj)

                    garage_state.act()
                    tlog(f"GarageState: {garage_state}")
                except json.JSONDecodeError as e:
                    tlog(f"JSON decode error: {e}")
                except Exception as e:
                    tlog(f"Error initializing GarageState: {e}")
            else:
                tlog("No JSON found")
        except Exception as e:
            tlog(f"Error while processing stdout: {e}")

        tlog(f"Sleeping for 30 seconds...")
        time.sleep(30)


if __name__ == '__main__':
    main()
