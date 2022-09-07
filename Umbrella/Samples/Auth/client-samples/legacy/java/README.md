# Java Spring Security Client Example for Umbrella API OAuth2.0 Authorization

The Java example client application shows how to create an Umbrella Reporting v2 API request protected by the OAuth2.0 authorization framework.

## Prerequisites

Download and install a version of Java for your system. For more information, see [Download Java](https://www.java.com/en/download/manual.jsp).

## Overview

To get started, set up the required environment variables:

* `API_KEY`: Umbrella API Reporting v2 key
* `API_SECRET`: Umbrella API Reporting v2 secret
* `ORG_ID`: Umbrella organization ID

### Maven Project Dependencies

Add the `spring-security-oauth2` library as a dependency in your Maven project. For information about the Spring Security OAuth 2.0 library, see [Spring Security Reference](https://docs.spring.io/spring-security/site/docs/current/reference/html5/).

```xml
<dependency>
    <groupId>org.springframework.security.oauth</groupId>
    <artifactId>spring-security-oauth2</artifactId>
    <version>2.3.3.RELEASE</version>
</dependency>
```

### Import Spring Security OAuth 2.0 Client Library

Import classes from the Spring Security OAuth 2.0 client library.

```java
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.security.oauth2.client.DefaultOAuth2ClientContext;
import org.springframework.security.oauth2.client.OAuth2ClientContext;
import org.springframework.security.oauth2.client.OAuth2RestTemplate;
import org.springframework.security.oauth2.client.token.grant.client.ClientCredentialsResourceDetails;
import org.springframework.security.oauth2.client.token.grant.client.ClientCredentialsAccessTokenProvider;
```

### Initialize HTTP Client

The example client application initializes an HTTP client object with the client credentials (Umbrella API key and secret) and token url.

The HTTP client is an OAuth 2.0 client credentials flow object that automatically manages the token lifecyle: creation, reuse, and refresh of access tokens.

```java
. . .
// Create the OAuth2 client credential resource details.
ClientCredentialsResourceDetails clientCredConfig = new ClientCredentialsResourceDetails();
clientCredConfig.setClientId(<Umbrella API_KEY>);
clientCredConfig.setClientSecret(<Umbrella API_SECRET>);
clientCredConfig.setAccessTokenUri(https://api.umbrella.com/auth/v2/oauth2/token);

// Create an OAuth2 REST template with OAuth 2.0 client credentials access-token-provider
OAuth2RestTemplate restTemplate = new OAuth2RestTemplate(clientCredConfig, new DefaultOAuth2ClientContext());
restTemplate.setRequestFactory(new BufferingClientHttpRequestFactory(new SimpleClientHttpRequestFactory()));
restTemplate.setAccessTokenProvider(new ClientCredentialsAccessTokenProvider());
. . .
```

### Create HTTP Request

Once initialized, the HTTP client acquires the Bearer token and creates a request to the Umbrella Reporting v2 API.

```java
. . .
final String requestUrl = "https://reports.api.umbrella.com/v2/organizations/<ORG_ID>/summary?from=-5days&to=now"
final String response = restTemplate.getForObject(requestUrl, String.class);
. . .
```

## Run the Java Spring Security Client

1. Set the Umbrella Reporting v2 API key, Umbrella Reporting v2 API secret, and Umbrella organization ID as environment variables.

   ```shell
   export API_KEY=<...>
   export API_SECRET=<...>
   export ORG_ID=<...>
   ```

1. Build the application as a single jar with dependencies using Maven. For more information, see [Apache Maven Project](https://maven.apache.org/guides/getting-started/maven-in-five-minutes.html).

   ```shell
   mvn assembly:assembly -DdescriptorId=jar-with-dependencies
   ```

1. Run the Java Spring Security client.

   ```shell
   java -cp target/springjava-1.0-SNAPSHOT-jar-with-dependencies.jar com.cisco.umbrella.oauth2client.ReportsExample
   ```

When you run the application, the client logs each request and provides the following information:

* Response time
* Request string
* Response body

Since the first request to the Reporting v2 API acquires the access token, you can expect a higher response time. All other requests in the sample application reuse the access token.

Sample output:

```java
call#1: RspTime: 980(ms): https://reports.api.umbrella.com/v2/organizations/2423463/summary?from=-5days&to=now
{"meta":{},"data":{"applications":0,"domains":0,"requestsblocked":0,"filetypes":0,"requests":0,"policycategories":0,"requestsallowed":0,"categories":0,"identitytypes":0,"applicationsblocked":0,"files":0,"identities":0,"policyrequests":0,"applicationsallowed":0}}
call#2: RspTime: 333(ms): https://reports.api.umbrella.com/v2/organizations/2423463/summary?from=-5days&to=now
{"meta":{},"data":{"applications":0,"domains":0,"requestsblocked":0,"filetypes":0,"requests":0,"policycategories":0,"requestsallowed":0,"categories":0,"identitytypes":0,"applicationsblocked":0,"files":0,"identities":0,"policyrequests":0,"applicationsallowed":0}}
call#3: RspTime: 392(ms): https://reports.api.umbrella.com/v2/organizations/2423463/summary?from=-5days&to=now
{"meta":{},"data":{"applications":0,"domains":0,"requestsblocked":0,"filetypes":0,"requests":0,"policycategories":0,"requestsallowed":0,"categories":0,"identitytypes":0,"applicationsblocked":0,"files":0,"identities":0,"policyrequests":0,"applicationsallowed":0}}
```
