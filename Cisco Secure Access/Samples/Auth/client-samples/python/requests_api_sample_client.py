"""
Copyright (c) 2024 Cisco and/or its affiliates.
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

class SecureAccessAPI():
	def __init__(self, token_url, client_id, client_secret):
		self.token_url = token_url
		self.client_id = client_id
		self.client_secret = client_secret

		try:
			self.access_token = self.getAccessToken()
			if self.access_token is None:
				raise Exception("Request for access token failed")
		except Exception as e:
			print(e)
	def getAccessToken(self):
		try:
			payload={}
			rsp = requests.post(self.token_url, data=payload, auth=(self.client_id, self.client_secret))
			rsp.raise_for_status()
		except Exception as e:
			print(e)
			return None
		else:
			clock_skew = 300
			self.access_token_expiration = int(time.time()) + rsp.json()['expires_in'] - clock_skew
			return rsp.json()['access_token']

	def __str__(self):
		return "token_url: {} client_id: {} client_secret: {} access_token_expiration: {}".format(self.token_url, self.client_id, self.client_secret, self.access_token_expiration)

def refreshToken(decorated):
	def wrapper(api, *args, **kwargs):
		if int(time.time()) > api.access_token_expiration:
			api.access_token = api.getAccessToken()
		return decorated(api, *args, **kwargs)
	return wrapper

@refreshToken
def callSecureAccessApi(api, path):
	try:
		api_headers = {}
		api_headers['Authorization'] = 'Bearer ' + api.access_token
		r = requests.get('https://api.sse.cisco.com/reports/v2' + path, headers=api_headers)
		r.raise_for_status()
	except Exception as e:
		print("Report API call failed for {}: {}", path, e)
	else:
		print(json.dumps(r.json(), indent=4))

def lookupOrgSummary():
    api = SecureAccessAPI(token_url, client_id, client_secret)
    for count in range(5):
        callSecureAccessApi(api, '/summary?from=-5days&to=now')

token_url = os.environ.get('TOKEN_URL') or 'https://api.sse.cisco.com/auth/v2/token'
#Export/Set the environment variables
client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')

# Exit out if the client_id or client_secret is not set
for var in ['API_SECRET', 'API_KEY']:
    if os.environ.get(var) == None:
        print("Required environment variable: {} not set".format(var))
        exit()

lookupOrgSummary()