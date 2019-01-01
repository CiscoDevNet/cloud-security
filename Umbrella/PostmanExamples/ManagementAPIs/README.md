# General
Postman is a REST API client that has many uses however we will focus on using it to make simple API calls.

# Disclaimer
Please see the [official API documentation](https://docs.umbrella.com/umbrella-api/reference) to learn about:
* [Authentication](https://docs.umbrella.com/umbrella-api/reference#rateauthentication-and-key-management-for-the-umbrella-api) (you will need to create an API token to use these examples).
* Endpoint fields and filters.
* Other endpoints and options (the collection herein contains only a number of examples).

# Prerequisites
* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Environment](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ManagementAPIs/Umbrella%20Management%20API%20-%20External.postman_environment.json) and [Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ManagementAPIs/Umbrella%20Management%20APIs%20-%20External.postman_collection.json) json files.
* Open `Manage Environments` (top right cogwheel button) and edit the `Umbrella Management API - External` environment. You will need to:
  * Edit the token variable and add your token instead of `Your API Token`.

# Making an API call:
* Select the `Umbrella Management API - External` environment from the drop down list.
* Select the `Umbrella Management APIs - External` collection.
* Replace the `EnterYourOrgID`, (and if needed the `EnterYourCustomerID`), placeholder/s with your orgs details. If you want to create a customer, replace the placeholders in the `body` content.
* Choose an API call.
* Hit the `Send` button.
