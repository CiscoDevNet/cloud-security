# Cisco Umbrella Enforcement API Postman Collection

The Cisco Umbrella Enforcement API Postman Collection includes a sample of the Umbrella Enforcement API endpoints. You can import and run the Cisco Umbrella Enforcement API Postman Collection in the Postman REST client. For information about Postman, see [What Is Postman](https://www.postman.com/product/what-is-postman).

## Before You Begin

We recommend that you review the Cisco Cloud Security API documentation. The Cloud Security API documentation describes how to authenticate and authorize requests to the Umbrella Enforcement API. For more information, see [Cisco Cloud Security API](https://developer.cisco.com/docs/cloud-security/).

## Prerequisites

* Download and install [Postman](https://www.getpostman.com/apps).
* Import the [Cisco Umbrella Enforcement Postman Collection JSON file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/legacy/EnforcementAPI/Enforce%20-%20External.postman_collection.json) into your Postman client.

## Set Path Parameters

* The Umbrella Enforcement API `DELETE` endpoint requires the domain ID. Replace the (`EnterYourDomainIdHere`) placeholder value with a domain ID.

## Set Request Body

* The Umbrella Enforcement API `POST` endpoint requires a request body. Set the required event information fields in the request body.

## Run an Umbrella Enforcement API Request

1. Choose the `Enforce - External` collection.
1. Choose an Umbrella Enforcement API endpoint.
1. Update the customer key (`EnterYourCustomerKeyHere`) query parameter with your Umbrella Enforcement API customer key.
1. Click `Send`.
