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
from umbrella.policies.destinationlists import DestinationLists
from umbrella.policies.destinations import Destinations

# Export/Set the environment variables
#os.environ['API_KEY'] = ''
#os.environ['API_SECRET'] = ''

client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
token_url = os.environ.get('TOKEN_URL') or 'https://api.umbrella.com/auth/v2/token'
export_sub_dir = 'exported-policies-data'


def get_destination_lists(dls):
    ''' Get Destination Lists '''
    params = {} # set pagination parameters
    params['page'] = 1
    params['limit'] = 8 # default is 100
    dls.writePolicy(dls.getDestinationLists(params), 'json')

def create_destination_list(dls):
    '''Create a Destination List'''
    request_body = {
        "name": "dl_three-10-11-23",
        "isGlobal": False,
        "access": "allow"
    }
    dls.writePolicy(dls.postDestinationList(request_body), 'json')

def get_destination_list(dls):
    '''Get a Destination List'''
    path_params = {}
    params = {}
    path_params['destinationListId'] = 17634429 # provide the ID of the destination list
    dls.writePolicy(dls.getDestinationList(path_params, params), 'json')

def patch_destination_list(dls):
    '''Update a Destintion List'''
    path_params = {}
    path_params['destinationListId'] = 17634429 # provide the ID of the destination list
    request_body = {
        "name": 'dl_changed-10-12-23'
    } # update the name of the destination list
    dls.writePolicy(dls.patchDestinationList(path_params, request_body), 'json')

def delete_destination_list(dls):
    '''Delete a Destination List'''
    path_params = {}
    params = {}
    path_params['destinationListId'] = 16322414 # provide the ID of the destination list
    dls.writePolicy(dls.deleteDestinationList(path_params, params), 'json')

def get_destinations_in_dls(ds):
    '''Get the destinations in a Destination List'''
    params = {}
    path_params = {}
    path_params['destinationListId'] = 17634429 # provide the ID of the destination list

    params = {} # set pagination parameters
    params['page'] = 1
    params['limit'] = 8 # default is 100
    ds.writePolicy(ds.getDestinations(path_params, params), 'json')

def create_destinations_in_dls(ds):
    '''Create destinations in a Destination List'''
    path_params = {}
    path_params['destinationListId'] = 17634429 # provide the ID of the destination list
    request_body = [
        {
            "destination": "cisco.com", "comment": "add cisco domain"
        },
        {
            "destination": "mydestination/telemetry.com", "comment": "add telemetry url"
        }
    ]
    ds.writePolicy(ds.postDestinations(path_params, request_body), 'json')

def delete_destinations_in_dls(ds):
    '''Delete destinations in a Destination List'''
    path_params = {}
    path_params['destinationListId'] = 17634429 # provide the ID of the destination list
    request_body = [] # provide the list of destination IDs
    ds.writePolicy(ds.deleteDestinations(path_params, request_body), 'json')

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

        # Initialize a DestinationLists resource with the session
        dls = DestinationLists(umbrella_api, export_sub_dir)

        get_destination_lists(dls)
        create_destination_list(dls)
        get_destination_list(dls)
        patch_destination_list(dls)

        # Initialize a Destinations resource with the session
        ds = Destinations(umbrella_api, export_sub_dir)

        get_destinations_in_dls(ds)
        create_destinations_in_dls(ds)
        delete_destinations_in_dls(ds)

        delete_destination_list(dls)

    except Exception as e:
        raise(e)
