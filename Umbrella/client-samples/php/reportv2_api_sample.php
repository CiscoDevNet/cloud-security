<?php
/*
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
*/

use kamermans\OAuth2\GrantType\ClientCredentials;
use kamermans\OAuth2\GrantType\RefreshToken;
use kamermans\OAuth2\OAuth2Middleware;
use GuzzleHttp\HandlerStack;
use GuzzleHttp\Client;
require 'vendor/autoload.php';


// Get ORG_ID, API_KEY and API_SECRET from environment
$client_id = getenv("API_KEY");
$client_secret = getenv("API_SECRET");
$org_id = getenv("ORG_ID");

// Authorization client - this is used to request OAuth access tokens
$reauth_client = new GuzzleHttp\Client([
    // URL for access_token request
    'base_uri' => 'https://management.api.umbrella.com/auth/v2/oauth2/token',
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

// This is the normal Guzzle client that you use in your application
$client = new GuzzleHttp\Client([
    'handler' => $stack,
    'auth'    => 'oauth',
]);

$response = $client->get("https://reports.api.umbrella.com/v2/organizations/$org_id/summary?from=-5days&to=now");

echo "Status: ".$response->getStatusCode()."\n";
