# General
[Postman is a REST API client](https://www.getpostman.com/) that has many uses however we will focus on using it to make simple API calls.

# Disclaimer
Please see the [official API documentation](https://docs.umbrella.com/investigate-api/docs/introduction-to-cisco-investigate) to learn about:
* [Authentication](https://docs.umbrella.com/investigate-api/docs/about-the-api-authentication) (you will need to create an API token to use these examples).
* Endpoint fields and filters.
* Other endpoints and options (the collection herein contains only a number of examples).

# Prerequisites
* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Environment](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/InvestigateAPI/Investigate%20-%20External.postman_environment.json) and [Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/InvestigateAPI/Investigate%20-%20EXTERNAL.postman_collection.json) json files.
* Open `Manage Environments` (top right cogwheel button) and edit the `Investigate - External` environment. You will need to:
  * Edit the token variable and add your token instead of `Your API Token`.
  * Change the `domain` variable and enter a domain name you'd like to get information on.
  * Edit the `email` variable and change it to an email address you would like to get information for (an email for a domain registrant for example).

# Making an API call:
* Select the `Investigate - External` environment from the drop down list.
* Select the `Investigate - External` collection.
* Choose an API call.
* Hit the `Send` button.
