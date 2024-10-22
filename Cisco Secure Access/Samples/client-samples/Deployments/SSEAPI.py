#!/usr/bin/env python3

"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at "https://developer.cisco.com/docs/licenses"
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

----------------------------------------------------------------------
"""

import requests
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth



class SSEAPI:
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

    ''' GET API request to a SSE endpoint '''
    def ReqGet(self, end_point):
        success = False
        resp = None
        if self.token == None:
            self.GetToken()
        while not success:
            try:

                bearer_token = "Bearer " + self.token['access_token']
                api_headers = {
                    "Authorization": bearer_token,
                    "Content-Type": "application/json"
                }
                resp = requests.get('https://api.sse.cisco.com/{}'.format(end_point), headers=api_headers)
                resp.raise_for_status()

                success = True
            except TokenExpiredError:
                token = self.GetToken()
            except Exception as e:
                raise(e)
        return resp

    ''' POST API request to an Umbrella endpoint '''
    def ReqPost(self, end_point, data):
        success = False
        resp = None
        if self.token == None:
            self.GetToken()
        while not success:
            try:
                bearer_token = "Bearer " + self.token['access_token']
                api_headers = { 'Authorization': bearer_token }
                resp = requests.post('https://api.sse.cisco.com/{}'.format(end_point), json=data, headers=api_headers)
                resp.raise_for_status()
                success = True
            except TokenExpiredError:
                token = self.GetToken()
            except Exception as e:
                raise(e)
        return resp

    ''' DELETE API request to an Umbrella endpoint '''
    def ReqDelete(self, end_point, data):
        success = False
        resp = None
        if self.token == None:
            self.GetToken()
        while not success:
            try:
                bearer_token = "Bearer " + self.token['access_token']
                api_headers = { 'Authorization': bearer_token }
                resp = requests.delete('https://api.sse.cisco.com/{}'.format(end_point), json=data, headers=api_headers)
                resp.raise_for_status()
                success = True
            except TokenExpiredError:
                token = self.GetToken()
            except Exception as e:
                raise(e)
        return resp