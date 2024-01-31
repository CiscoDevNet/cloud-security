# Cisco Secure Access Postman Collection

[Postman is a REST API client](https://www.getpostman.com/) that you can use to make requests to API endpoints.

## Disclaimer

* The Cisco Secure Access APIs require authentication and authorization of all endpoints.
* The `Cisco Secure Access APIs` Postman collection and environment are provided only as examples.

## Prerequisites

* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Cisco Secure Access Postman Environment](https://github.com/CiscoDevNet/cloud-security/blob/master/Cisco%20Secure%20Access/PostmanExamples/Cisco%20Secure%20Access.postman_environment.json) JSON file. Copy the Cisco Secure Access Postman environment file to your local system.
* Import the [Cisco Secure Access Postman Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Cisco%20Secure%20Access/PostmanExamples/Cisco%20Secure%20Access.postman_collection.json) JSON file. Copy the Cisco Secure Access Postman collection file to your local system.
* Select the `Cisco Secure Access` collection.
* Select the `Cisco Secure Access` environment from the environment drop down list.
* Locate the `1. Auth - Start Here` folder in the Postman collection.
* Click on the `Get Access Token` endpoint. Under Authorization, click on `Type` and select `Basic Auth` ![image](https://user-images.githubusercontent.com/11685750/163167297-d3ea0103-3711-42c8-81e9-2374f093584e.png)
* Enter your API key and API secret in the `Username` and `Password` fields respectively:
![image](https://user-images.githubusercontent.com/11685750/163173840-a9c399ae-929f-4891-b298-b9321a12f023.png)
* Now generate an API access token:
  1. Hit `Send` to generate a Cisco Secure Access API access token.
  1. Add your new access token token to the `AccessToken` variable in the `Cisco Secure Access` Postman environment.

**Note:** Cloud Security API access tokens are valid for up to one hour. Once a token expires, you can go back an generate a new access token and plug it into the environment as demonstrated above.

## Send an API call

* Choose an API call.
* Hit the `Send` button.
