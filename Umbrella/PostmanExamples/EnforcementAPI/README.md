# General
[Postman is a REST API client](https://www.getpostman.com/) that has many uses however we will focus on using it to make simple API calls.

# Disclaimer
Please see the [official API documentation](https://docs.umbrella.com/enforcement-api/reference/) to learn about:
* [Authentication](https://docs.umbrella.com/enforcement-api/reference/#authentication-and-versioning) (you will need to create a customer key to use these examples).
* Endpoint fields and filters.
* Other endpoints and options (the collection herein contains only a number of examples).

# Prerequisites
* Download and install the [Postman Client](https://www.getpostman.com/apps).
* Import the [Collection](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/PostmanExamples/EnforcementAPI/Enforce%20-%20External.postman_collection.json) json file.

# Making an API call:
* Select the `Enforce - External` collection.
* Choose an API call.
* Update the customer key (`EnterYourCustomerKeyHere`) and if needed, the domain ID, (`EnterYourDomainIdHere` for the DELETE example), and request body (needed for the POST example).
* Hit the `Send` button.
