# C-LR Shell
C-LR Shell is a module within C-LiveResponse (C-LR) that enables manual interrogation of a Windows system directly from the Wazuh DevTools console. This utility allows security teams to perform live response and threat hunting actions by sending CMD or PowerShell commands to endpoints through Wazuh's Active Response mechanism. It can be used to retrieve system state information such as active users, network connections, running processes, scheduled tasks, and more during incident investigation. Command outputs are sent back as events and can be viewed in the `Wazuh Explore > Discover` section, providing visibility and context within your existing telemetry.

## Windows Endpoint

### Installation & Setup
This process requires the user to have administrator privileges.
- Package the [shell.py](../../endpoint/windows/) script
- Alternatively, copy the [shell.exe](../../endpoint/windows/bin/) binary to the Active Response folder on the Windows agent `C:\Program Files (x86)\ossec-agent\active-response\bin\`
- Restart the Wazuh agent to apply the changes `Restart-Service -Name wazuh`

### Usage
For the use of the C-LR Shell, we will utilize the Wazuh API and the DevTools from the Server Management Dashboard to send commands to the endpoint. The module supports two main command execution methods:
- **CMD commands** must be prefixed with `cmd /c`, for example: `cmd /c net user`
- **PowerShell commands** must be prefixed with `powershell -c`, for example: `powershell -c Get-Process`
These commands are executed remotely via Wazuh's Active Response and the output can be reviewed directly in the Explore > Discover section of the Wazuh dashboard.
```json
# CMD Commands
PUT /active-response?agents_list=001
{
  "command": "!shell.exe",
  "arguments": ["cmd /c net user"],
  "alert": {
    "data": {
      "user": "c-137labs",
      "debug": false
    }
  }
}

# PowerShell Commands
PUT /active-response?agents_list=001
{
  "command": "!shell.exe",
  "arguments": ["powershell -c Get-NetTCPConnection -State Established"],
  "alert": {
    "data": {
      "user": "c-137labs",
      "debug": false
    }
  }
}
```
- `?agents_list=001`: Specifies the ID of the agent to be isolated, according to the Wazuh [API](https://documentation.wazuh.com/current/user-manual/api/reference.html) documentation, this parameter can accept a list of agent IDs to apply the action to multiple agents simultaneously.<br><br>
- `command`: Executes the shell.exe binary, the `!` is required before the command for proper execution in Wazuh.
- `arguments`: The command to be executed on the target endpoint. This must include the proper prefix depending on the shell used (`cmd /c` for CMD or `powershell -c` for PowerShell).
- `alert.data.user`: Specifies the user who triggered the action for auditing purposes.
- `alert.data.debug`: Used for development purposes; should be set to false in production.