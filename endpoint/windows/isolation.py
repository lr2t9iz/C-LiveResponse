
# Written by lr2t9iz (2024.04.02) - updated(2025.03.09)
# Ref: https://documentation.wazuh.com/current/user-manual/capabilities/active-response/custom-active-response-scripts.html

import sys
import json
from datetime import datetime
import subprocess
import ipaddress

from pathlib import Path
WAR_DIR = Path("C:/Program Files (x86)/ossec-agent/active-response")
LOG_FILE = WAR_DIR / "active-responses.log"
debug_file = WAR_DIR / "isolation.log"
backup_dir = WAR_DIR / "backup"
fw_rules_file = backup_dir / "fw_rules.xml"

def debug(message):
  with open(debug_file, 'a') as file:
    file.write(f"{message}\n")  

def output(input_program, action, by_user, result, stderr, log_h):
  cmd_result = {
    "command": "add",
    "origin": { "name": "WLR", "module": "Isolation" },
    "parameters": { "program": input_program },
    "wlr": { 
      "action": action,
      "user": by_user,
      "result": f"stdout: {result}\nstderr: {stderr}"
    }
  }
  with open(LOG_FILE, 'a') as file:
    file.write(f"{log_h}: {json.dumps(cmd_result)}\n")

def is_valid_ip(ip):
    try:
        ipaddress.ip_network(ip, strict=False)  # IPv4 & IPv6
        return True
    except ValueError:
        return False

def isolate(ip_exeption):
  results_out = []
  results_err = []
  if not all(is_valid_ip(ip) for ip in ip_exeption):
    return [""], ["One or more IP addresses are invalid."]
  
  backup_dir.mkdir(parents=True, exist_ok=True)
  
  if fw_rules_file.exists() and fw_rules_file.is_file():
    return [""], ["The device is already isolated, no action was taken."]

  r = subprocess.run(["cmd", "/c", "netsh", "advfirewall", "export", str(fw_rules_file)], capture_output=True, text=True)
  results_out.append(r.stdout)
  results_err.append(r.stderr)
  r = subprocess.run(["cmd", "/c", "netsh", "advfirewall", "firewall", "delete", "rule", "name=all"], capture_output=True, text=True)
  results_out.append(r.stdout)
  results_err.append(r.stderr)
  r = subprocess.run(["cmd", "/c", "netsh", "advfirewall", "set", "allprofiles", "state", "on"], capture_output=True, text=True)
  results_out.append(r.stdout)
  results_err.append(r.stderr)
  r = subprocess.run(["cmd", "/c", "netsh", "advfirewall", "set", "allprofiles", "firewallpolicy", "blockinbound,blockoutbound"], capture_output=True, text=True)
  results_out.append(r.stdout)
  results_err.append(r.stderr)
  for ip in ip_exeption:
    r = subprocess.run(["cmd", "/c", "netsh", "advfirewall", "firewall", "add", "rule", 
                        "name=allow-siem-in", "dir=in", "action=allow", "protocol=any", f"remoteip={ip}"], capture_output=True, text=True)
    results_out.append(r.stdout)
    results_err.append(r.stderr)
    r = subprocess.run(["cmd", "/c", "netsh", "advfirewall", "firewall", "add", "rule", 
                        "name=allow-siem-out", "dir=out", "action=allow", "protocol=any", f"remoteip={ip}"], capture_output=True, text=True)
    results_out.append(r.stdout)
    results_err.append(r.stderr)
  return results_out, results_err

def release():
  if fw_rules_file.exists() and fw_rules_file.is_file():
    result = subprocess.run(f'cmd /c netsh advfirewall import "{fw_rules_file}"', 
      capture_output=True, text=True)
    fw_rules_file.unlink()
    return result.stdout, result.stderr
  else:
    return [''], ['The host is not isolated, or the backup has been removed.']

def main():
  input_str = sys.stdin.readline()
  current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

  try: 
    input_json = json.loads(input_str)
  except json.JSONDecodeError:
    output("Isolation.WLR", "error", "system", "", "Invalid JSON input received.", f"{current_datetime} Isolation.WLR")
    sys.exit(1)

  input_parameters = input_json.get('parameters')
  input_program = input_parameters.get('program')

  log_h = f"{current_datetime} {input_program}"

  ip_exeption = input_parameters.get('extra_args')
  action = input_parameters.get('alert', {}).get('data', {}).get('action', 'unknown')
  by_user = input_parameters.get('alert', {}).get('data', {}).get('user', 'unknown')
  debug_mode = input_parameters.get('alert', {}).get('data', {}).get('debug', False)
  
  if debug_mode:
    debug(f"main: {input_str}")

  if by_user:
    if action == "isolate":
      stdout, stderr = isolate(ip_exeption)
      stdout = ' '.join(stdout).replace("\n", " ")
      stderr = ' '.join(stderr).replace("\n", " ")
      output(input_program, action, by_user, stdout, stderr, log_h)
    elif action == "release":
      stdout, stderr = release()
      stdout = ' '.join(stdout).replace("\n", " ")
      stderr = ' '.join(stderr).replace("\n", " ")
      output(input_program, action, by_user, stdout, stderr, log_h)
    else:
      output(input_program, action, by_user, "", "No action was provided. Please specify an action in the alert [isolate, release] > data.", log_h)
  else:
    output(input_program, action, by_user, "", "No user was provided. Please specify a user in the alert > data, for audit.", log_h)

if __name__ == "__main__":
  main()
