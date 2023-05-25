"""
Copyright (c) 2023 Cisco and/or its affiliates.
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
import csv
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

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

    ''' GET API request to an Umbrella endpoint '''
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
                resp = requests.get('https://api.umbrella.com/{}'.format(end_point), headers=api_headers)
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
                resp = requests.post('https://api.umbrella.com/{}'.format(end_point), json=data, headers=api_headers)
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
                resp = requests.delete('https://api.umbrella.com/{}'.format(end_point), json=data, headers=api_headers)
                resp.raise_for_status()
                success = True
            except TokenExpiredError:
                token = self.GetToken()
            except Exception as e:
                raise(e)
        return resp

''' Read destinations for destination list from CSV file and return data '''
def read_destinations_from_csv(destination_filename, filters):
    print(f'Read destinations from file: {destination_filename}')

    data = []
    with open(destination_filename, newline='') as f:
        reader = csv.DictReader(f)

        print(f"Print rows in CSV file")
        for row in reader:
            # format of destinations CSV file
            # print(row['id'], row['type'], row['destination'], row['comment'], row['createdAt'])
            d = {}

            if 'destinations' in filters:
                d['destination'] = row['destination']
            if 'comment' in filters:
                if 'comment' in row:
                    d['comment'] = row['comment']
            if 'id' in filters:
                d['id'] = row['id']
            if 'type' in filters:
                d['type'] = row['type']
            if 'createdAt' in filters:
                if 'createdAt' in row:
                    d['createdAt'] = row['createdAt']
            if d.keys():
                # print(f"row of data from CSV file {d}")
                data.append(d)
        f.close()
    return data

''' Write destinations from a destination list to CSV file '''
def write_destinations_to_csv(data, destination_filename):

    with open(destination_filename,'w',encoding='utf-8') as f:

        # Write header for CSV file
        fieldnames = ['id', 'destination', 'type', 'comment', 'createdAt']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        print(f'Write destinations to file: {destination_filename}')

        # Write destinations to CSV file
        for destinations in data:
            for d in destinations:
                writer.writerow(
                    {
                    'destination': d['destination'],
                    'type': d['type'],
                    'comment': d['comment']
                    }
                )
        f.close()

''' Write destination list summary information to CSV file '''
def write_destination_lists_summary_to_csv(data, destination_filename):

    with open(destination_filename, 'w', newline='') as f:

        # Write header for CSV file
        fieldnames = ['name', 'id', 'type', 'access', 'destinationCount', 'domainCount', 'urlCount', 'ipv4Count', 'applicationCount', 'createdAt', 'modified']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        print(f'Write summary information to file: {destination_filename}')
        # Write summary information for destination lists to CSV file

        meta = {}
        for dl in data:
            for d in dl:
                meta = d['meta']
                writer.writerow(
                    {
                    'name': d['name'],
                    'id': d['id'],
                    'type': 'web' if d['bundleTypeId'] == 2 else 'dns',
                    'access': d['access'],
                    'destinationCount': meta['destinationCount'],
                    "domainCount": meta['domainCount'],
                    "urlCount": meta['urlCount'],
                    "ipv4Count": meta['ipv4Count'],
                    "applicationCount": meta['applicationCount'],
                    "createdAt": d['createdAt'],
                    "modified": d['modifiedAt']
                    }
                )
        f.close()
