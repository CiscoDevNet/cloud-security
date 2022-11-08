# Cisco Umbrella Network Tunnels API Postman Collection

The Cisco Umbrella Network Tunnels API Postman Collection includes a sample of the Umbrella Network Tunnels API endpoints. You can import and run the Umbrella Network Tunnels (CDFW) API Postman Collection in the Postman REST client. For information about Postman, see [What Is Postman](https://www.postman.com/product/what-is-postman).

## Before You Begin

We recommend that you review the Cisco Cloud Security API documentation. The Cloud Security API documentation describes how to create your Umbrella Management API key, and authorize requests to the Umbrella Network Tunnels API. For more information, see [Cisco Cloud Security API](https://developer.cisco.com/docs/cloud-security/).

## Prerequisites

* Download and install [Postman](https://www.getpostman.com/apps).
* Import the [Umbrella Network Tunnels API Postman Environment JSON file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/legacy/TunnelAPI/Umbrella%20CDFW%20External.postman_environment.json) into your Postman client.
* Import the [Umbrella Network Tunnels API Postman Collection JSON file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/legacy/TunnelAPI/CDFW%20APIs%20%5BExternal%5D.postman_collection.json) into your Postman client.

## Set Up Postman Environment Variables

1. Navigate to your Postman Environments and choose the `Umbrella CDFW External` environment.
1. Edit the token variable. Update `EnterYourManagementAPIToken` with your Umbrella Management API Base64 encoded key and secret pair.
1. Click `Save` to apply the changes to the Postman environment.

## Set Path Parameters

* Replace the `EnterYourOrgId` placeholder value with your organization ID.
* Replace the `EnterYourTunnelId` placeholder value with a Network Tunnel ID.

## Set Request Body

* The Umbrella Network Tunnels API `POST` (Create Network Tunnel) and (Update or rotate Network Tunnel credentials) endpoints require a request body. Set the required fields in the request body.

## Run an Umbrella Network Tunnels API Request

1. Choose the `Umbrella CDFW External` environment from the drop-down list.
1. Choose the `CDFW APIs - External` collection.
1. Choose an Umbrella Network Tunnels API endpoint.
1. Click `Send`.
