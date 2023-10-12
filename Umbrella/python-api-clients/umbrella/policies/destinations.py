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

from umbrella.policies.policy import Policy

class Destinations(Policy):
    def __init__(self, session, export_sub_dir, uri='policies/v2/destinationlists'):
        super(Destinations, self).__init__(session, uri, export_sub_dir)
        self._uri = uri

    def getDestinations(self, path_params, params):
        """
        Return the destinations in the destination list

        path_parameters: destinationListId
        parameters: none
        """

        if 'destinationListId' in path_params:
            url_with_id = self._uri + '/' + str(path_params['destinationListId']) + '/destinations'
        else:
            raise Exception("Did not set destinationListId.")

        print(f"Get Destinations in DestinationList")
        return self.listPolicies(params, url_with_id)

    def postDestinations(self, path_params, request_body):
        """
        Create the destinations in the destination list

        path_parameters: destinationListId
        parameters: none
        request_body: list of destinations
        """

        if 'destinationListId' in path_params:
            url_with_id = self._uri + '/' + str(path_params['destinationListId']) + '/destinations'
        else:
            raise Exception("Did not set destinationListId.")

        print(f"Create Destinations in DestinationList")
        return self.postPolicy(request_body, url_with_id)

    def deleteDestinations(self, path_params, request_body):
        """
        Delete the destinations in the destination list

        path_parameters: destinationListId
        parameters: none
        request_body: list of destinations
        """

        if 'destinationListId' in path_params:
            url_with_id = self._uri + '/' + str(path_params['destinationListId']) + '/destinations/remove'
        else:
            raise Exception("Did not set destinationListId.")


        print(f"Delete Destinations in Destination List")
        return self.deletePolicy(request_body, url_with_id)
