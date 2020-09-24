# General
[Postman is a REST API client](https://www.getpostman.com/) that has many uses however we will focus on using it to make simple API calls.

# Disclaimer
Please see the [official API documentation](https://docs.umbrella.com/umbrella-api/reference) to learn about:
* [Authentication](https://docs.umbrella.com/umbrella-api/reference#rateauthentication-and-key-management-for-the-umbrella-api) (you will need to create an Umbrella Management API token to use these examples).
* [Endpoint options, fields and filters](https://docs.umbrella.com/umbrella-api/reference#organization-tunnel).
* Other endpoints and options (the collection herein contains only a number of examples).

# Prerequisites
* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Environment](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/TunnelAPI/Umbrella%20CDFW%20External.postman_environment.json) and [Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/TunnelAPI/CDFW%20APIs%20%5BExternal%5D.postman_collection.json) json files.
* Open `Manage Environments` (top right cogwheel button) and edit the `Umbrella CDFW External` environment. You will need to:
  * Edit the token variable and add your token instead of `EnterYourManagementAPIToken`.

# Making an API call:
* Select the `Umbrella CDFW External` environment from the drop down list.
* Select the `CDFW APIs - External` collection.
* Open the desired folder/s.
* Replace the `EnterYourOrgId`, (and if needed the `EnterYourTunnelId`), placeholder/s with your environment details. If you want to create a tunnel or update/rotate credentials, replace the placeholders in the `body` content.
* Choose an API call.
* Hit the `Send` button.
