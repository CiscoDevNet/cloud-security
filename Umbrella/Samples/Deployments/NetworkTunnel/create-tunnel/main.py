#!/usr/bin/env python3

"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at "https://developer.cisco.com/docs/licenses".
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

----------------------------------------------------------------------
"""

''' Create Umbrella Network Tunnel through Network Tunnel POST request, and log Network Tunnel response. '''

import base64
import csv
import json, requests, time
from datetime import datetime

''' Base64 encode API key pair '''
def get_auth_token():
    auth_string = key + ':' + secret
    token_bytes = auth_string.encode('ascii')
    token_b64 = base64.b64encode(token_bytes)
    token_string = token_b64.decode('ascii')
    if debug:
        print('[get_auth_token()] auth_string = ' + str(auth_string))
        print('[get_auth_token()] token_string = ' + str(token_string))
    return token_string

''' Write Network Tunnel response to log '''
def write_tunnel_attributes(response, tunnel, lines):
    data = json.loads(response.text)
    status = response.status_code

    # ['tunnelName,deviceType,tunnelId,tunnelKey,umbrellaId,status,error,tunnelCreatedAt\n']
    line = data.get('name', '') if status == 200 else tunnel['tunnelname']
    line += ',' + (data['client'].get('deviceType', '') if status == 200 else tunnel['devicetype'])
    line += ',' + (str(data['client']['authentication']['parameters'].get('id', 0)) if status == 200 else '')
    line += ',' + tunnel['key']
    line += ',' + org_id
    line += ',' + (str(data.get('id', 0)) if status == 200 else '')
    line += ',' + ('Success' if status == 200 else data['error'])
    line += ',' + (data.get('createdAt','') if status == 200 else '')
    line += '\n'
    if debug:
        print('[write_tunnel_attributes()] line = ' + str(line))
        print('[write_tunnel_attributes()] number of fields in response =  %s' % str(len(data)))
    lines += line
    return lines

''' Load Tunnel attributes from CSV to JSON '''
def csv_to_json(tunnel_data):
    jsonArray = []
    with open(tunnel_data, 'r', encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            jsonArray.append(row)
    jsonString = json.dumps(jsonArray, indent=4)
    json_data = json.loads(jsonString)
    if debug:
        print('[csvToJson()] jsonString = ' + jsonString)
    return json_data

''' Create tunnels from attributes in tunnel_data.csv '''
def create_tunnel(tunnel):
    # get authentication token
    authtoken = get_auth_token()

    url = "https://management.api.umbrella.com/v1/organizations/"+ str(org_id) + "/tunnels"
    payload = json.dumps({
        "name": tunnel['tunnelname'],
        "deviceType": tunnel['devicetype'],
        "transport": {
            "protocol": "IPSec"
        },
        "authentication": {
            "type": "PSK",
            "parameters": {
            "idPrefix": tunnel['prefix'],
            "secret": tunnel['key']
            }
        }
    })
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': 'Basic ' + str(authtoken)
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        print('Success. Created ' + str(tunnel['tunnelname']))
    else:
        print('Error creating ' + str(tunnel['tunnelname']) + ', see log for details')
    if debug:
        print('[createTunnel()] response = ' + str(response.text))
    return response

# main
if __name__=='__main__':

    # read credentials
    with open("credentials.json") as f:
        content = json.load(f)
        key = content.get("key")
        secret = content.get("secret")
        org_id = content.get("org_id")
        log_file = content.get("log_file")
        tunnel_data = content.get("tunnel_data")
        debug = content.get("debug")
        f.close()

    # open log file
    log_file = log_file + str(datetime.now().strftime('_%Y_%m_%d_%H_%M')) + '.csv'
    if debug:
        print('[Write to log] ' + log_file)

    lines = ['tunnelName,deviceType,tunnelId,tunnelKey,umbrellaId,status,error,tunnelCreatedAt\n']
    with open(str(log_file), 'w', encoding='utf-8') as file:
        start_time = time.monotonic()

    # read tunnel attributes, create tunnels
        tunnels = csv_to_json(tunnel_data)
        for tunnel in tunnels:
            response = create_tunnel(tunnel)
            write_tunnel_attributes(response, tunnel, lines)
        file.writelines(lines)
        file.close()
        print('Complete - elapsed time = ' + str(round(time.monotonic() - start_time)) + ' seconds')
