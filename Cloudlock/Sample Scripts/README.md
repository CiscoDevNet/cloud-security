# Cisco CloudLock Sample Script

## Introduction
The following is a step by step guide to get incidents from Cisco CloudLock via a Python script that makes API calls. This scripts is supplied to customers as a sample which customers are free to use or modify for use with your CloudLock subscription under the [CloudLock Terms of Service](https://www.cloudlock.com/ToS).
However, please note that any samples are not covered by the CloudLock product warranty or support and are provided “AS IS”. Variations or changes in scripts can impact the effectiveness of the script and customers are responsible for updating the samples as needed to meet their use cases. Use of the APIs are subject to the Cloudlock Terms of Service referenced above.

## Script Overview
The scripts function in four steps, as detailed below:
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Sample%20Scripts/sampleScriptDiag.png)

1. The script calls the CloudLock API [instructions on prerequisites and configuration are provided in the official documentation](https://docs.cloudlock.info/docs/introduction-to-api-enterprise)
2. The script gets the API call results
3. The script outputs the incidents/activities to either a file or to syslog (syslog is a way to
send messages to a logging server).
4. The SIEM picks up the incidents/activities from the file

­­­ OR ­­­

1. The syslog sends the incidents/activities to the SIEM
2. The script can be run on demand or via a schedule. With a scheduler, the best practice is to run every 180 seconds.
 
## Before Running the Script
* Create an API Token (in CloudLock open the Integrations tab under the Settings to generate your token - please see the documentation mentioned above for additional instructions).
* Contact support@cloudlock.com to get your API servers address and then replace it in stead of the `YourAPIServersAddress` placeholders below.

## Running the Script (OS X, Linux systems)
Note: Best run under virtualenv

1. The following example is a python script.
2. Download and copy the cl_sample_incidents.py to a server you want to run it on.
3. Make sure that you have Python 2.7.6 installed and then install:
   - ‘requests’: sudo pip install requests
   - ‘configparser’: sudo pip install configparser
   - ‘dateutil’: sudo pip install python-dateutil
4. The output is written to the siem.json file (the last incidents timestamp gets written to cl_polling.ini).
5. Run the script (remember to enter your token and path instead of the placeholders below). For example:

```
python /home/ubuntu/cl_sample_incidents.py -c flat_file -u https://YourAPIServersAddress/api/v2 -t <your token> -p /tmp
```
In the above example the siem.json file gets written to /tmp and the output is written to the screen.

### Optional: 
Schedule the script using crontab, for example you can create a file called
`clToSiem` in /etc/cron.d:

```SHELL=/bin/bash
*/2 * * * * root python /home/ubuntu/cl_sample_incidents.py -c flat_file -u https://YourAPIServersAddress/api/v2 -t <your token> -p /tmp >> /tmp/sim.log 2>&1
```
In the above example the siem.json file and siem.log get written to /tmp. 

Note: You can also send events to a local or remote syslog. To learn more about other output options, run:

```
python /home/ubuntu/pull_incidents.py --help 
```

## Running the Script (Windows systems)
Python 2.7.6 is required to run samplescript.py on Windows server 2012R2. Follow the steps below to run the script.

### Install Python 2.7.6
1. Download Python for Windows from this location: https://www.python.org/download/releases/2.7.6/
2. Download and install https://www.python.org/ftp/python/2.7.6/python-2.7.6.amd64.msi from the page.

### Install Pip
1. Install pip on windows by copying this file to your temp directory: https://bootstrap.pypa.io/get-pip.py
2. Run the program from the command line as an administrator.
3. Use the following command to install the pip file (ignore the warnings during installation):
```
c:\Python27\python.exe <directory where pip file was copied>get-pip.py
```
Pip is installed in the c:\python27\scripts directory. 

### Install required libraries for Samplescript
Run the following commands to install the libraries required for the sample script:

```
c:\python27\scripts\Pip.exe install requests c:\python27\scripts\Pip.exe install configparser c:\python27\scripts\Pip.exe install python-dateutil
```

### Run the sample script
1. Copy the sample script into c:\python27\scripts directory
2. Run the script with the following command:
```
C:\Python27>python.exe c:\Python27\Scripts\cl_sample_incidents.py -c flat_file -u https://YourAPIServersAddress/api/v2 -t <your token> -p c:\tmp
```
The `siem.json` file is created in `c:\tmp`

## Troubleshooting
If you encounter difficulties, check the following:
* Before running the Sample Script, can you make an API call (Replace "EnterTokenHere" with your API token):
```
curl -k -H "Authorization: Bearer EnterTokenHere" 'https://YourAPIServersAddress/api/v2/incidents'
```

* Whitelist your external IP address/range (Settings -> API and Authentication).
* Do you need to whitelist CloudLock’s IP Address? As of 6/10/16, the CloudLock API IPs are: `52.0.185.54`
  `54.236.77.64`
* Did you create and/or properly copy the token generated in CloudLock?
* Are you using the correct url (there are a number of these so please contact support@cloudlock.com if you are unsure).
* If you still have issues, please contact support@cloudlock.com.

Copyright © 2016 CloudLock, Inc. All rights reserved.
