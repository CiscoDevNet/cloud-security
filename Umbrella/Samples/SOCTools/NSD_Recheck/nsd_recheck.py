#!/usr/bin/env python3

"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at "https://developer.cisco.com/docs/licenses"
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
----------------------------------------------------------------------
"""

""" Newly Seen Domains (NSD) recheck script (nsd_recheck.py).
    Used to maintain an allow list used only for NSD temporary exemptions.
"""


import requests
import json
import os
import sys
import time


class UmbrellaAPI:
    def __init__(self, token_url, client_id, client_secret):
        self.token_url      = token_url
        self.client_id      = client_id
        self.client_secret  = client_secret

        try:
            self.access_token = self.getAccessToken()
            if self.access_token is None:
                raise Exception("Request for access token failed")
        except Exception as e:
            print(e)

    def getAccessToken(self):
        try:
            p = {}
            rsp = requests.post(
                self.token_url, data=p, auth=(self.client_id, self.client_secret)
            )
            rsp.raise_for_status()
        except Exception as e:
            print(e)
            return None
        else:
            clock_skew = 300
            self.access_token_expiration = (
                int(time.time()) + rsp.json()["expires_in"] - clock_skew
            )
            return rsp.json()["access_token"]

    def __str__(self):
        return self.access_token


def gen_open_api_url(dest_id):
    """Generates URL for Open API, including dest_id"""
    open_api_url = (
        "https://api.umbrella.com/policies/v2/destinationlists/"
        + dest_id
        + "/destinations"
    )
    return open_api_url


def get_domains(open_api_token, open_api_url):
    """GET Request destinations from Umbrella API"""
    h = {"Authorization": "Bearer " + open_api_token}
    p = {}
    r = requests.request("GET", open_api_url, headers=h, data=p).json()
    return r["data"]


def check_domains(destinations):
    """Check Categorization and Classification of Domains with the Investigate API"""
    domains = [i["destination"] for i in destinations]
    url = "https://investigate.api.umbrella.com/domains/categorization"
    p   = json.dumps(domains)
    h   = {
            "Authorization": "Bearer " + i_pass,
            "Content-Type": "application/json",
        }
    check_request   = requests.request("POST", url, headers=h, data=p)
    checked         = check_request.json()
    return checked


def check_for_blocks(checked, destinations):
    '''Use check_domains data to see if blocked and return a list of domain IDs to be removed.'''
    blocked_ids     = []
    blocked_domains = []
    blocked_domains = [i for i in checked if checked[i]["status"] == -1]
    blocked_ids     = [i['id'] for i in destinations if i['destination'] in blocked_domains]
    return blocked_ids


def check_for_nsd(checked, destinations):
    '''Checks if any domains are no longer NSD, returning a list of expired NSD domain IDs to be removed.'''
    expired_ids     = []
    expired_domains = []
    nsd             = "108"  # Investigate API identifies NSD as "108".
    expired_domains = [i for i in checked if nsd not in checked[i]["security_categories"]]
    expired_ids     = [i['id'] for i in destinations if i['destination'] in expired_domains]
    return expired_ids


def combine(block_ids, expired_ids):
    """Combines list of IDs for removal"""
    combined = []
    combined = list(set(block_ids + expired_ids))
    return combined


def remove_domains(open_api_url, combined_ids, open_api_token):
    """Remove Domains from the Umbrella destination list."""
    url = open_api_url + "/remove"
    h = {
        "Authorization": "Bearer " + open_api_token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    p = json.dumps(combined_ids)
    r = requests.request("DELETE", url, headers=h, data=p).json()
    return r


# main
if __name__ == "__main__":
    print("Starting Newly Seen Domains Re-Check Script.")

    # dest_id = 12345678 # Option to Hardset Destination List ID for automation, comment out line 153 )
    destinations    = []  # reset the get request
    delete_request  = []  # reset the delete request
    domains         = []  # reset the domains list.

    # Set these variables in your environment or .bash_profile. Check the README for more information.
    i_pass          = os.environ["INVESTIGATE_TOKEN"]  # Umbrella Investigate API token
    token_url       = os.environ.get('TOKEN_URL') or 'https://api.umbrella.com/auth/v2/token'
    client_id       = os.environ.get('API_KEY')  # Umbrella Open API key
    client_secret   = os.environ.get('API_SECRET')  # Umbrella Open API secret

    # Exit out if the client_id or client_secret is not set
    for var in ["API_SECRET", "API_KEY", "INVESTIGATE_TOKEN"]:
        if os.environ.get(var) == None:
            print("Required environment variable: {} not set".format(var))
            sys.exit(1)

    # Enter destination list ID
    dest_id = ""  # If you would like to hard-set the destination list ID, set it as a string here and comment out the next line.
    dest_id = input( "Enter your NSD Allow Destination List ID (1234567) for NSD recheck: " )
    print("Destination list ID: ", dest_id)

    # Retrieve Open API Token
    token = UmbrellaAPI(token_url, client_id, client_secret)
    open_api_token = token.access_token

    # Generate Open API URL containing destination list ID
    open_api_url = gen_open_api_url(dest_id)

    # Get the list of domains from the destination list then prepare them. Stops script if list of domains is empty.
    destinations = get_domains(open_api_token, open_api_url)
    if len(destinations) == 0:  # Stop Script if the list is empty
        print("No Domains on list. Stopping Script")
    elif len(destinations) > 0:
        """If the list has domains, prepare the list of domain IDs, check each domain ID with the
        Investigate API for security blocks and NSD expiration."""
        print(f"Checking {len(destinations)} Domains")
        checked         = check_domains(destinations)
        block_ids       = check_for_blocks(checked, destinations)
        expired_ids     = check_for_nsd(checked, destinations)
        combined_ids    = combine(block_ids, expired_ids)

        # Remove Each Blocked Domain ID from the destination list, because the block would be allowed.
        if len(block_ids) > 0:
            print(f"{len(block_ids)} domains are blocked.")
            
        # Remove Domains Not Marked NSD from the Destination List because NSD classification has expired.
        if len(expired_ids) > 0:
            print(f"{len(expired_ids)} domains are expired NSDs.")
        if len(combined_ids) > 0:
            print(f"{len(combined_ids)} total domains for removal.")
            removal_response = remove_domains(
                open_api_url, combined_ids, open_api_token
            )
            print("Result : " + str((removal_response["status"])))
            print(
                "Domains remaining for next run : "
                + str(removal_response["data"]["meta"]["destinationCount"])
            )
        else:
            print("No domains to remove.")

    print("Done.")
