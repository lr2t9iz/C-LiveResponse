# Wazuh Live Response (WLR)
Wazuh Live Response (WLR) is a Python-based module that enhances Wazuh by integrating external security solutions for better threat detection and incident response. It includes a structured framework for automated correlation and response, with the following components:

- **correlation/** contains rule modules that analyze collected Wazuh alerts to identify potential threats.
- **response/** defines action modules that execute specific responses when a threat is detected.
- **utils/** provides integrations with databases, APIs, and external services to enrich detections.
- **custom-xdr** orchestrates the correlation and response modules, dynamically managing detection and response workflows.
- **endpoint/** contains the executables that perform actions on Windows and Linux endpoints.

## Setup
To install Wazuh Live Response (WLR), initialize a Git repository inside the /var/ossec/integrations/ directory and pull the latest version. This method ensures that the module files are placed directly in the integrations folder rather than inside a subdirectory.
```sh
cd /var/ossec/integrations/
git init
git remote add origin https://github.com/lr2t9iz/wazuh-live-response.git
git pull origin main
```

## Requirements
```sh
cd /var/ossec/integrations/
/var/ossec/framework/python/bin/pip3 install --upgrade pip
/var/ossec/framework/python/bin/pip3 install -r requirements.txt
```

## Usage
### Repository wiki
The complete documentation is available in the [wiki](https://github.com/lr2t9iz/wazuh-live-response/wiki/)

# References
- https://documentation.wazuh.com/current/user-manual/manager/integration-with-external-apis.html
