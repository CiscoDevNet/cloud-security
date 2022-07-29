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

''' Newly Seen Domains (NSD) recheck script (nsd_recheck.py).
    Used to maintain an allow list used only for NSD temporary exemptions.
'''

import requests, json
import base64
import pandas as pd
import os
import sys

''' Generates URL for Management API, including org_id and dest_id '''
def gen_management_api_url(org_id, dest_id):
    management_api_url = (
            "https://management.api.umbrella.com/v1/organizations/"
            + org_id
            + "/destinationlists/"
            + dest_id
            + "/destinations"
    )
    return management_api_url


''' Generates base64 encoded key and secret for passing credentials to the management api '''
def gen_credentials(mkey, msec):
    """Gen Base64 API Token"""
    mkp = mkey + ":" + msec
    management_api_pass = base64.b64encode(mkp.encode()).decode()
    return management_api_pass

'''GET Request destinations from Umbrella API'''
def get_domains(management_api_pass, management_api_url):
    headers = {"Authorization": "Basic " + management_api_pass, "Content-Type": "application/json"}
    payload = None
    print("Getting Domains from Destination List")
    get_request = requests.request("GET", management_api_url, headers=headers, data=payload)
    if get_request:
        get_request = pd.DataFrame.from_dict(get_request.json()['data'])
    return get_request


''' Remove Domains from the Umbrella destination list.
    Domains are checked by check_for_nsd() and check_for_blocks() functions. '''
def remove_domains(domain_id):
    deleteurl = management_api_url + "/remove"
    headers = {
        "Authorization": "Basic " + management_api_pass,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = json.dumps(domain_id)
    delete_request = requests.request("DELETE", deleteurl, headers=headers, data=payload)
    return delete_request.text


'''Check Categorization and Classification of Domains with the Investigate API'''
def check_domains(domains):
    investigate_url = "https://investigate.api.umbrella.com/domains/categorization"
    payload = json.dumps(domains)
    investigate_headers = {
        "Authorization": "Bearer " + ipass,
        "Content-Type": "application/json",
    }
    check_request = requests.request("POST", investigate_url, headers=investigate_headers, data=payload)
    checked = check_request.json()
    return checked


'''Use check_domains data to see if blocked and return a list of domain IDs to be removed.'''
def check_for_blocks(checked):
    blocked_domains = []
    for d in checked:
        if checked.get(d)["status"] == -1:
            blocked_domains.append(d)
    block_df = get_request[get_request["destination"].isin(blocked_domains)]
    block_ids = []
    block_ids = block_df.id
    block_ids = block_ids.tolist()
    return block_ids


'''Checks if any domains are no longer NSD, returning a list of expired NSD domain IDs to be removed.'''
def check_for_nsd(checked):
    expired = []
    nsd = "108" # 108 is the Newly Seen Domains Number returned from the API.
    for d in checked:
        if nsd not in checked.get(d)["security_categories"]:
            expired.append(d)
    expired_df = get_request[get_request["destination"].isin(expired)]
    expired_ids = []
    expired_ids = expired_df.id
    expired_ids = expired_ids.tolist()
    return expired_ids


# main
if __name__ == '__main__':

    print("Starting Newly Seen Domains Re-Check Script.")

    # dest_id = 12345678 # ( Optionally hard-set the Destination List ID for automation, comment out 140-143 )
    get_request = []  # reset the get request
    delete_request = []  # reset the delete request
    domains = []  # reset the domains list.

    # Set these variables in your environment or .bash_profile. Check the README for more information.
    mkey = os.environ["MANAGEMENT_KEY"]  # Umbrella Management API key
    msec = os.environ["MANAGEMENT_SECRET"]  # Umbrella Management API secret
    ipass = os.environ["INVESTIGATE_TOKEN"]  # Umbrella Investigate API token
    orgid = os.environ["ORG_ID"]  # orgID

    # Enter destination list ID
    dest_id = input("Enter your destination list ID for NSD recheck: ")
    print("Destination list ID: ", dest_id)

    # generate credentials and a Management API URL containing orgId and destination list ID
    management_api_pass = ""
    management_api_pass = gen_credentials(mkey, msec)
    management_api_url = ""
    management_api_url = gen_management_api_url(orgid, dest_id)

    # Get the list of domains from the destination list then prepare them. Stops script if list of domains is empty.
    get_request = get_domains(management_api_pass, management_api_url)

    if len(get_request) == 0:  # Stop Script if the list is empty
        sys.exit("No Domains on list. Stopping Script")
    elif len(get_request) > 0:
        '''If the list has domains, prepare the list of domain IDs, check each domain ID with the
        Investigate API for malware and NSD expiration.'''
        domains = get_request.destination
        domains = domains.tolist()
        print(f"Checking {len(domains)} Domains")
        checked = check_domains(domains)
        block_ids = check_for_blocks(checked)
        expired_ids = check_for_nsd(checked)

        # Remove Each Malware Domain ID from the destination List ( Malware was allowed )
        print(f"Removing {len(block_ids)} Domains marked malware.")
        if len(block_ids) > 0:
            remove_domains(block_ids)
        # Remove Domains Not Marked NSD from the Destination List because NSD classification has expired.
        print(f"Removing {len(expired_ids)} Expired NSDs.")
        if len(expired_ids) > 0:
            remove_domains(expired_ids)

    print(f"{len(domains) - len(expired_ids) - len(block_ids)} domains remain for next run.")
    print("Done.")