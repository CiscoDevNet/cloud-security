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

''' Import destinations from CSV file and delete destinations in destination lists '''

import json, os

from umbrella.destination_lists import UmbrellaAPI
from umbrella.destination_lists import read_destinations_from_csv

# Export/Set the environment variables
client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
token_url = os.environ.get('TOKEN_URL') or 'https://api.umbrella.com/auth/v2/token'
cur_dir = os.environ.get('CISCO_SAMPLE_DIR') or os.getcwd()
umbrella_dl_id = os.environ.get('UMBRELLA_DL_ID')
umbrella_import_filename = os.environ.get('DESTINATIONS_FILENAME')

# main
if __name__ == '__main__':

    # Exit out if the required environment variables are not set
    for var in ['API_SECRET', 'API_KEY', 'UMBRELLA_DL_ID', 'DESTINATIONS_FILENAME']:
        if os.environ.get(var) == None:
            print("Required environment variable: {} not set".format(var))
            exit()
    try:
        # Step 1: Create the API client
        umbrella_api = UmbrellaAPI(token_url, client_id, client_secret)

        # Step 2: GET the summary information for an Umbrella destination list
        umbrella_dl_endpoint = 'policies/v2/destinationlists/' + umbrella_dl_id
        rsp = umbrella_api.ReqGet(umbrella_dl_endpoint)

        destination_count = 0
        if rsp.json():
            print(json.dumps(rsp.json(), indent=4))
            meta = rsp.json()['data']['meta']
            destination_count = meta['destinationCount']

        # Step 3: Read the destination data from a saved CSV file
        data = []
        filters = ['id']
        data = read_destinations_from_csv(umbrella_import_filename, filters)
        num_destinations = len(data)

        # remove destinations API request body accepts an array of destination id
        dest_ids = []
        for i in data:
            dest_ids.append(i['id'])
        if len(dest_ids) != len(data):
            raise Exception

        # Step 4: Delete the destinations from the destination list
        umbrella_destinations_endpoint = 'policies/v2/destinationlists/' + umbrella_dl_id + '/destinations/remove'

        print(f"Delete destinations from a destination list {data}")
        destinations_rsp_remove = umbrella_api.ReqDelete(umbrella_destinations_endpoint, dest_ids)

        # Step 5: Compare the number of destinations in the destination list before the delete operation
        if destinations_rsp_remove.json():
            meta = destinations_rsp_remove.json()['data']['meta']
            print(f"Destinations in destination list before DELETE operation {destination_count}")
            print(f"Destinations in destination list {meta['destinationCount']}")

    except Exception as e:
        raise(e)
