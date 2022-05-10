# Monitor Cisco Umbrella Network Tunnel State

## Use Cases

The Monitor Umbrella Network Tunnel State script checks the state of your organization's Network Tunnels (TunnelState), and logs the tunnel state information received from the Umbrella Network Tunnels API. If configured to generate email alerts, the script sends an email message about the state of a tunnel or the status of an Umbrella Network Tunnel API response.

The script alerts on these conditions:

* Umbrella Network Tunnel API response status that is not `200/OK`.
* Umbrella Network Tunnel state that is not `UP`. Check for the following Network Tunnel states: `DOWN`, or `FAILED`.
* Umbrella Network Tunnel state that is `UP`, but last modified timestamp is not updated within the configured interval.

## Prerequisites

* Python 3.x.x
* Cisco Umbrella

## Before You Begin

* Create an Umbrella Management API key.
* Install Python libraries. For more information, see `Requirements.txt`.

  ```shell
  pip install -r Requirements.txt
  ```
* Create a `credentials.json` file from the `SAMPLE_CREDENTIALS.json` template. Update the fields in `credentials.json` with your data.

## Usage

* Run the sample script:

  ```shell
  python3 main.py
  ```

## Troubleshooting

If you are unable to access the Umbrella Network Tunnels API and the Umbrella TunnelState resource, or you have not configured an email server, check your Umbrella Management API key, Umbrella subscription, or data configured in `credentials.json`. A `404` response looks similar to:

```shell
Checking Tunnel Status at 2022-05-09 11:33:33.979461
============================================================
GET /tunnelsState
Response: Status = 404, Message Content = {"error":"Tunnels states not found for organization"}
ERROR: Response Status is not 200/OK
Update Tunnel States Result: {"update status": "Script fail", "reason": "ERROR: API Request fail, status = 404"}
Error detected
Email alert enabled, send email alert.
Try connection to mail server.
Error connecting to email server please run connect() first.
Tunnel Status Check completed. Wait 120 seconds before next status check.
```

## Try Out Cisco DevNet Sandbox

You can run the script against an instance of the Cisco Umbrella Secure Internet Gateway Sandbox.

The DevNet Sandboxes provide developers with zero-cost, flexible access to cloud-native development environments. Within the Cisco Umbrella Secure Internet Gateway Sandbox, you can develop and run code that interacts with the Umbrella APIs. For more information, see [Cisco Security Sandboxes](https://devnetsandbox.cisco.com/RM/Topology?c=a6f8430c-5b24-439d-b28a-effb42d4c20c) in the Sandbox Catalog.
