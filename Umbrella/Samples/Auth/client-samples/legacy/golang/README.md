# Go Client Example for Umbrella API OAuth2.0 Authorization

The Go example client application shows how to create an Umbrella Reporting v2 API request protected by the OAuth2.0 authorization framework.

## Prerequisites

Download and install a version of Go for your system. For more information, see [Download Go](https://go.dev/learn/).

**Note:** We recommend that you install Go version 1.16 or higher.

## Overview

To get started, set up the required environment variables:

* `API_KEY`: Umbrella API Reporting v2 key
* `API_SECRET`: Umbrella API Reporting v2 secret
* `ORG_ID`: Umbrella organization ID

### Import Go Libraries

The client application imports the required Go OAuth 2.0 client credentials flow libraries.

```go
import (
    "net/http"
    "golang.org/x/net/context"
    "golang.org/x/oauth2/clientcredentials"
)
```

### Initialize HTTP Client

The example client application initializes an HTTP client object with the client credentials (Umbrella API key and secret) and token url.

The HTTP client is an OAuth 2.0 client credentials flow object that automatically manages the token lifecyle: creation, reuse, and refresh of access tokens.

```go
config := &clientcredentials.Config{
    TokenURL:     https://management.api.umbrella.com/auth/v2/oauth2/token,
    ClientID:     <Umbrella API_KEY>,
    ClientSecret: <Umbrella API_SECRET>,
}
httpClient := config.Client(context.Background())
if httpClient == nil {
    fmt.Printf("Error creating Oauth2 http client for %s ", config.TokenURL)
    return
}
```

### Create HTTP Request

Once initialized, the HTTP client acquires the Bearer token and creates a request to the Umbrella Reporting v2 API.

```go
res, err := httpClient.Get("https://reports.api.umbrella.com/v2/organizations/<ORG_ID>/summary?from=-5days&to=now")
if err != nil {
    fmt.Printf("Error calling API, %s\n", err.Error())
    return
}
```

## Run the Go Client

1. Set the Umbrella Reporting v2 API key, Umbrella Reporting v2 API secret, and Umbrella organization ID as environment variables.

   ```shell
   export API_KEY=<...>
   export API_SECRET=<...>
   export ORG_ID=<...>
   ```

1. Fetch the Go packages required by the client application.

   ```go
   go mod init
   go mod tidy
   ```

1. Run the Go client application.

   ```go
   go run main.go
   ```

When you run the application, the client logs each request and provides the following information:

* Response status code
* Response time
* Request string
* Response body

Since the first request to the Reporting v2 API acquires the access token, you can expect a higher response time. All other requests in the sample application reuse the access token.

Sample output:

```go
Code: 200: RspTime: 746(ms): https://reports.api.umbrella.com/v2/organizations/xxxxxxx/summary?from=-5days&to=now
{"meta":{},"data":{"applications":0,"domains":0,"requestsblocked":0,"filetypes":0,"requests":0,"policycategories":0,"requestsallowed":0,"categories":0,"identitytypes":0,"applicationsblocked":0,"files":0,"identities":0,"policyrequests":0,"applicationsallowed":0}}
Code: 200: RspTime: 286(ms): https://reports.api.umbrella.com/v2/organizations/xxxxxxx/summary?from=-5days&to=now
{"meta":{},"data":{"applications":0,"domains":0,"requestsblocked":0,"filetypes":0,"requests":0,"policycategories":0,"requestsallowed":0,"categories":0,"identitytypes":0,"applicationsblocked":0,"files":0,"identities":0,"policyrequests":0,"applicationsallowed":0}}
Code: 200: RspTime: 204(ms): https://reports.api.umbrella.com/v2/organizations/xxxxxxx/summary?from=-5days&to=now
{"meta":{},"data":{"applications":0,"domains":0,"requestsblocked":0,"filetypes":0,"requests":0,"policycategories":0,"requestsallowed":0,"categories":0,"identitytypes":0,"applicationsblocked":0,"files":0,"identities":0,"policyrequests":0,"applicationsallowed":0}}
```
