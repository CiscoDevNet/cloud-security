# AD Connector Monitor

## Use Cases

The AD Connector Monitor script sends email alerts when it detects an AD connector in error state.  
This is achieved by sending a GET request to https://api.umbrella.com/deployments/v2/virtualappliances to get all the AD integration components (VAs, DCs and AD connectors) from the dashboard. After this, the script checks the status of all AD connectors in the dashboard and if it finds an AD connector in error state, it will send an email alert to the specified recipients.

## Prerequisites

- Python 3.x.x.
- Cisco Umbrella.
- Email account with rights to send emails from applications (an application password is required).

## Before You Begin

- Create an Umbrella API Key with a at least "read-only" scope to either all Deployments or just the Virtual-Appliances API.
- Create an APP (application) password from your prefered email solution.
- Install Python libraries. For more information, see Requirements.txt.

```bash
pip install -r Requirements.txt
```

- Create the following environment variables (in the PASSWD variable use the APP password created):

```bash
export API_KEY=VALUE
export API_SECRET=VALUE
export EMAIL_ADDRESS=VALUE
export PASSWD=VALUE
```

## Usage

Run the script:

Windows:

```
python ADConnectorMonitor.py
```

Mac:

```
python3 ADConnectorMonitor.py
```
