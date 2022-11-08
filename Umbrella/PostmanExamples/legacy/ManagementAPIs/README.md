# Cisco Umbrella Management API Postman Collection

The Cisco Umbrella Management API Postman Collection includes a sample of the Umbrella Management API endpoints. You can import and run the Umbrella Management API Postman Collection in the Postman REST client. For information about Postman, see [What Is Postman](https://www.postman.com/product/what-is-postman).

## Before You Begin

We recommend that you review the Cisco Cloud Security API documentation. The Cloud Security API documentation describes how to create your Umbrella Management API key, and authorize requests to the Umbrella Management API. For more information, see [Cisco Cloud Security API](https://developer.cisco.com/docs/cloud-security/).

## Prerequisites

* Download and install [Postman](https://www.getpostman.com/apps).
* Import the [Umbrella Management API Postman Environment JSON file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/legacy/ManagementAPIs/Umbrella%20Management%20API%20-%20External.postman_environment.json) into your Postman client.
* Import the [Umbrella Managemene API Postman Collection JSON file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/legacy/ManagementAPIs/Umbrella%20Management%20APIs%20-%20External.postman_collection.json) into your Postman client.

## Set Up Postman Environment Variables

1. Navigate to your Postman Environments and choose the `Umbrella Management API - External` environment.
1. Update `YourAPIToken` with your Umbrella Management API Base64 encoded key and secret pair.
1. Click `Save` to apply the changes to the Postman environment.

## Set Path Parameters

The Umbrella Management API endpoints require that you set various path parameters.

* Replace the `EnterYourOrgId` placeholder value with your organization ID.
* Replace the `EnterYourCustomerID` placeholder value with your customer ID.
* Replace the `EnterYourDestListID` placeholder value with your Destination List ID.
* Replace the `EnterYourUserID` placeholder value with your User ID.

## Set Request Body

* The Umbrella Management API `POST` endpoints require a request body. Set the required fields in the request body.

## Run an Umbrella Management API Request

1. Choose the `Umbrella Management API - External` environment from the drop-down list.
1. Choose the `Umbrella Management API - External` collection.
1. Choose an Umbrella Management API endpoint.
1. Click `Send`.
