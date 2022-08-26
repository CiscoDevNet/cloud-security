# Cisco Umbrella Reporting v2 API Postman Collection

The Cisco Umbrella Reporting v2 API Postman Collection includes a sample of the Umbrella Reporting v2 API endpoints. You can import and run the Umbrella Reporting v2 API Postman Collection in the Postman REST client. For information about Postman, see [What Is Postman](https://www.postman.com/product/what-is-postman).

## Before You Begin

We recommend that you review the Cisco Cloud Security API documentation. The Cloud Security API documentation describes how to create your Umbrella Reporting API key, generate a *Bearer* token, and authorize requests to the Umbrella Reporting v2 API. For more information, see [Cisco Umbrella Reporting v2 API Getting Started](https://developer.cisco.com/docs/cloud-security/#!reporting-v2-getting-started).

## Prerequisites

* Download and install [Postman](https://www.getpostman.com/apps).
* Import the [Umbrella Reporting v2 API Postman Environment JSON file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ReportingAPI%20V2/Umbrella%20Reporting%20V2%20-%20External.postman_environment.json) into your Postman client.
* Import the [Umbrella Reporting v2 API Postman Collection JSON file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/ReportingAPI%20V2/Umbrella%20ReportingV2%20-%20External.postman_collection.json) into your Postman client.

## Authentication

In Postman, set up a request to the Umbrella Management API token authorization endpoint and generate a *Bearer* access token.

1. Navigate to your Postman Environments and choose the `Umbrella Reporting V2 - External` environment from the drop-down list.
1. Navigate to your Postman Collections and open the `Umbrella ReportingV2 - External` collection.
1. Choose the `Get Access Token` endpoint under the `1. Auth` folder.
1. Navigate to the `Auth` tab and choose `Basic Auth`.
1. Enter your Umbrella Reporting v2 API key as the `Username` and Umbrella Reporting v2 API secret as the `Password`.
1. Navigate to the `Headers` tab and *deselect* the `Authorization` checkbox.
1. Navigate to the `Body` tab and choose `raw`. Enter `grant_type=Client_credentials`.
1. Click `Send`.

### Set Up Access Token in Postman Environment

1. Navigate to your Postman Environments and open the `Umbrella Reporting V2 - External` environment.
1. Replace the `AccessToken` variable with your generated access token.
1. Click `Save` to apply the changes to the Postman environment.

## Set Path Parameters

* Replace the `EnterYourOrgId` placeholder value with your organization ID.

## Set Query Parameters

* Set the Umbrella Reporting v2 API query parameters to filter or sort the collection.

## Run an Umbrella Reporting v2 API Request

1. Choose the `Umbrella ReportingV2 - External` environment from the drop-down list.
1. Open the `ReportingV2 - External` collection and choose the `Reporting` folder.
1. Choose an Umbrella Reporting v2 API endpoint.
1. Click `Send`.
