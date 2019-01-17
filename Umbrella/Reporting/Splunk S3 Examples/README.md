# Example of a Splunk Dashboard [Lab Grade]
The following is an example of how you could create a dashboard within Splunk for Umbrella S3 log data. This is more of a descriptive example than a guide and your environment could be significantly different and require a different configuration (for example the fields mentioned in the `Assumptions` sections could be completely different):
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Reporting/Splunk%20S3%20Examples/UmbrellaS3SplunkSec.png)

## Prerequisits
You first need to setup your Umbrella instance to export logs to S3. These logs can be exported to either [your own S3 bucket](https://support.umbrella.com/hc/en-us/articles/230650987-Configuring-Splunk-with-a-Self-managed-S3-Bucket) or to a [Cisco managed S3 bucket](https://support.umbrella.com/hc/en-us/articles/360001388406-Configuring-Splunk-with-a-Cisco-managed-S3-Bucket).

## Assumptions
1. You have defined a sourcetype for your Umbrella S3 data in Splunk and can search for these events.
2. You have extracted your data fields using a comma delimited extraction and have defined the followiwng as field names (note that these can change and depend on the [log format version](https://support.umbrella.com/hc/en-us/articles/231248508-Log-Export-Format-and-Versioning)):
  - status (for example: `Allowed`/`Blocked`)
  - eventtype (for example: `Malware`/`C2`)
  - security_category (for example: `Malware,Computer Security`/`Malware,Illegal Downloads`)
  - user (the identity, for example: `billyfuentesWa7`/`NYC Office`)

## Configuration
1. Copy the [attached source file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Reporting/Splunk%20S3%20Examples/umbrella_security.xml) to the `views` folder on your Splunk server. For example: `/opt/splunk/etc/apps/search/local/data/ui/views/` (if you want this dashboard in the `search` app).
2. In the [attached source file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Reporting/Splunk%20S3%20Examples/umbrella_security.xml) replace the `EnterYourSourceTypeHere` placeholder with your defined sourcetype.
3. If needed, change the field names mentioned in the `Assumptions` section based on your environment.
4. Open the app and goto the dashboards view to see the new dashboard (for example: `https://YourServerName:yourPort/en-US/app/search/dashboards`) and then select the dashboard.
5. If you don't see data in the panels, you most likely need to change the queries in the xml (either the `field names`, the `sourcetype`/`index` or `value`).
