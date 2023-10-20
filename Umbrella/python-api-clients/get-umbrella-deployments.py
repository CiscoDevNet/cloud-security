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
from umbrella.deployments.networks import Networks
from umbrella.deployments.internalnetworks import InternalNetworks
from umbrella.deployments.roamingcomputers import RoamingComputers
from umbrella.deployments.virtualappliances import VirtualAppliances
from umbrella.deployments.networktunnels import NetworkTunnels, NetworkTunnelsState
from umbrella.deployments.datacenters import DataCenters
from umbrella.deployments.internaldomains import InternalDomains
from umbrella.deployments.networkdevices import NetworkDevices
from umbrella.deployments.policies import Policies
from umbrella.deployments.sites import Sites


# Export/Set the environment variables
#os.environ['API_KEY'] = ''
#os.environ['API_SECRET'] = ''

client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
token_url = os.environ.get('TOKEN_URL') or 'https://api.umbrella.com/auth/v2/token'
export_sub_dir = 'exported-deployments-data'


def get_networks(umbrella_api):
    '''Get Networks'''
    params = {}
    params['page'] = 1
    params['limit'] = 50

    networks = Networks(umbrella_api, export_sub_dir)
    networks.writeDeployment(networks.listNetworks(params), 'csv')

def get_internal_networks(umbrella_api):
    '''Get Internal Networks'''
    params = {}
    params['page'] = 1
    params['limit'] = 50
    internalnetworks = InternalNetworks(umbrella_api, export_sub_dir)
    internalnetworks.writeDeployment(internalnetworks.listInternalNetworks(params), 'csv')

def get_roaming_computers(umbrella_api):
    '''Get Umbrella Roaming Computers'''
    params = {}
    params['page'] = 1
    params['limit'] = 50
    rcs = RoamingComputers(umbrella_api, export_sub_dir)
    rcs.writeDeployment(rcs.listRoamingComputers(params), 'csv')

def get_network_tunnels(umbrella_api):
    '''Get Umbrella Network Tunnels'''
    params = {}
    params['limit'] = 50
    tunnels = NetworkTunnels(umbrella_api, export_sub_dir)
    tunnels.writeDeployment(tunnels.getTunnels(params), 'json')

def get_network_tunnel_state(umbrella_api):
    '''Get Umbrella Network Tunnels state information'''
    params = {}
    tState = NetworkTunnelsState(umbrella_api, export_sub_dir)
    tState.writeDeployment(tState.getTunnelsState(params), 'json')

def get_network_tunnel_datacenters(umbrella_api):
    '''Get Umbrella Data Centers associated with Network Tunnels'''
    params = {}
    dcs = DataCenters(umbrella_api, export_sub_dir)
    dcs.writeDeployment(dcs.getDataCenters(params), 'json')

def get_network_devices(umbrella_api):
    '''Get Umbrella Network Devices'''
    params = {}
    # no pagination
    networkdevices = NetworkDevices(umbrella_api, export_sub_dir)
    networkdevices.writeDeployment(networkdevices.getNetworkDevices(params), 'json')

def get_sites(umbrella_api):
    '''Get Umbrella Sites'''
    params = {}
    params['page'] = 1
    params['limit'] = 50
    sites = Sites(umbrella_api, export_sub_dir)
    sites.writeDeployment(sites.listSites(params), 'csv')

def get_internal_domains(umbrella_api):
    '''Get Umbrella Internal Domains'''
    params = {}
    # no pagination
    internaldomains = InternalDomains(umbrella_api, export_sub_dir)
    internaldomains.writeDeployment(internaldomains.getInternalDomains(params), 'json')

def get_virtual_appliances(umbrella_api):
    '''Get Umbrella Virtual Appliances'''
    params = {}
    params['page'] = 1
    params['limit'] = 50
    vas = VirtualAppliances(umbrella_api, export_sub_dir)
    vas.writeDeployment(vas.listVirtualAppliances(params), 'json')

def get_deployment_policies(umbrella_api):
    '''Get Umbrella Deployment Policies'''
    params = {}
    params['page'] = 1
    params['limit'] = 50
    policies = Policies(umbrella_api, export_sub_dir)
    policies.writeDeployment(policies.listPolicies(params), 'csv')


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

        # Get Networks
        get_networks(umbrella_api)

        # Get Internal Networks
        get_internal_networks(umbrella_api)

        # Get Roaming Computers
        get_roaming_computers(umbrella_api)

        # Get Umbrella Virtual Appliances
        get_virtual_appliances(umbrella_api)

        # Get Deployment Policies
        get_deployment_policies(umbrella_api)

        # Get Internal Domains
        get_internal_domains(umbrella_api)

        # Get Umbrella Sites
        get_sites(umbrella_api)

        # Get Network Devices
        get_network_devices(umbrella_api)

        # Get Network Tunnels
        get_network_tunnels(umbrella_api)

    except Exception as e:
        raise(e)
