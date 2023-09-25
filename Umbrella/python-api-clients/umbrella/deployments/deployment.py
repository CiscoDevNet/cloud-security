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

import json
from datetime import datetime

from umbrella.utils import write_data_to_csv
from umbrella.utils import write_data_to_json
from umbrella.utils import get_directory

class Deployment(object):
    def __init__(self, session, uri, export_sub_dir):
        self._session = session
        self._uri = uri
        self._export_sub_dir = export_sub_dir

    def getDeployment(self, params):
        ''' Get the Deployment resource'''

        umbrella_endpoint = self._uri

        try:
            rsp = self._session.GetToken()
            rsp = self._session.ReqGet(umbrella_endpoint, params)

            if rsp.status_code == 200 or rsp.status_code == 202 or rsp.status_code == 204:
                print(f"response status is OK")
                #print(json.dumps(rsp.json(), indent=4))

                if len(rsp.json()) == 0:
                    print(f"No data in response")
                return rsp.json()
            else:
                print(f"Error condition: {rsp.status_code}")

        except Exception as e:
            print(f'Error occured: {e}')

    def listDeployment(self, params):
        ''' List the Deployment resources '''

        hasMoreData = True
        data = []
        umbrella_endpoint = self._uri

        # page query parameter
        if 'page' in params:
            if params['page'] < 1:
                params['page'] = 1 # default page value

        # limit query parameter
        if 'limit' in params:
            if params['limit'] > 100 or params['limit'] < 1:
                params['limit'] = 100 #default limit value

        try:

            while hasMoreData:
                rsp = self._session.ReqGet(umbrella_endpoint, params)
                if rsp.status_code == 200 or rsp.status_code == 202 or rsp.status_code == 204:
                    print(f"response status is OK")
                    #print(json.dumps(rsp.json(), indent=4))

                    if len(rsp.json()) == 0:
                        hasMoreData = False
                        print(f"No data in response")
                    else:
                        if 'page' in params:
                            params['page'] += 1
                            data.extend(rsp.json())
                            #print(f"records read: {len(data)}")
                            #print(f"next page: {params['page']}")
                else:
                    print(f"Error condition: {rsp.status_code}")
                    hasMoreData = False
            return data
        except Exception as e:
            print(f'Error occured: {e}')

    def writeDeployment(self, data, write_data='json'):
        ''' Write the deployment resource to CSV or JSON file.'''

        if len(data) == 0:
            print(f"No data to write")
            return

        isDataObj = False
        deployment_type = self._uri.split('/')[2]
        print(f"Deployment type: {deployment_type}")
        if isinstance(data, dict):
            isDataObj = True

        d_filename = get_directory(self._export_sub_dir) + '/' + f'{deployment_type}_list_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}' + '.' + write_data
        if write_data == 'csv' and not isDataObj:
            write_data_to_csv(data, d_filename)
        elif write_data == 'json' or isDataObj:
            write_data_to_json(data, d_filename)
        else:
            print(f"No data in response for " + f'{deployment_type}_list_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}')
