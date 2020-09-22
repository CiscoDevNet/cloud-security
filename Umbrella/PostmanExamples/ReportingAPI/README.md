# General
[Postman is a REST API client](https://www.getpostman.com/) that has many uses however we will focus on using it to make simple API calls.

# Disclaimer
Please see the [official API documentation](https://docs.umbrella.com/umbrella-api/docs/overview) to learn about:
* [Authentication](https://docs.umbrella.com/umbrella-api/docs/authentication-and-errors) (you will need to create an API token to use these examples).
* [Endpoint options, fields and filters](https://docs.umbrella.com/umbrella-api/reference#organization-tunnel).
* Other endpoints and options (the collection herein contains only a number of examples).

# Prerequisites
* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Environment](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ReportingAPI/Umbrella%20Reporting%20-%20External.postman_environment.json) and [Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ReportingAPI/Umbrella%20Reporting%20-%20External.postman_collection.json) json files.
* Open `Manage Environments` (top right cogwheel button) and edit the `Umbrella Reporting - External` environment. You will need to:
  * Edit the token variable and add your token instead of `EnterYourManagementAPIToken`.

# Making an API call:
* Select the `Umbrella Reporting - External` environment from the drop down list.
* Open the relevant folder.
* Choose an API call.
* Hit the `Send` button.
