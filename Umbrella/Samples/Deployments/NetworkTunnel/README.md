# Umbrella Network Tunnel State Sample Script

## Use Cases

The sample script checks the Umbrella Network Tunnel status within an organization. The script uses the Umbrella API to report on the state of each tunnel and alert on these conditions:

* Network Tunnel API response status that is not `200/OK`.
* Network Tunnel state that is not _UP_. Check for the following Network Tunnel states: _DOWN_, or _FAILED_.
* Network Tunnel state that is _UP_, but last modified timestamp is not updated within the configured interval.

## Prerequisites

Python 3.x.x

## Installation

```shell
pip install -r Requirements.txt
```

## Usage

* Update the fields in `SAMPLE_CREDENTIALS.json` with your data. You must generate `credentials.json` using the `SAMPLE_CREDENTIALS.json` template.
* Run the sample script with the default parameters:

  ```shell
  python3 main.py
  ```

### Try Out With Cisco DevNet Sandbox

You can run the script against an instance of the Cisco Umbrella Secure Internet Gateway Sandbox.

The DevNet Sandboxes provide developers with zero-cost, flexible access to cloud-native development environments. Within the Cisco Umbrella Secure Internet Gateway Sandbox, you can develop and run code that interacts with the Umbrella APIs. For more information, see [Cisco Security Sandboxes](https://devnetsandbox.cisco.com/RM/Topology?c=a6f8430c-5b24-439d-b28a-effb42d4c20c) in the Sandbox Catalog.
