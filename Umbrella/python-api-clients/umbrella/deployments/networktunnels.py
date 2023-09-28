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

from umbrella.deployments.deployment import Deployment

class NetworkTunnels(Deployment):
    def __init__(self, session, export_sub_dir):
        super(NetworkTunnels, self).__init__(session, 'deployments/v2/tunnels', export_sub_dir)
        self._session = session
        self._uri = 'deployments/v2/tunnels'

    def getTunnels(self, params):
        """
        Return the network tunnels in the organization
        """

        print(f"List Network Tunnels")
        return self.getDeployment(params)
