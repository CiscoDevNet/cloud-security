A simple sync tool to bring Security Group Tags from ISE to Secure Access.

## Usage
main.py [-h] [--list-ise | --list-sa | --list-sa-inactive | --diff-only]

options:
  -h, --help          show this help message and exit
  --list-ise          List all Security Group Tags found in Cisco Identity Services Engine (ISE).
  --list-sa           List all Security Group Tags found in Cisco Secure Access (active and inactive).
  --list-sa-inactive  List only the INACTIVE Security Group Tags found in Cisco Secure Access.
  --diff-only         Show the difference between ISE and Secure Access SGTs without performing any synchronization (no changes applied).

## Environmental Variables
| Variable | Comment |
|----------------|-------------------------|
ISE-SERVER       | IP address or FQDN
ISE-USER         | ISE ERS Admin Username
ISE-PASS         | ISE ERS Admin Password
SA-KEY           | Secure Access API Key
SA-SECRET        | Secure Access API Secret

