# General
[Postman is a REST API client](https://www.getpostman.com/) that has many uses however we will focus on using it to make simple API calls.

# Disclaimer
Please see the [official API documentation](https://docs.umbrella.com/umbrella-api/docs/overview) to learn about:
* [Authentication](https://docs.umbrella.com/umbrella-api/docs/authentication-and-errors) (you will need to create an API token to use these examples).
* Endpoint fields and filters.
* Other endpoints and options (the collection herein contains only a number of examples).

# Prerequisites
* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Environment](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ReportingAPI/Umbrella%20Reporting%20-%20External.postman_environment.json) and [Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ReportingAPI/Umbrella%20Reporting%20-%20External.postman_collection.json) json files.
* Open `Manage Environments` (top right cogwheel button) and edit the `Umbrella Reporting - External` environment. You will need to:
  * Change the `url` variable and add your org ID instead of `OrgId`.
  * Edit the token variable and add your token instead of `Your API Token`.
  * Edit the `domainName` variable and change `domainname.com` to the domain name you would like to get information for.

# Making an API call:
* Select the `Umbrella Reporting - External` environment from the drop down list.
* Open the `Reporting` folder.
* Choose an API call.
* Hit the `Send` button.
