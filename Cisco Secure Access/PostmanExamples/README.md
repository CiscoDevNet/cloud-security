# Cisco Secure Access API Collections

Explore Cisco Secure Access APIs with organized request examples and sample payloads. The same collection and environment JSON files work with compatible API clients. Choose your preferred client; no client-specific version of these examples is required.

## Disclaimer

- These collections and environments are provided as examples, not a production SDK.
- API access requires authentication, authorization and the appropriate scopes.
- Some requests create, update or delete tenant configuration. Review each request and run it individually; do not run an entire collection against a live tenant.
- Payloads contain illustrative values. Replace IDs, addresses and other organization-specific data before sending a request.

## Prerequisites

- An API client that supports importing Collection v2.1 JSON and environment JSON files.
- An active Cisco Secure Access tenant in the deployment you want to use.
- An API key and API secret for that deployment, with the scopes needed for your requests.

## Choose Your Deployment

Download a **matching collection and environment** from the same row. Every deployment uses the same import workflow. Do not mix credentials or environment files between deployments.

| Deployment | API base URL | Collection | Environment |
| --- | --- | --- | --- |
| Commercial | `https://api.sse.cisco.com/` | [Download collection](collections/Cisco%20Secure%20Access%20API%20Collections%20-%20Commercial.collection.json) | [Download environment](environments/Cisco%20Secure%20Access%20API%20Collections%20-%20Commercial.environment.json) |
| Government | `https://api.secureaccessfed.cisco/` | [Download collection](collections/Cisco%20Secure%20Access%20API%20Collections%20-%20Government.collection.json) | [Download environment](environments/Cisco%20Secure%20Access%20API%20Collections%20-%20Government.environment.json) |
| China | `https://api.ciscosecureaccess.cn/` | [Download collection](collections/Cisco%20Secure%20Access%20API%20Collections%20-%20China.collection.json) | [Download environment](environments/Cisco%20Secure%20Access%20API%20Collections%20-%20China.environment.json) |
| Australia | `https://api.au.sse.cisco.com/` | [Download collection](collections/Cisco%20Secure%20Access%20API%20Collections%20-%20Australia.collection.json) | [Download environment](environments/Cisco%20Secure%20Access%20API%20Collections%20-%20Australia.environment.json) |
| United Kingdom | `https://api.uk.sse.cisco.com/` | [Download collection](collections/Cisco%20Secure%20Access%20API%20Collections%20-%20United%20Kingdom.collection.json) | [Download environment](environments/Cisco%20Secure%20Access%20API%20Collections%20-%20United%20Kingdom.environment.json) |

Request availability depends on your deployment, tenant features and permissions. Government and China use their respective API definitions; some preserved folders may be empty where an API is not documented for that deployment.

## Import The Examples

1. Open your API client's import action and import the collection JSON for your deployment.
2. Import the matching environment JSON using the client's environment import action.
3. Select the imported collection and environment.
4. Set `APIKey` and `APISecret` in your local environment. Keep these values private; do not include them in exported files, source control or shared screenshots.

The files are shared JSON imports, not a client-native collection directory to open. Your client may convert the collection to its own internal format during import. The request hierarchy and examples remain available after import.

## Get An Access Token

1. Open **1. Auth - Start Here / Get Access Token**.
2. Confirm that the request uses `POST {{server}}auth/v2/token` and Basic Auth with `{{APIKey}}` and `{{APISecret}}`.
3. Leave the form body as `grant_type=client_credentials`, then send the request.
4. The included response script saves the returned `access_token` in the selected environment's `AccessToken` variable. If your client does not execute or translate response scripts, copy the returned token into `AccessToken` manually.

Tokens expire. When a token expires, send **Get Access Token** again to renew it. Use the token's `expires_in` value to check its lifetime.

## Send An API Request

1. Choose a request under **Deployments**, **Admin**, **Policies**, **Reports** or **Investigate**, as available for your deployment.
2. Review the request description, required scopes, path values, query parameters and example body. Additional named payload examples are included in request descriptions when documented.
3. Replace sample values with values for your organization. Enable optional query parameters only when needed. For upload requests, select your local file.
4. Send the individual request and inspect its response.

Requests use `{{server}}` for the base URL and `Bearer {{AccessToken}}` for authorization. The token request uses Basic Auth instead. Selecting the matching environment supplies the correct regional host without editing request URLs.

| Environment variable | Purpose |
| --- | --- |
| `server` | API base URL for the selected deployment, including a trailing `/`. |
| `Authurl` | Full token endpoint URL, supplied for compatibility with existing workflows. |
| `APIKey` | Your deployment-specific API key. Set locally. |
| `APISecret` | Your deployment-specific API secret. Set locally and keep private. |
| `AccessToken` | Current access token used by authenticated requests. |

## About The Examples

Requests are organized into API groups and family subfolders. Example payloads come from the API documentation's YAML/JSON definitions. A schema-derived sample is identified when a complete example is not provided. Examples still require review and tenant-specific values; their presence does not grant access to an API or make a request safe to execute unchanged.

Some preserved legacy requests may no longer appear in the current API reference. Check the relevant documentation before using an older example. DLP event APIs may also require a storage-region path such as `reports.us` or `reports.eu`, independently of the selected deployment host.

## API Documentation

- [Commercial API reference](https://developer.cisco.com/docs/cloud-security/secure-access-api-reference-overview/), also used for Australia and United Kingdom examples.
- [Government API reference](https://developer.cisco.com/docs/cloud-security-gov/secure-access-api-reference-overview/).
- [China API reference](https://developer.cisco.com/docs/secure-access-china/api-reference-overview/).

## Collection Format And License

The files use the **Postman Collection Format v2.1** JSON structure. The format and its schemas are published by Postman; they are not a Cisco-authored specification. The [upstream schema repository](https://github.com/postmanlabs/schemas) distributes its schemas under the [Apache License, Version 2.0](https://github.com/postmanlabs/schemas/blob/develop/LICENSE.md), with the copyright notice:

> Copyright 2015 Postdot Technologies Pvt. Ltd.

That attribution and license concern the upstream schema, separately from the Cisco API request examples and their applicable license. Naming the format identifies its origin and does not imply affiliation with or endorsement by Postman.
