# Monitor Cisco Secure Access Network Tunnel State

## Use Cases

The Monitor Secure Access Network Tunnel State script checks the state of your organization's Network Tunnels (TunnelState), and logs the tunnel state information received from the Umbrella Network Tunnels API. If configured to generate email alerts, the script sends an email message about the state of a tunnel or the status of a Secure Access Network Tunnel API response.

The script alerts on these conditions:

* Secure Access Network Tunnel state that is  `disconnected`.
* Secure Access Tunnel state that is `warning`.

## Prerequisites

* Python 3.x.x
* Cisco Secure Access
* Create an App password for the desired email to send the notification from, save the App Password in the PASSWD environment variable
* Modify the recipients variable in the tunnel_monitor_sse.py and enter the desired email address to send the notifications from


## Before You Begin

* Create a Secure Access Management API key.
* Install Python libraries. For more information, see `Requirements.txt`.

  ```shell
  pip install -r requirements.txt
  ```
* Create environment variables:
* export API_KEY=VALUE
* export API_SECRET=VALUE
* export PASSWD=VALUE
* export EMAIL=VALUE


## Usage

* Run the sample script:

  ```shell
    python3 tunnel_monitor_sse.py
  ```



