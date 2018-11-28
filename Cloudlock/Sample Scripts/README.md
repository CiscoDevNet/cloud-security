# CloudLock® Sample Script Guide

## Introduction
The following is a step by step guide to get incidents or activities from the CloudLock®​ ​Security FabricTM via a Python script. CloudLock scripts are supplied to customers as samples which customers are free to use or modify for use with your CloudLock subscription under the [CloudLock Terms of Service](https://www.cloudlock.com/ToS).
However, please note that these samples are not covered by the CloudLock product warranty or support and are provided “AS IS”. Variations or changes in scripts can impact the effectiveness of the script and customers are responsible for updating the samples as needed to meet their use cases. Use of the APIs are subject to the Cloudlock Terms of Service referenced above.

## Script Overview
There are four sample scripts:
* Incidents, for use with any domain
* Activities, for use with any domain
* Incidents, for use with .gov domains
* Activities, for use with .gov domains

The scripts function in four steps, as detailed below:
1. The script calls the CloudLock API’s [instructions on prerequisites and configuration are provided in the official documentation](https://docs.cloudlock.info/docs/introduction-to-api-enterprise)
2. The script gets the API call results
3. The script outputs the incidents/activities to either a file or to syslog (syslog is a way to
send messages to a logging server).
4. The SIEM picks up the incidents/activities from the file
­­­ OR ­­­
The syslog sends the incidents/activities to the SIEM
The script can be run on­demand or via a schedule. With a scheduler, the best practice is to run every 180 seconds.
 
## Before Running the Script
Create an API Token (in CloudLock open the Integrations tab under the Settings to generate your token):

### Running the Script (OS X, Linux systems)
Note: Best run under virtualenv

1. The following example is a python script.
2. Download and copy the cl_sample_incidents.py to a server you want to run it on.
3. Make sure that you have Python 2.7.6 installed and then install:

* ‘requests’: sudo pip install requests
* ‘configparser’: sudo pip install configparser
* ‘dateutil’: sudo pip install python-dateutil

4. The output is written to the siem.json file (the last incident gets written to cl_polling.ini).
5. You have two options in running the script (remember to enter your token and path instead of the placeholders below):
a. Schedule the script using crontab, for example you can create a file called
clToSiem in /etc/cron.d:
In the above example the siem.json file and siem.log get written to /tmp.

```SHELL=/bin/bash
*/2 * * * * root python /home/ubuntu/cl_sample_incidents.py -c flat_file -u https://api.cloudlock.com/api/v2 -t <your token> -p /tmp >> /tmp/sim.log 2>&1
```

 b. Set a polling interval, (in seconds), as an argument (the ‘-i’ argument). For example:
```python /home/ubuntu/cl_sample_incidents.py -c flat_file -u https://api.cloudlock.com/api/v2 -t <your token> -p /tmp -i 120
```
 
In the above example the siem.json​ file gets written to /tmp and the output is
written to the screen.

Note: You can also send events to a local or remote syslog. To learn more about other
output options, run:

### Running the Script (Windows systems)
Python 2.7.6 is required to run samplescript.py on Windows server 2012R2. Follow the steps below to run the script.

#### Install Python 2.7.6
1. Download Python for Windows from this location: https://www.python.org/download/releases/2.7.6/
2. Download and install https://www.python.org/ftp/python/2.7.6/python-2.7.6.amd64.msi from the page.

#### Install Pip
1. Install pip on windows by copying this file to your temp directory: https://bootstrap.pypa.io/get-pip.py
2. Run the program from the command line as an administrator.
3. Use the following command to install the pip file (ignore the warnings during installation):
```
c:\Python27\python.exe <directory where pip file was copied>get-pip.py
```
Pip is installed in the c:\python27\scripts directory. 

#### Install required libraries for Samplescript
Run the following commands to install the libraries required for the sample script:
```
c:\python27\scripts\Pip.exe install requests c:\python27\scripts\Pip.exe install configparser c:\python27\scripts\Pip.exe install python-dateutil
python /home/ubuntu/cl_sample_incidents.py -c flat_file -u https://api.cloudlock.com/api/v2 -t <your token> -p /tmp -i 120
python /home/ubuntu/pull_incidents.py --help
```

Run the sample script
Copy the sample script into ​c:\python27\scripts directory
Run the script with the following command:
C:\Python27>python.exe c:\Python27\Scripts\cl_sample_incidents.py ­c flat_file ­u ​https://api.cloudlock.com/api/v2​ ­t <your token> ­p c:\tmp
The siem.json file is created in ​c:\tmp T roubleshooting
If you encounter difficulties, check the following:
● Before running the Sample Script, can you make an API call?
Replace "EnterTokenHere" with your API token:
curl ­k ­H "Authorization: Bearer EnterTokenHere"
'https://api­platform.cloudlock.com/api/v2/incidents'
● Has your IP address been whitelisted by CloudLock?
If not, contact support@cloudlock.com with the IP address/es or range that needs to be whitelisted.
Note: to check your IP address, run the following on the servers making the API calls: curl ­s checkip.dyndns.org | sed ­e 's/.*Current IP Address: //' ­e 's/<.*$//'
● Do you need to whitelist CloudLock’s IP Address? As of 6/10/16, the CloudLock API IPs are: 52.0.185.54
54.236.77.64
● Did you create and/or properly copy the token generated in CloudLock?
● Are you using the CloudLock .gov domain? If so your script must point to:
https://api­platformusgov.cloudlock.com/api/v2
Change History
Most recent updates to the sample scripts:
1. Page based on the updated_after filter (instead of the created_after).
2. Fix for rate limit recovery issue (delay before re­polling).
3. Fixes to LEEF output (devTimeFormat, EventID, and formatting issues).
4. Fixed: certain entity null values could cause abnormal behavior of the script.
5. Syslog fix: when dealing with a large number of matches, the script could terminate
when exceeding the maximum syslog capacity. The solution: When you have over 100
 Copyright © 2016 CloudLock, Inc. All rights reserved.

matches, show the first 100 and then add a field to indicate that there were additional
matches.
6. Activities scripts only: The offset for the API was not applied, which caused duplicate
calls.
7. Activities scripts only: A one hour delay has been introduced to deal with platform
specific limitations (events do not come in chronologically from the various platforms).
Notes
● It is possible to receive duplicate events when using the script; keep this in mind and de­duplicate.
 Copyright © 2016 CloudLock, Inc. All rights reserved.
