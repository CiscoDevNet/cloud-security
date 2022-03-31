# PHP Client Example for Umbrella API OAuth2.0 Authorization

The PHP example client application shows how to create an Umbrella Reporting v2 API request protected by the OAuth2.0 authorization framework.

## Overview

To get started, set up the required environment variables:

* `API_KEY`: Umbrella API Reporting v2 key
* `API_SECRET`: Umbrella API Reporting v2 secret
* `ORG_ID`: Umbrella organization ID

### Download and Install

To create and send HTTP requests, download and install:

* `Composer`: Composer is a dependency management tool for PHP. For more information, see [Composer](https://getcomposer.org/doc/00-intro.md).
* `Guzzle`: Guzzle is a PHP HTTP client. You can install Guzzle with Composer. For more information, see [Guzzle](https://docs.guzzlephp.org/en/stable/).
* `PHP`: You must have PHP version 5.3.2 or later to run Composer. For more information, see [Install and Configure PHP](https://www.php.net/manual/en/install.php).

**Note:** We recommend that you install PHP version 7.4.3 or higher.

To install Guzzle with Compose (`compose.phar`), you can use the example `composer.json` file. Alternatively, update your project's `composer.json` file with the required libraries.

```json
{
        "require": {
            "kamermans/guzzle-oauth2-subscriber": "~1.0",
            "guzzlehttp/guzzle": "^7.0"
        }
}
```

Compose reads the `compose.json` file and installs the required libraries. To install Guzzle, run:

```shell
php composer.phar install
```

### Initialize HTTP Client

The example client application initializes an HTTP client with the client credentials and sets up the OAuth 2.0 middleware with the client credentials token flow:

* Create Guzzle HTTP client and initialize the `base_uri` for the authorization service.
* Create Client credentials object with the Umbrella API key and secret.
* Initialize OAuth 2.0 middleware.

For example:

```php
// Authorization client - this is used to request OAuth access tokens
$reauth_client = new GuzzleHttp\Client([
    // URL for access_token request
    'base_uri' => 'http://some_host/access_token_request_url',
]);
$reauth_config = [
    "client_id" => $client_id,
    "client_secret" => $client_secret,
    //"scope" => "your scope(s)", // optional
];
$grant_type = new ClientCredentials($reauth_client, $reauth_config);
// This grant type is used to get a new Access Token and Refresh Token when
//  only a valid Refresh Token is available
$refresh_grant_type = new RefreshToken($reauth_client, $reauth_config);

// Tell the middleware to use the two grant types
$oauth = new OAuth2Middleware($grant_type, $refresh_grant_type);

$stack = HandlerStack::create();
$stack->push($oauth);
```

### Run the Guzzle Client

1. Set the Umbrella Reporting v2 API key, Umbrella Reporting v2 API secret, and Umbrella organization ID as environment variables.

   ```shell
   export API_KEY=<...>
   export API_SECRET=<...>
   export ORG_ID=<...>
   ```

1. Initialize the Guzzle HTTP client and OAuth 2.0 middleware. Create a request to the Umbrella Reporting v2 API.

   ```php
   // This is the normal Guzzle client that you use in your application
   $client = new GuzzleHttp\Client([
    'handler' => $stack,
    'auth'    => 'oauth',
   ]);

   $response = $client->get("https://reports.api.umbrella.com/v2/organizations/$org_id/summary?from=-5days&to=now");

   echo "Status: ".$response->getStatusCode()."\n";
   ```

1. Run the PHP client application. If successful, the Umbrella Reporting v2 API request returns a `200` response.

   ```shell
   php reportv2_api_sample.php
   ```

The OAuth 2.0 middleware on the Guzzle HTTP client refreshes the access token when it expires. The Guzzle HTTP client can make API calls to any Umbrella Reporting v2 endpoint authorized by the OAuth 2.0 token.
