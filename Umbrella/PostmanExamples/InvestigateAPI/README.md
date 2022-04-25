# Cisco Umbrella Investigate API Postman Collection

The Cisco Umbrella Investigate API Postman Collection includes a sample of the Umbrella Investigate API endpoints. You can import and run the Umbrella Investigate API Postman Collection in the Postman REST client. For information about Postman, see [What Is Postman](https://www.postman.com/product/what-is-postman).

## Before You Begin

We recommend that you review the Cisco Cloud Security API documentation. The Cloud Security API documentation describes how to create your Umbrella Investigate API *Bearer* access token and authorize requests to the Umbrella Investigate API. For more information, see [Cisco Umbrella Investigate API Overview](https://developer.cisco.com/docs/cloud-security/#!investigate-introduction-overview).

## Prerequisites

* Download and install [Postman](https://www.getpostman.com/apps).
* Import the [Umbrella Investigate API Postman Environment JSON file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/InvestigateAPI/Investigate%20-%20External.postman_environment.json) into your Postman client.
* Import the [Umbrella Investigate API Postman Collection JSON file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/InvestigateAPI/Investigate%20-%20EXTERNAL.postman_collection.json) into your Postman client.

## Set Up Postman Environment Variables

1. Navigate to your Postman Environments and choose the `Investigate - External` environment.
1. Update the `Your API Token` with your Umbrella Investigate API *Bearer* access token.
1. Edit the `domain` variable and enter a domain name that you seek information about.
1. Edit the `email` variable and change it to an email address you seek information about (an email address for a domain registrant).
1. Click `Save` to apply the changes to the Postman environment.

## Run an Umbrella Investigate API Request

1. Choose the `Investigate - External` environment from the drop-down list.
1. Choose the `Investigate - External` collection.
1. Choose an Umbrella Investigate API endpoint.
1. Click `Send`.
