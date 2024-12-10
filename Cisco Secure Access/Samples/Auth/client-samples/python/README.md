# Python Client Examples for Secure Access API OAuth2.0 Authorization

We provide two Python client example applications. Each client application shows how to create a Cisco Secure Access Reporting API request protected by the OAuth2.0 authorization framework.

## Prerequisites

Download and install a version of Python for your system. For more information, see [Download Python](https://www.python.org/downloads/).

**Note:** We recommend that you install Python version 3.8 or higher.

## Overview

To get started, set up the required environment variables:

* `API_KEY`: Secure Access API key
* `API_SECRET`: Secure Access API secret

The following Python libraries provide the OAuth 2.0 authorization framework:

* Standard: `oauthlib`
* Basic: `requests`

## Python `oauthlib` Client Example

The client application provides the OAuth2.0 client credentials token flow through the `oauthlib` library. We use the `BackendApplicationClient` flow, but the `oauthlib` library supports other flows. For more information about the `oauthlib` library, see [Python OAuth 2.0 Application Flow](https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow).

### Install the OAuth Python Libraries

To install the required OAuth 2.0 client credentials libraries, fetch the Python packages.

```shell
pip install oauthlib
pip install requests_oauthlib
```

The client application imports the following `oauthlib` libraries:

```python
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
```

### Initialize HTTP Client

The example client application initializes an HTTP client object with the client credentials (Secure Access API key and secret), organization ID, and token url.

For example:

```python
auth = HTTPBasicAuth(client_id, client_secret)
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url=url, auth=auth)
```

### Create HTTP Request

The HTTP client object is an OAuth 2.0 client credentials flow object that automatically manages the token lifecyle: creation, reuse, and refresh of access tokens.

```python
try:
    api_headers = {'Authorization': "Bearer " + self.token['access_token']}
    req = requests.get('https://api.sse.cisco.com/reports/v2/{}'.format(end_point), headers=api_headers)
    req.raise_for_status()
    success = True
except TokenExpiredError:
    token = self.GetToken()
except Exception as e:
    raise(e)
```

### Run `oauthlib` Python Client

1. Set the Secure Access Reporting API key and secret as environment variables.

   ```shell
   export API_KEY=<...>
   export API_SECRET=<...>
   ```

1. Run the `oauthlib` Python client application.

   ```shell
   python3 oauthlib_api_sample_client.py
   ```

When you run the application, the client logs the response for each request. In the sample output, the first request to the Secure Access Reporting API acquires the access token. The remaining requests reuse the access token until the token expires. When the token expires, the client automatically refreshes the token.

Sample output:

```python
Token: {'token_type': 'bearer', 'access_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2Mjk5Mzc3MTUsImlhdCI6MTYyOTkzNDExNSwiaXNzIjoidW1icmVsbGEtYXV0aHovYXV0aHN2YyIsIm5iZiI6MTYyOTkzNDExNSwic3ViIjoib3JnLzU3MjE4NzgvdXNlci8xMTgxODU2NCIsInNjb3BlIjoicm9sZTpyb290LWFkbWluIiwiYXV0aHpfZG9uZSI6ZmFsc2V9.mh3OoJV4Wzjv04SSkiDi6rR65Zrd9aigV0K5ciPvF5a2aiy0tKdlLpT_ty0NBxh5ojyt9iO5588Ntu5GzzWvDbGgtdrkus1pMNU92IUioN4cF2Y4yCLooshFfDjiwccuJd8afmD1o6miZ4Tzqg906ZGq5KEwfclzA9lPwmkalpGkQDCYFRCtQWXWIKVHPNhgpZjf1lAgUwDngSvwJHC_KRb1MICHgiM_SolhwIz66ISkdIm_aRKeTK5EAWW0RCBEQx0E2kY1AHVyahrKDZMPV-tQEPxAEaiMhQKqHtJUbITTYt7LQzQZ6aOrOaS-Stip6_lLgcGIPXOUmGFEjg1Vvg', 'expires_in': 3600, 'expires_at': 1629937714.8636105}
{'meta': {}, 'data': {'applications': 0, 'domains': 0, 'requestsblocked': 0, 'filetypes': 0, 'requests': 0, 'policycategories': 0, 'requestsallowed': 0, 'categories': 0, 'identitytypes': 0, 'applicationsblocked': 0, 'files': 0, 'identities': 0, 'policyrequests': 0, 'applicationsallowed': 0}}
{'meta': {}, 'data': {'applications': 0, 'domains': 0, 'requestsblocked': 0, 'filetypes': 0, 'requests': 0, 'policycategories': 0, 'requestsallowed': 0, 'categories': 0, 'identitytypes': 0, 'applicationsblocked': 0, 'files': 0, 'identities': 0, 'policyrequests': 0, 'applicationsallowed': 0}}
```

## Python `requests` Client Example

The client application imports the `requests` Python library.

```python
import requests
```

### Initialize a Python Class

The client application initializes a Python class with the client credentials (Secure Access API key and secret) and token url.

```python
class secureAccessAPI():
    def __init__(self, token_url, client_id, client_secret):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
```

### Create Access Token

Create an access token through the Secure Access Token Authorization API.

```python
    def getAccessToken(self):
        try:
            payload={}
            rsp = requests.post(self.token_url, data=payload, auth=(self.client_id, self.client_secret))
            rsp.raise_for_status()
        except Exception as e:
            print(e)
            return None
        else:
            return rsp.json()['access_token']
```

### Refresh Access Token

The `refreshToken` decorator calls `getAccessToken()`. When the access token is nearly expired, the client application automatically refreshes the token.

```python
def refreshToken(decorated):
    def wrapper(api, *args, **kwargs):
        if int(time.time()) > api.access_token_expiration:
            api.access_token = api.getAccessToken()
        return decorated(api, *args, **kwargs)
    return wrapper
```

### Secure Access API Request

Before the application sends a request to the Secure Access Reporting API, the client acquires an access token.

```python
@refreshToken
def callSecureAccessApi(api, path):
    try:
        api_headers = {}
        api_headers['Authorization'] = 'Bearer ' + api.access_token
        r = requests.get('https://api.sse.cisco.com/reports/v2/' + path, headers=api_headers)
        r.raise_for_status()
    except Exception as e:
        print("Report API call failed for {}: {}", path, e)
    else:
        print(json.dumps(r.json(), indent=4))
```

### Run `requests` Python Client

1. Set the Secure Access Reporting API key and secret as environment variables.

   ```shell
   export API_KEY=<...>
   export API_SECRET=<...>
   ```

1. Run the `requests` Python client application.

   ```shell
   python3 requests_api_sample_client.py
   ```

When you run the application, the client logs the response for each request. In the sample output, the first request to the Secure Access Reporting API acquires the access token. The remaining requests reuse the access token until the token expires. When the token expires, the client automatically refreshes the token.

Sample output:

```python
Token: {'token_type': 'bearer', 'access_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2Mjk5Mzc3MTUsImlhdCI6MTYyOTkzNDExNSwiaXNzIjoidW1icmVsbGEtYXV0aHovYXV0aHN2YyIsIm5iZiI6MTYyOTkzNDExNSwic3ViIjoib3JnLzU3MjE4NzgvdXNlci8xMTgxODU2NCIsInNjb3BlIjoicm9sZTpyb290LWFkbWluIiwiYXV0aHpfZG9uZSI6ZmFsc2V9.mh3OoJV4Wzjv04SSkiDi6rR65Zrd9aigV0K5ciPvF5a2aiy0tKdlLpT_ty0NBxh5ojyt9iO5588Ntu5GzzWvDbGgtdrkus1pMNU92IUioN4cF2Y4yCLooshFfDjiwccuJd8afmD1o6miZ4Tzqg906ZGq5KEwfclzA9lPwmkalpGkQDCYFRCtQWXWIKVHPNhgpZjf1lAgUwDngSvwJHC_KRb1MICHgiM_SolhwIz66ISkdIm_aRKeTK5EAWW0RCBEQx0E2kY1AHVyahrKDZMPV-tQEPxAEaiMhQKqHtJUbITTYt7LQzQZ6aOrOaS-Stip6_lLgcGIPXOUmGFEjg1Vvg', 'expires_in': 3600, 'expires_at': 1629937714.8636105}
{'meta': {}, 'data': {'applications': 0, 'domains': 0, 'requestsblocked': 0, 'filetypes': 0, 'requests': 0, 'policycategories': 0, 'requestsallowed': 0, 'categories': 0, 'identitytypes': 0, 'applicationsblocked': 0, 'files': 0, 'identities': 0, 'policyrequests': 0, 'applicationsallowed': 0}}
{'meta': {}, 'data': {'applications': 0, 'domains': 0, 'requestsblocked': 0, 'filetypes': 0, 'requests': 0, 'policycategories': 0, 'requestsallowed': 0, 'categories': 0, 'identitytypes': 0, 'applicationsblocked': 0, 'files': 0, 'identities': 0, 'policyrequests': 0, 'applicationsallowed': 0}}
```
