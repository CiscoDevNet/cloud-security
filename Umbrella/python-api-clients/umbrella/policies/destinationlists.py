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

class DestinationLists(Policy):
    # policies.destinationlists:read
    def __init__(self, session, export_sub_dir, uri='policies/v2/destinationlists'):
        super(DestinationLists, self).__init__(session, uri, export_sub_dir)
        self._uri = uri


    def getDestinationLists(self, params):
        """
        Return the destination lists in the organization

        parameters: page, limit
        """

        print(f"Get Destination Lists")
        return self.listPolicies(params)

    def postDestinationList(self, request_body):
        """
        Create a destination list in the organization
        Required: name, access, isGlobal
        """

        print(f"Create a Destination List")
        return self.postPolicy(request_body)

    def getDestinationList(self, path_params, params):
        """
        Return a certain destination list in the organization

        parameters: destination list ID
        """

        if 'destinationListId' in path_params:
            url_with_id = self._uri + '/' + str(path_params['destinationListId'])
        else:
            raise Exception("Did not set destinationListId.")
        print(f"Get a Destination List")
        return self.getPolicy(params, url_with_id)

    def patchDestinationList(self, path_params, request_body):
        """
        Update a certain destination list in the organization

        parameters: destination list ID
        """

        if 'destinationListId' in path_params:
            url_with_id = self._uri + '/' + str(path_params['destinationListId'])
        else:
            raise Exception("Did not set destinationListId.")
        print(f"Patch a Destination List")
        return self.patchPolicy(request_body, url_with_id)

    def deleteDestinationList(self, path_params, params):
        """
        Delete a certain destination list in the organization

        parameters: destination list ID

        Returns no data
        """

        if 'destinationListId' in path_params:
            url_with_id = self._uri + '/' + str(path_params['destinationListId'])
        else:
            raise Exception("Did not set destinationListId.")
        print(f"Delete a Destination List")
        return self.deletePolicy(params, url_with_id)
