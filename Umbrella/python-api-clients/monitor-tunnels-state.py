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
import json
from datetime import datetime

from umbrella.session import UmbrellaAPI
from umbrella.deployments.networktunnels import NetworkTunnelsState, NetworkTunnels
from umbrella.utils import create_log_file, send_email

# Export/Set the environment variables
#os.environ['API_KEY'] = ''
#os.environ['API_SECRET'] = ''

client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
token_url = os.environ.get('TOKEN_URL') or 'https://api.umbrella.com/auth/v2/token'
export_sub_dir = 'exported-tunnels-state-data'

def check_tunnel_state(t, monitor_config):
    ''' Check status of Umbrella Network Tunnels and log results '''
    tunnel_id = ''
    tunnel_status = ''
    tunnel_data = []
    sender = monitor_config['sender']
    receiver = monitor_config['receiver']
    smtp_username = monitor_config['smtp_username']
    smtp_password = monitor_config['smtp_password']
    server = monitor_config['smtp_server']
    subject = monitor_config['email_subject']
    monitor_interval = monitor_config['monitor_interval'] # monitor interval in seconds
    monitor_logfile = monitor_config['logfile'] # logfile
    email_alert = monitor_config['email_alert'] # enable or disable email alerts
    max_inactive_interval = monitor_config['max_inactive_interval']

    # Tunnel States: UP, ACTIVE, INACTIVE, UNESTABLISHED, UNKNOWN

    try:
        if 'tunnelId' in t:
            tunnel_id = t['tunnelId']
        logfile = create_log_file(monitor_logfile + '-' + tunnel_id, export_sub_dir)

        with open(logfile,'w',encoding='utf-8') as f:

            f.write("Umbrella Monitoring Script starting at {}\n".format(datetime.now()))

            if 'status' in t:
                tunnel_status = t['status']

            f.write("Tunnel {} state is {}.\n".format(tunnel_id, tunnel_status))

            # State of the tunnel (DOWN or UNESTABLISHED)
            if tunnel_status != 'UP':
                tunnel_data.append(t)
                f.write(json.dumps(tunnel_data, indent=4))
            else:
                # Is Tunnel state UP, compare the time of the last state update
                last_modified_timestamp = datetime.strptime( t['modifiedAt'][:-4], "%Y-%m-%dT%H:%M:%S.%f")
                delta_since_last_update = (datetime.utcnow()-last_modified_timestamp).total_seconds()
                f.write("Tunnel {} last state update {} seconds ago.  ".format(tunnel_id, delta_since_last_update))

                #if last 'modifiedAt' time delta is greater than configured MAX_INACTIVE_INTERVAL, then the tunnel is INACTIVE
                if delta_since_last_update > max_inactive_interval:
                    f.write("Tunnel is UP but INACTIVE.\n")
                    tunnel_data.extend(t)
                else:
                    f.write( "Tunnel UP {} and ACTIVE {}.\n".format(tunnel_id, delta_since_last_update))
            f.close()
    except Exception as e:
        raise(e)

    try:
        if email_alert:
            send_email(server, sender, receiver, subject, tunnel_data, username="", password="", sub_type="plain")
    except Exception as e:
        raise(e)

def monitor_tunnels_state(umbrella_api, monitor_config):
    ''' Monitor state of Umbrella Network Tunnels '''
    params = {}
    tState = NetworkTunnelsState(umbrella_api, export_sub_dir)
    tunnel_state_response = []
    tunnel_state_response = tState.getTunnelsState(params)

    if len(tunnel_state_response):
        print(f"tunnel state response: {tunnel_state_response}")

        try:
            for t in tunnel_state_response:
                check_tunnel_state(t, monitor_config)
                #logfile.write("Response: Status = {}, Message Content = {}\n".format(tunnel_state_response.status_code, tunnel_state_response.text))
        except Exception as e:
            raise(e)

def get_network_tunnels(umbrella_api):
    '''Get Umbrella Network Tunnels'''
    params = {}
    params['includeState'] = True
    params['limit'] = 50
    tunnels = NetworkTunnels(umbrella_api, export_sub_dir)
    tunnels.writeDeployment(tunnels.getTunnels(params), 'json')


# main
if __name__=='__main__':

   # Exit out if the required API_KEY and API_SECRET are not set in the environment
    for var in ['API_SECRET', 'API_KEY']:
        if os.environ.get(var) == None:
            print("Required environment variable: {} not set".format(var))
            exit()

    try:

        cwd = os.getcwd() or os.environ.get('CISCO_SAMPLES_DIR')
        print(f"current dir: {cwd}")

        with open(cwd + "/tunnels-state-config.json") as f:
            monitor_config = json.load(f)
            f.close()

            # Create the API client session
            umbrella_api = UmbrellaAPI(token_url, client_id, client_secret)

            # Get the Network Tunnels
            get_network_tunnels(umbrella_api)

            # Monitor the state of the network tunnel (log state and if configured, send email alert)
            monitor_tunnels_state(umbrella_api, monitor_config)

    except Exception as e:
        raise(e)
