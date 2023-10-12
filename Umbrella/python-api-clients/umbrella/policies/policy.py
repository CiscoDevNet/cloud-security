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

from umbrella.utils import write_data_to_json
from umbrella.utils import get_directory

class Policy(object):
    def __init__(self, session, uri, export_sub_dir):
        self._session = session
        self._uri = uri
        self._export_sub_dir = export_sub_dir

    def set_uri(self, uri):
        self._uri = uri

    def postPolicy(self, request_body, url_with_id=None):
        ''' Create the resource'''

        if url_with_id:
            umbrella_endpoint = url_with_id
        else:
            umbrella_endpoint = self._uri

        try:
            rsp = self._session.ReqPost(umbrella_endpoint, request_body)
            if rsp.status_code == 200 or rsp.status_code == 202:
                print(f"response status is OK")

                if len(rsp.json()) == 0:
                    print(f"No data in response")
                return rsp.json()
            else:
                print(f"Error condition: {rsp.status_code}")

        except Exception as e:
            print(f'Error occured: {e}')

    def patchPolicy(self, request_body, url_with_id):
        ''' Update the resource'''

        umbrella_endpoint = url_with_id

        try:
            rsp = self._session.ReqPatch(umbrella_endpoint, request_body)
            if rsp.status_code == 200 or rsp.status_code == 202:
                print(f"response status is OK")

                if len(rsp.json()) == 0:
                    print(f"No data in response")
                return rsp.json()
            else:
                print(f"Error condition: {rsp.status_code}")

        except Exception as e:
            print(f'Error occured: {e}')

    def deletePolicy(self, params, url_with_id):
        ''' Delete the resource'''

        umbrella_endpoint = url_with_id

        try:
            rsp = self._session.ReqDelete(umbrella_endpoint, params)
            if rsp.status_code == 200 or rsp.status_code == 202:
                print(f"response status is OK")

                if len(rsp.json()) == 0:
                    print(f"No data in response")
                return rsp.json()
            else:
                print(f"Error condition: {rsp.status_code}")

        except Exception as e:
            print(f'Error occured: {e}')


    def getPolicy(self, params, url_with_id):
        ''' Get the resource'''

        umbrella_endpoint = url_with_id

        try:
            rsp = self._session.ReqGet(umbrella_endpoint, params)

            if rsp.status_code == 200 or rsp.status_code == 202:
                print(f"response status is OK")

                if len(rsp.json()) == 0:
                    print(f"No data in response")
                return rsp.json()
            else:
                print(f"Error condition: {rsp.status_code}")

        except Exception as e:
            print(f'Error occured: {e}')

    def listPolicies(self, params, url_with_id=None):
        ''' List the resources '''

        hasMoreData = True
        data = []

        if url_with_id:
            umbrella_endpoint = url_with_id
        else:
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
                if rsp.status_code == 200 or rsp.status_code == 202:
                    print(f"response status is OK")

                meta = {}
                if rsp.json():
                    d = rsp.json()['data']
                    meta = rsp.json()['meta']
                    print(f"Total records {meta['total']}")
                    if len(d) == 0:
                        hasMoreData = False
                    else:
                        params['page'] += 1
                        data.extend(d)
                else:
                    print(f"No data in response")
                    hasMoreData = False

            return data
        except Exception as e:
            print(f'Error occured: {e}')

    def writePolicy(self, data, write_data='json'):
        ''' Write the resource to CSV or JSON file.'''

        resource_type = self._uri.split('/')[2]
        print(f"Resource type: {resource_type}")

        if len(data) == 0:
            print(f"No data in response for " + f'{resource_type}_list_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}')
            return

        d_filename = get_directory(self._export_sub_dir) + '/' + f'{resource_type}_list_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}' + '.' + write_data
        write_data_to_json(data, d_filename)
