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

''' Get destinations in the destination lists and export to CSV files '''

import json, os
import datetime

from datetime import datetime

from umbrella.destination_lists import UmbrellaAPI
from umbrella.destination_lists import write_destinations_to_csv

# Export/Set the environment variables
client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
token_url = os.environ.get('TOKEN_URL') or 'https://api.umbrella.com/auth/v2/token'
cur_dir = os.environ.get('CISCO_SAMPLE_DIR') or os.getcwd()

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

        # Step 2: GET the Umbrella destination lists
        # Paginate the response, limited to 100 destinations lists per API response
        print("Get all destination lists for your Umbrella organization")

        # Initialize API pagination variables
        hasMoreDestinationLists = True
        dl_page = 1

        while hasMoreDestinationLists:
            umbrella_dl_endpoint = 'policies/v2/destinationlists?page=' + str(dl_page)
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
                hasMoreDestinationLists = False
                print(f"No more destinations, page is {dl_page}")
            else:
                dl_page += 1

            # Step 3: GET Destinations in each Umbrella destination list
            # Limited to 100 destinations in a response page
            for i in data:

                # Make a directory from the current directory to hold the exported CSV files
                exported_csv_files_dir = cur_dir + '/exported-destinations-csv-files'
                if not os.path.exists(exported_csv_files_dir):
                    os.makedirs(exported_csv_files_dir)

                dl_id = i['id'] # destination list ID
                if 'name' in i:
                    dl_name = i['name']    
                else:
                    print(f"Destination list name is missing")
                    dl_name = 'no-name'

                umbrella_dest_endpoint = 'policies/v2/destinationlists/' + str(dl_id)

                # Initialize API pagination variables for list of destinations
                hasMoreDestinations = True
                page = 1
                dls_data = []

                while hasMoreDestinations:
                    umbrella_destinations_endpoint = 'policies/v2/destinationlists/' + str(dl_id) + '/destinations?page=' + str(page)
                    destinations_rsp = umbrella_api.ReqGet(umbrella_destinations_endpoint)
                    dest_data = destinations_rsp.json()['data']

                    print(json.dumps(destinations_rsp.json(), indent=4))
                    print(f"The number of destinations {len(dest_data)} in page {page}")

                    # data is the list of destinations
                    if len(dest_data) == 0:
                        hasMoreDestinations = False
                        print(f"Page is {page}")
                    else:
                        page += 1
                        dls_data.append(dest_data)

                # Step 4: Write the destinations to a CSV file
                if len(dls_data) > 0:
                    dl_filename = exported_csv_files_dir + '/' + str(dl_id) + '-' + i['name'] + '-' + str(datetime.now()) + '.csv'
                    write_destinations_to_csv(dls_data, dl_filename)

    except Exception as e:
        raise(e)
