# Example of a Splunk AR Alert Action [Lab Grade]

## Introduction
The attached [Adaptive Response Alert Action](http://dev.splunk.com/view/enterprise-security/SP-CAAAFBF) is a Lab Grade example of how you can get additional context for a Cloudlock incident within Splunk®. This example is supplied as a sample only for use with your Cisco Cloudlock subscription under the [Universal Cloud Agreement](http://www.cisco.com/c/dam/en_us/about/doing_business/legal/docs/universal-cloud-agreement.pdf) and [Offer Description](http://www.cisco.com/c/dam/en_us/about/doing_business/legal/docs/omnibus-cloud-security.pdf) respectively (collectively, the “Cisco Agreement”).
However, please note that any samples are not covered by the Cisco Cloudlock product warranty or support and are provided “AS IS”. Variations or changes in scripts can impact the effectiveness of the Alert Action and customers are responsible for updating the sample as needed to meet their use cases. Use of the APIs are subject to the Cloudlock Terms of Service referenced above.

## Alert Action Overview
The Alert Action gets triggered by an alert in Splunk and creats a new event which includes:
* Data from the incident:
  - incident id
  - user
  - origin id
* Event information that is collected from the activity which triggered the incident:
  - event name
  - geolocation data
  - source ip
  
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Splunk/Alert%20Action/UEBA%20Context%20AR.png)
 
## Before Running the Script
* Create an API Token (in Cloudlock open the Integrations tab under the Settings to generate your token - please see the documentation mentioned above for additional instructions).
* Contact support@cloudlock.com to get your API servers address and then replace it in stead of the `YourAPIServersAddress` placeholders below.
* Install the [Cisco Cloudlock Splunk app](https://splunkbase.splunk.com/app/3043/) and configure it (please contact support@cloudlock.com for more info).
* Follow the instructions to create an [Adaptive Response Alert Action](http://dev.splunk.com/view/enterprise-security/SP-CAAAFBF) and only then proceed to add the code by overwriting the default Alert Action in the [Splunk Add-On Builder](https://splunkbase.splunk.com/app/2962/).
* Enter your API servers URL, (`EnterYourAPIServerURLHere`), and API token, (`EnterYourAPITokenHere`), instead of the placeholders.
* To test, create an alert for a Cloudlock incident and in the alert actions select the Alert Action you created in the previous step.


## Troubleshooting
If you encounter difficulties, check the following:
* Before running the Splunk App, check to see that you can you make an API call (Replace "EnterTokenHere" with your API token):
```
curl -k -H "Authorization: Bearer EnterTokenHere" 'https://YourAPIServersAddress/api/v2/incidents'
```

* Whitelist your external IP address/range (Settings -> API and Authentication).
* Do you need to whitelist Cloudlock’s IP Address? As of 6/10/16, the Cloudlock API IPs are: `52.0.185.54`
  `54.236.77.64`.
* Did you create and/or properly copy the token generated in Cloudlock?
* Are you using the correct url (there are a number of these so please contact support@cloudlock.com if you are unsure).
