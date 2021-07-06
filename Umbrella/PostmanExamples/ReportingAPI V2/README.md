# General
[Postman is a REST API client](https://www.getpostman.com/) that has many uses however we will focus on using it to make simple API calls.

# Disclaimer
Please see the [official API documentation](https://docs.umbrella.com/umbrella-api/docs/overview) to learn about:
* [Authentication](https://docs.umbrella.com/umbrella-api/docs/authentication-and-errors) (you will need to create an API token to use these examples).
* Endpoint fields and filters.
* Other endpoints and options (the collection herein contains only a number of examples).

# Prerequisites
* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Environment](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ReportingAPI%20V2/Umbrella%20Reporting%20V2%20-%20External.postman_environment.json) and [Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ReportingAPI%20V2/Umbrella%20ReportingV2%20-%20External.postman_collection.json) json files.

# Authentication
* Open `Manage Environments` (top right cogwheel button) and edit the `Umbrella Reporting V2 - External` environment. You will need to:
  * Get your API Access Token by making a call to the `oauth2/token` endpoint. To do this:
    * First generate your key:secret using the [following instructions](https://docs.umbrella.com/umbrella-api/docs/authentication-and-errors#section-authentication-and-key-management-for-umbrella-ap-is ).
    * Select the `Umbrella ReportingV2 - External` collection and select the `Get Access Token` under the `1. Auth` folder.
    * In the `Authorization` tab, select `Basic Auth` and enter the `API Key`as the `Username` and `API Secret` as the `Password`.
    * In the `Headers` tab, *De-Select* the `Authorization` checkbox.
    * In the `Body` tab, select `RAW` and enter the following string:
        * `grant_type=Client_credentials`
    * Hit the `Send` button.
    * This should return the `Bearer Access Token`


  * Now you can return to `Manage Environments`, edit the `Umbrella Reporting V2 - External` environment again and replace the `AccessToken` variable with your access token.
  * Please also change the `org_id` variables value (`EnterYourOrgID`) to your org's ID.
  * Click `Save` for it to apply.

# Making an API call:
* Open the `ReportingV2 - External` collection and select the `Reporting` folder.
* Choose an API call.
* Replace the placeholders such as `EnterTheFromDateInEpochMs` with values.
* Hit the `Send` button.
