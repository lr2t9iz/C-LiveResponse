# C-LR Isolation
C-LR Isolation is a module within C-LiveResponse (C-LR) that enables manual isolation of a Windows system directly from the Wazuh DevTools console. This feature allows security teams to contain threats by restricting network access to the affected endpoint. The system can also be released from isolation using the same method. The actions and results are logged and can be reviewed in the Wazuh logs, ensuring visibility and traceability of the response process.

## Windows Endpoint

### Installation & Setup
This process requires the user to have administrator privileges.
- Package the [isolation.py](../../endpoint/windows/) script
- Alternatively, copy the [isolation.exe](../../endpoint/windows/bin/) binary to the Active Response folder on the Windows agent `C:\Program Files (x86)\ossec-agent\active-response\bin\`
- Restart the Wazuh agent to apply the changes `Restart-Service -Name wazuh`

### Usage
For the use of the C-LR Isolation, we will utilize the Wazuh API and the DevTools from Server management Dashboard to send actions. The module accepts two main actions:
- The **isolate** action configures the Windows firewall to block all connections except those going to the Wazuh server.
- The **release** action restores the normal firewall configuration.

```json
PUT /active-response?agents_list=001
{
  "command": "!isolation.exe",
  "arguments": ["192.168.1.1", "192.168.1.2"],
  "alert": { 
    "data": { 
      "action": "isolate",
      "user": "c-137labs",
      "debug": false
    }
  }
}
```
- `?agents_list=001`: Specifies the ID of the agent to be isolated, according to the Wazuh [API](https://documentation.wazuh.com/current/user-manual/api/reference.html) documentation, this parameter can accept a list of agent IDs to apply the action to multiple agents simultaneously.<br><br>
- `command`: Executes the isolation.exe binary, the `!` is required before the command for proper execution in Wazuh.
- `arguments`: List of IP addresses that are allowed for communication, such as the Wazuh server and another necessary host.
- `alert.data.action`: Specifies the action to be performed (**isolate** or **release**).
- `alert.data.user`: Specifies the user who triggered the action for auditing purposes.
- `alert.data.debug`: Used for development purposes; should be set to false in production.

## 🔜 Linux Endpoint

