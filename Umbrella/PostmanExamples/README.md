# Umbrella Postman Collection

[Postman is a REST API client](https://www.getpostman.com/) that you can use to make requests to API endpoints.

## Disclaimer

* The Umbrella APIs require authentication and authorization of all endpoints.
* The `Umbrella NextGen APIs -External` Postman collection and environment are provided only as examples.

## Prerequisites

* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Umbrella Postman Environment](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/umbrella-external-postman-environment.json) JSON file. You may need to copy the contents of this file to a local json file before you import.
* Import the [Umbrella Postman Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/umbrella-external-postman-collection.json) JSON file. You may need to copy the contents of this file to a local json file before you import.
* Select the `Umbrella NextGen APIs - External` collection.
* Select the `Umbrella NextGen API - External` environment from the drop down list.
* Locate the `Auth` folder in the Postman collection.
* Click on the `Get Access Token` endpoint. Under Authorization, click on `Type` and select `Basic Auth` ![image](https://user-images.githubusercontent.com/11685750/163167297-d3ea0103-3711-42c8-81e9-2374f093584e.png)
* Enter your API key and API secret in the `Username` and `Password` fields respectively:
![image](https://user-images.githubusercontent.com/11685750/163173840-a9c399ae-929f-4891-b298-b9321a12f023.png)
* Now generate an API access token:
  1. Hit `Send` to generate an Umbrella API access token.
  1. Add your new access token token to the `AccessToken` variable in the `Umbrella NextGen APIs - External` Postman environment.

**Note:** Cloud Security API access tokens are valid for up to one hour. Once a token expires, you can go back an generate a new access token and plug it into the environment as demonstrated above.

## Send an API call

* Choose an API call.
* Hit the `Send` button.
