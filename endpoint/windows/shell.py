
# Written by lr2t9iz (2024.04.07) - updated(2025.04.18)
# Ref: https://documentation.wazuh.com/current/user-manual/capabilities/active-response/custom-active-response-scripts.html

import sys
import json
from datetime import datetime
import subprocess


from pathlib import Path
WAR_DIR = Path("C:/Program Files (x86)/ossec-agent/active-response")
LOG_FILE = WAR_DIR / "active-responses.log"
debug_file = WAR_DIR / "shell.log"



def debug(message):
  with open(debug_file, 'a') as file:
    file.write(f"{message}\n")  

def output(input_program, commandline, by_user, result, stderr, log_h):
  part = 1
  for batch in result:
    cmd_result = {
      "command":"add",
      "origin": { "name": "C-LR", "module": "Shell" },
      "parameters": { "program": input_program },
      "clr": {
        "action": f"commandline: {commandline}",
        "user": by_user,
        "result": f"stdout: {batch}\nstder: {stderr}",
        "sequence": part
      }
    }
    with open(LOG_FILE, 'a') as file:
      file.write(f"{log_h}: {json.dumps(cmd_result)}\n")
      part=part+1

def parse(stdout, batch_size):
  lines = stdout.splitlines()
  batches = []
  for i in range(0, len(lines), batch_size):
    batch = lines[i:i+batch_size]
    batches.append("\n".join(batch))
  return batches

def cmdrun(command):
  result = subprocess.run(command, 
    capture_output=True, text=True)
  return result.stdout, result.stderr

def main():
  input_str = sys.stdin.readline()
  current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

  try:
    input_json = json.loads(input_str)
  except json.JSONDecodeError:
    output("C-LR Shell", "", "system", "", "Invalid JSON input received.", f"{current_datetime} C-LR Shell")
    sys.exit(1)

  input_parameters = input_json.get('parameters')
  input_program = input_parameters.get('program')

  log_h = f"{current_datetime} {input_program}"

  commandline = input_parameters.get('extra_args')[0]
  by_user = input_parameters.get('alert', {}).get('data', {}).get('user', 'unknown')
  debug_mode = input_parameters.get('alert', {}).get('data', {}).get('debug', False)

  if debug_mode:
    debug(f"main: {input_str}")
  
  if by_user:
    stdout, stderr = cmdrun(commandline)

    if stderr:
      stdout = "error"
    if not stdout and not stderr:
      stdout = "Command executed successfully"
    result = parse(stdout, 50)
    output(input_program, commandline, by_user, result, stderr, log_h)
  else:
    output(input_program, commandline, by_user, ["Command was not executed"], "No user was provided. Please specify a user in the alert > data, for audit.", log_h)

if __name__ == "__main__":
  main()
