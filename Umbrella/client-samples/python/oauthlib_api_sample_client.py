"""
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
"""

import requests
import json
import os
import time
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

token_url = os.environ.get('TOKEN_URL') or 'https://management.api.umbrella.com/auth/v2/oauth2/token'
#Export/Set the environment variables
client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
org_id = os.environ.get('ORG_ID')

class UmbrellaAPI:
    def __init__(self, url, ident, secret):
        self.url = url
        self.ident = ident
        self.secret = secret
        self.token = None

    def GetToken(self):
        auth = HTTPBasicAuth(self.ident, self.secret)
        client = BackendApplicationClient(client_id=self.ident)
        oauth = OAuth2Session(client=client)
        self.token = oauth.fetch_token(token_url=self.url, auth=auth)
        return self.token

    def Query(self, end_point):
        success = False
        req = None
        if self.token == None:
            self.GetToken()
        while not success:
            try:
                api_headers = {'Authorization': "Bearer " + self.token['access_token']}
                req = requests.get('https://reports.api.umbrella.com/v2/{}'.format(end_point), headers=api_headers)
                req.raise_for_status()
                success = True
            except TokenExpiredError:
                token = self.GetToken()
            except Exception as e:
                raise(e)
        return req

# Exit out if the require client_id, client_secret and org_id are not set
for var in ['API_SECRET', 'API_KEY', 'ORG_ID']:
    if os.environ.get(var) == None:
        print("Required environment variable: {} not set".format(var))
        exit()

# Get token and make an API request
end_point = 'organizations/{}/summary?from=-5days&to=now'.format(org_id)
api = UmbrellaAPI(token_url, client_id, client_secret)
print("Token: " + str(api.GetToken()))
for count in range(5):
    rsp = api.Query(end_point)
    print(rsp.json())
