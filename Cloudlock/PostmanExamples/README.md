# General
Postman is a REST API client that has many uses however we will focus on using it to make simple API calls.

# Disclaimer
Please see the [official API documentation](https://docs.umbrella.com/cloudlock-documentation/docs/introduction-to-api-enterprise) to learn about:
* Authentication (you will need to create an API token to use these examples).
* Pagination.
* Rate Limits.
* Endpoint fields and filters.
* Other endpoints and options (the collection herein contains only a number of examples).

# Prerequisites
* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Environment](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/PostmanExamples/CloudLock%20-%20External.postman_environment.json) and [Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/PostmanExamples/Ent.API%20-%20External.postman_collection.json) json files.
* Open `Manage Environments` (top right cogwheel button) and edit the `Cloudlock - External` environment. You will need to:
  * Change the `server` variable and add your API servers url. Please contact support@cloudlock.com for this address.
  * Edit the token variable and add your token instead of `Your API Token`.

# Making an API call:
* Select the `Cloudlock - External` environment from the drop down list.
* Select the `Ent.API - External` collection.
* Choose an API call.
* If you are making a call to a specific resource (incident/app/etc)... replace the placeholders in the url. For example: `EnterAnAppID` or `EnterIncidentID`.
* Hit the `Send` button.

# Troubleshooting
If you encounter difficulties, check the following:
* See if you can make an API call (Replace "EnterTokenHere" with your API token):
```
curl -k -H "Authorization: Bearer EnterTokenHere" 'https://YourAPIServersAddress/api/v2/incidents'
```

* Whitelist your external IP address/range (Settings -> API and Authentication).
* Do you need to whitelist CloudLock’s IP Address? As of 6/10/16, the CloudLock API IPs are: `52.0.185.54`
  `54.236.77.64`
* Did you create and/or properly copy the token generated in CloudLock?
* Are you using the correct url (there are a number of these so please contact support@cloudlock.com if you are unsure).
* If you still have issues, please contact support@cloudlock.com.
