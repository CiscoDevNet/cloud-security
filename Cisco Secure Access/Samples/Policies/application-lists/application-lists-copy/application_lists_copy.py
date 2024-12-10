"""
Copyright (c) 2024 Cisco and/or its affiliates.
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

'''
Manage application lists of internet applications in Secure Access

Create API key credentials for an organization in Secure Access.
Get an access token using the organization's API credentials.
Get the application lists in the organization, identified by the ID.
Get the details for each application list, including the list of applications and list of content categories for the applications in the list.
Write out the details for all of the application lists in the organization to a file in the JSON format.

Read the file that contains the application list information from the organization.
Create new application lists from the application list information that was serialized to file. Create unique names for the new application lists in the organization.
'''

import requests
import random
import json
import os
from dotenv import dotenv_values
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

# try and load the environment variables from the .env file
dotenv_config = dotenv_values(".env")

# get and set the environment variables
token_url = os.environ.get('TOKEN_URL') or 'https://api.sse.cisco.com/auth/v2/token'
client_id = os.environ.get('API_KEY') or dotenv_config['API_KEY']
client_secret = os.environ.get('API_SECRET') or dotenv_config['API_SECRET']

policies = 'policies'
PUT = 'put'
POST = 'post'
GET = 'get'
DELETE = 'delete'
PATCH = 'patch'

# The directory where to write out files
output_dir = os.environ.get('OUTPUT_DIR') or dotenv_config['OUTPUT_DIR']

first_output_file = output_dir + "/application_lists_json_get.out"
second_output_file = output_dir + "/second_application_lists_json_get.out"

# Define the API endpoints
application_lists_endpoint = "applicationLists"
application_lists_details_endpoint = "applicationLists/{}"

class API:
    def __init__(self, url, ident, secret):
        self.url = url
        self.ident = ident
        self.secret = secret
        self.token = None

    def GetToken(self):
        auth = HTTPBasicAuth(self.ident, self.secret)
        client = BackendApplicationClient(client_id=self.ident)
        oauth = OAuth2Session(client=client)
        self.token = oauth.fetch_token(token_url=self.url, auth=auth)
        return self.token

    def Query(self, scope, end_point, operation, request_data=None):
        success = False
        base_uri = 'https://api.sse.cisco.com/' + scope + "/v2"
        req = None
        if self.token == None:
            self.GetToken()
        while not success:
            try:
                api_headers = {
                    'Authorization': "Bearer " + self.token['access_token'],
                    "Content-Type": "application/json"
                }
                if operation in GET:
                    req = requests.get('{}/{}'.format(base_uri, end_point), headers=api_headers)
                elif operation in PATCH:
                    req = requests.patch('{}/{}'.format(base_uri, end_point), headers=api_headers, json=request_data)
                elif operation in POST:
                    req = requests.post('{}/{}'.format(base_uri, end_point), headers=api_headers, json=request_data)
                elif operation in PUT:
                    req = requests.put('{}/{}'.format(base_uri, end_point), headers=api_headers, json=request_data)
                elif operation in DELETE:
                    req = requests.delete('{}/{}'.format(base_uri, end_point), headers=api_headers)
                req.raise_for_status()
                success = True
            except TokenExpiredError:
                token = self.GetToken()
            except Exception as e:
                raise(e)
        return req

def get_application_lists(api, application_list_file):
    '''
    Make an API request to the Application Lists API to get the application lists in the organization.
    For each application list with a given ID, get the details about the application list.
    Write the application list information to a file.
    '''

    print(f"Get the application lists in the organization.")

    try:
        # Make the GET request to the initial API endpoint
        response = api.Query(policies, application_lists_endpoint, GET)

        # Check if the API request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            application_details = []

            for application_list in data.get('results', []):
                if application_list['applicationListId']:
                    # Collect details for each applicationListId
                    details = get_application_list_details(api, application_list['applicationListId'])
                    if details:
                        application_details.append(details)

            # Write the collected details to a JSON file
            with open(str(application_list_file), 'w', encoding='utf-8') as write_output_file:
                write_output_file.writelines(json.dumps(application_details, indent=4))

            print(f"Application details written to {application_list_file}.")
        else:
            print(f"Failed to retrieve application lists. Status code: {response.status_code}")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}.")

def get_application_list_details(api, application_list_id):
    '''
    Make an API request to the Application Lists API to get the details for an application list in the organization.
    Return the details about an application list in the JSON format.
    '''

    print(f"Get the details for the application lists in the organization.")
    try:
        # Format the URL with the applicationListId
        url = application_lists_details_endpoint.format(application_list_id)
        print(f"Url for application list details: {url}.")

        # Make the GET request to the application list details endpoint
        response = api.Query(policies, url, GET)

        # Check if the request was successful
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            print(f"Failed to retrieve details for Application List ID {application_list_id}. Status code: {response.status_code}")
            print("Response:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}.")
        return None

def create_application_list(api, application_lists_file, prepend_list_name=None):
    '''
    Make an API request to the Application Lists API to create a new set of application lists from an existing set of application lists in the organization.
    prepend_list_name: string; If set, prepend the text to each application list name. If prepend_list_name is None, create a random number and use this number to make
    a unique name for the application lists in the organization.
    '''
    print(f"Create the application lists in the organization.")

    data = []

    if prepend_list_name is None:
        random_number = random.random()
        print(f"Random number to create unique application list name: {str(random_number)}")
        prepend_list_name = str(random_number)

    # Load the application list information in the JSON format that you serialized to a file.
    with open(application_lists_file, 'r') as file:
        data = json.load(file)

    # Iterate over each application list object in the JSON data
    for application_list in data:

        # Extract the required fields
        application_list_name = prepend_list_name + ' ' + application_list.get('applicationListName')
        is_default = application_list.get('isDefault')
        application_ids = application_list.get('applicationIds')
        application_category_ids = application_list.get('applicationCategoryIds')

        # Prepare the payload for the POST request
        payload = {
            'applicationListName': application_list_name,
            'isDefault': is_default,
            'applicationIds': application_ids,
            'applicationCategoryIds': application_category_ids
        }

        # Make the POST request
        response = api.Query(policies, application_lists_endpoint, POST, payload)

    # Check the response status
    if response.status_code == 200:
        print(f"Successfully created application list: {application_list_name}")
    else:
        print(f"Failed to create application list: {application_list_name}")
        print(f"Status Code: {response.status_code}, Response: {response.text}")

def main():
    # Exit out if the required variables are not set
    env_vars = {}
    env_vars['API_KEY'] = client_id
    env_vars['API_SECRET'] = client_secret
    env_vars['OUTPUT_DIR'] = output_dir

    for k, v in env_vars.items():
        print(f"env variable: {k} and value: {v}")
        if v is None:
            print("Required environment variable: {} not set".format(k))
            exit()

    try:

        # Get your API token for the organization.
        api = API(token_url, client_id, client_secret)

        # Get the application lists for the organization.
        get_application_lists(api, first_output_file)

        # Create the new application lists for the organization.
        create_application_list(api, first_output_file)

       # Get application lists for the organization after you add the new application lists.
        get_application_lists(api, second_output_file)

    except Exception as e:
        print(e)

# main
if __name__ == "__main__":
    main()
