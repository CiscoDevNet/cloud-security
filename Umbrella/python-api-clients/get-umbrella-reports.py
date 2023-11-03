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

import os

from umbrella.session import UmbrellaAPI
from umbrella.reports.aggregations import Activity

# Export/Set the environment variables
#os.environ['API_KEY'] = ''
#os.environ['API_SECRET'] = ''

client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
token_url = os.environ.get('TOKEN_URL') or 'https://api.umbrella.com/auth/v2/token'
export_sub_dir = 'exported-reports-data'

# main
if __name__ == '__main__':

    # Exit out if the required API_KEY and API_SECRET are not set in the environment
    for var in ['API_SECRET', 'API_KEY']:
        if os.environ.get(var) == None:
            print("Required environment variable: {} not set".format(var))
            exit()

    try:
        # Create the API client session
        umbrella_api = UmbrellaAPI(token_url, client_id, client_secret)

        # set pagination parameters
        params = {}
        params['offset'] = 0
        params['limit'] = 100
        params['to'] = 'now'
        params['from'] = '-20days'

        # Get Activity Search report
        activity = Activity(umbrella_api, export_sub_dir)
        activity.writeReport(activity.getActivity(params), 'json')

    except Exception as e:
        raise(e)
