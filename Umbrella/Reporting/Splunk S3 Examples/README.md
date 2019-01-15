# Example of a Splunk Dashboard [Lab Grade]
The following is an example of how you could create a security dashboard within Splunk for Umbrella S3 log data.

## Prerequisits
You first need to setup your Umbrella instance to export logs to S3. These logs can be exported to either [your own S3 bucket](https://support.umbrella.com/hc/en-us/articles/230650987-Configuring-Splunk-with-a-Self-managed-S3-Bucket) or to a [Cisco managed S3 bucket](https://support.umbrella.com/hc/en-us/articles/360001388406-Configuring-Splunk-with-a-Cisco-managed-S3-Bucket).

## Assumptions
1. You have defined a sourcetype for your Umbrella S3 data in Splunk and can search for these events.
2. You have extracted your data fields using a comma delimited extraction and have defined the followiwng as field names:

## Configuration
1. Copy the [attached source file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Reporting/Splunk%20S3%20Examples/umbrella_security.xml) to the `views` folder on your Splunk server. For example: `/opt/splunk/etc/apps/search/local/data/ui/views/`.
2. In the [attached source file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Reporting/Splunk%20S3%20Examples/umbrella_security.xml) replace the `EnterYourSourceTypeHere` placeholder with your defined sourcetype.
3. 
