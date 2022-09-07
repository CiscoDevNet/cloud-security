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

package com.cisco.umbrella.oauth2client;

import java.io.IOException;
import java.util.concurrent.ExecutionException;
import org.springframework.http.client.BufferingClientHttpRequestFactory;
import org.springframework.http.client.ClientHttpRequest;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.security.oauth2.client.DefaultOAuth2ClientContext;
import org.springframework.security.oauth2.client.OAuth2ClientContext;
import org.springframework.security.oauth2.client.OAuth2RestTemplate;
import org.springframework.security.oauth2.client.token.grant.client.ClientCredentialsResourceDetails;
import org.springframework.security.oauth2.client.token.grant.client.ClientCredentialsAccessTokenProvider;


public class ReportsExample {

    private static final int API_REPEAT_COUNT = 3;
    private static final int API_REPEAT_DELAY_IN_SEC = 1;

    private static final String UMBRELLA_OAUTH2_TOKEN_URI = "https://api.umbrella.com/auth/v2/oauth2/token";
    private static final String UMBRELLA_REPORTS_SUMMARY_URI = "https://reports.api.umbrella.com/v2/organizations/{ORG_ID}/summary?from=-5days&to=now";

    public static void main(String... args) throws IOException, InterruptedException, ExecutionException {
        // Timestamps to compute response time
        long startTime, rspTime;

        // Get clientID, clientSecret, orgId from the envars
        final String clientId = System.getenv("API_KEY");
        if (clientId == null) {
            System.out.println("Mandatory environment variable API_KEY not set");
            System.exit(1);
        }
        final String clientSecret = System.getenv("API_SECRET");
        if (clientSecret == null) {
            System.out.println("Mandatory environment variable API_SECRET not set");
            System.exit(1);
        }
        final String orgId = System.getenv("ORG_ID");
        if (orgId == null) {
            System.out.println("Mandatory environment variable ORG_ID not set");
            System.exit(1);
        }

        // Create the OAuth2 client credential resource details.
        ClientCredentialsResourceDetails clientCredConfig = new ClientCredentialsResourceDetails();
        clientCredConfig.setClientId(clientId);
        clientCredConfig.setClientSecret(clientSecret);
        clientCredConfig.setAccessTokenUri(UMBRELLA_OAUTH2_TOKEN_URI);

        // Create an OAuth2 REST template with OAuth2 client-cred access-token-provider
        OAuth2RestTemplate restTemplate = new OAuth2RestTemplate(clientCredConfig, new DefaultOAuth2ClientContext());
        restTemplate.setRequestFactory(new BufferingClientHttpRequestFactory(new SimpleClientHttpRequestFactory()));
        restTemplate.setAccessTokenProvider(new ClientCredentialsAccessTokenProvider());

        // Use the REST template to call Umbrella Reports API calls.
        // The access-token is re-used and re-freshed automatically, as per RFC-6749.
        final String requestUrl = UMBRELLA_REPORTS_SUMMARY_URI.replace("{ORG_ID}", orgId);
        for (int i = 0; i < API_REPEAT_COUNT; i++) {
            startTime = System.currentTimeMillis();
            final String response = restTemplate.getForObject(requestUrl, String.class);
            rspTime = System.currentTimeMillis() - startTime;
            System.out.println("call#" + (i+1) + ": RspTime: " + rspTime + "(ms): " + requestUrl);
            System.out.println(response);

            Thread.sleep(API_REPEAT_DELAY_IN_SEC * 1000);
        }
    }

}
