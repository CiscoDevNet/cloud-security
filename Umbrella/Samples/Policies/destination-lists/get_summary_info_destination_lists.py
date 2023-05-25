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

''' Get summary information for destination lists and export to CSV files '''

import json, os
from datetime import datetime

from umbrella.destination_lists import UmbrellaAPI
from umbrella.destination_lists import write_destination_lists_summary_to_csv


# Export/Set the environment variables
client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
token_url = os.environ.get('TOKEN_URL') or 'https://api.umbrella.com/auth/v2/token'
cur_dir = os.environ.get('CISCO_SAMPLES_DIR') or os.getcwd()

# main
if __name__ == '__main__':

    # Exit out if the required API_KEY and API_SECRET are not set in the environment
    for var in ['API_SECRET', 'API_KEY']:
        if os.environ.get(var) == None:
            print("Required environment variable: {} not set".format(var))
            exit()

    try:
        # Step 1: Create the API client
        umbrella_api = UmbrellaAPI(token_url, client_id, client_secret)

        # Initialize API pagination variables
        hasMoreDestinations = True
        page = 1
        dls_summary_data = []
        org_id = ''

        # Make directory from the current working directory for the destination list summary info CSV files
        exported_csv_files_dir = cur_dir + '/exported-dl-summary-csv-files'
        if not os.path.exists(exported_csv_files_dir):
            os.makedirs(exported_csv_files_dir)

        while hasMoreDestinations:
            umbrella_dl_endpoint = 'policies/v2/destinationlists?page=' + str(page)

            print(f"Get all destination lists for your Umbrella organization")
            
            # Step 2: GET Umbrella Destination Lists API
            # Paginate the response, limited to 100 destination lists per API request
            dls_rsp = umbrella_api.ReqGet(umbrella_dl_endpoint)

            data = []
            meta = {}
            if dls_rsp.json():
                data = dls_rsp.json()['data']
                meta = dls_rsp.json()['meta']
                print(f"Total records {meta['total']}")
                print(json.dumps(dls_rsp.json(), indent=4))
            else:
                print(f"No data in response")
                exit()

            if len(data) == 0:
                hasMoreDestinations = False
                print(f"No more destinations, page is {page}")
            else:
                page += 1
                dls_summary_data.append(data)

            # Get the organization ID to identify exported filename
            for i in data:
                org_id = str(i['organizationId'])
                break

        # Step 3: Write the summary information for the destination lists in the organization
        dl_filename = exported_csv_files_dir + '/' + org_id + '-' + str(datetime.now()) + '.csv'
        write_destination_lists_summary_to_csv(dls_summary_data, dl_filename)

    except Exception as e:
        raise(e)
