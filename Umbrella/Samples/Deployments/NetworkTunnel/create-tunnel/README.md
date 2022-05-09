# Create Cisco Umbrella Network Tunnels

## Use Cases

The Create Umbrella Network Tunnel script registers Umbrella Network Tunnels for your organization, and logs the response from the Umbrella Network Tunnels API. Set up your tunnel attributes in `tunnel_data.csv` to create each tunnel.

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

  Sample `credentials.json`:

  ```json
  {
    "key": "",
    "secret": "",
    "org_id": "",
    "log_file": "tunnel_log",
    "tunnel_data": "tunnel_data.csv",
    "debug": true
  }
  ```

* Modify `tunnel_data.csv` with your tunnel attributes.

## Usage

* Run the sample script:

  ```shell
  python3 main.py
  ```

## Troubleshooting

If you are unable to create an Umbrella Network Tunnel, check your Umbrella Management API key, Umbrella subscription, or data configured in `credentials.json` and `tunnel_data.json`.

The script generates log files named using the following format:

```ini
<log filename>_<YYYY_MM_DD_HH_MM>.csv
```

For example:

```ini
tunnel_log_2022_05_09_12_43.csv
```

### Duplicate Network Tunnel Name Error

A duplicate tunnel name error looks similar to:

```shell
Error creating tunnel04test, see log for details
[createTunnel()] response = {"error":"Tunnel Name must be unique."}
[write_tunnel_attributes()] line = tunnel04test,Meraki MX,,ABCDEF9876543210fedcba,,,Tunnel Name must be unique.,
```

## Try Out Cisco DevNet Sandbox

You can run the script against an instance of the Cisco Umbrella Secure Internet Gateway Sandbox.

The DevNet Sandboxes provide developers with zero-cost, flexible access to cloud-native development environments. Within the Cisco Umbrella Secure Internet Gateway Sandbox, you can develop and run code that interacts with the Umbrella APIs. For more information, see [Cisco Security Sandboxes](https://devnetsandbox.cisco.com/RM/Topology?c=a6f8430c-5b24-439d-b28a-effb42d4c20c) in the Sandbox Catalog.
