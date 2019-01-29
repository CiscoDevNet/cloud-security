# Important Note
Please note that the Cisco Cloud Security App for IBM Qradar is in a beta phase and is provided to early adopters only at this phase. Please note that the Cisco Cloud Security App for IBM Qradar is not covered by the general product warranty. Variations or changes made to the App can impact the effectiveness of the App. A separate email will be sent shortly with the password for the resources specified in the links below.


# Preparations and Prerequisites
Please first review 1.4. Prerequisites in the [product guide](https://github.com/CiscoDevNet/cloud-security/blob/master/Cisco%20Cloud%20Security/IBM%20Qradar/Cisco%20Umbrella%20App%20Product%20Guide_Beta_V_0.4.pdf).
 
The Cisco Cloud Security App for IBM Qradar includes four different modules that represent four of the Cisco Cloud Security products. You do not have to have all four products and can use different combinations of them, but please first make sure that you have the necessary perquisites for the products you do have, as you will need these when installing the app:
 
## For Cisco Umbrella
[Umbrella s3 Log Management](https://support.umbrella.com/hc/en-us/articles/231248448-Cisco-Umbrella-Log-Management-in-Amazon-S3)
 
## For Cisco Umbrella Enforcement API
[Enforcement API](https://docs.umbrella.com/enforcement-api/reference/)
 
## For Cisco Investigate API
[Investigate API](https://docs.umbrella.com/investigate-api/docs)
 
## For Cisco Cloudlock API
Please see the [authentication section](https://docs.cloudlock.info/docs/introduction-to-api-enterprise) for instructions on how to generate your API token.
Also - in order for the Cisco Cloud Security App for IBM Qradar to access Cisco Cloudlock's API, we will need to whitelist your Qradars servers external IP address/es or range (if this has not already been done). You can whitelist these within the Cisco Cloudlock User Interface under the Authentication & API tab in the Settings page (which is also where you will generate your API token).
 
# Installation Instructions
To install the app:
1. Please [download the app](https://github.com/CiscoDevNet/cloud-security/blob/master/Cisco%20Cloud%20Security/IBM%20Qradar/Cisco%20Cloud%20Security_V1.0.0%20Beta.zip)
2. Please [download the supporting dsms](https://github.com/CiscoDevNet/cloud-security/blob/master/Cisco%20Cloud%20Security/IBM%20Qradar/aws_protocol_jar_Beta.zip)
3. Please [download the product guide](https://github.com/CiscoDevNet/cloud-security/blob/master/Cisco%20Cloud%20Security/IBM%20Qradar/Cisco%20Umbrella%20App%20Product%20Guide_Beta_V_0.4.pdf) and follow the install and usage instructions
