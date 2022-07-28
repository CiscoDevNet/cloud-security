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


# GET Request for all domains from the specified NSD Destination List
def get_domains(management_api_pass, management_api_url):
    """GET Request destinations from Umbrella API"""
    headers = {"Authorization": "Basic " + management_api_pass, "Content-Type": "application/json"}
    payload = None
    print("Getting Domains from Destination List")
    # get request
    gr = requests.request("GET", management_api_url, headers=headers, data=payload)

    if gr:
        gr = pd.DataFrame.from_dict(gr.json()['data'])

    return gr


# Creates a list of domains that should reviewed by Investigate API
def domain_prep(gr):
    """Sort Domains"""
    domains = []
    domains = gr.destination
    domains = domains.tolist()
    return domains


''' Remove Domains from the Umbrella destination list.
    Domains were checked by check_for_nsd() and check_for_malware() functions. '''


def remove_domains(domain_id):
    deleteurl = management_api_url + "/remove"
    headers = {
        "Authorization": "Basic " + management_api_pass,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = json.dumps(domain_id)
    # delete request
    dr = requests.request("DELETE", deleteurl, headers=headers, data=payload)
    return dr.text


# Check Categorization and Classification of Domains with the Investigate API
def check_domains(domains):
    """Bulk Check Domains on Investigate API"""
    investigateurl = "https://investigate.api.umbrella.com/domains/categorization"
    payload = json.dumps(domains)

    ih = {
        # 'Authorization': 'Bearer %s' % ipass,
        "Authorization": "Bearer " + ipass,
        "Content-Type": "application/json",
    }
    # investigate request for bulk domain list categorization
    ir = requests.request("POST", investigateurl, headers=ih, data=payload)
    checked = ir.json()
    return checked


# Checks Results from check_domains to see if Malware returning a list of domains to be removed.
def check_for_malware(checked):
    """Check if Domains are Malware"""
    blockeddomains = []
    for d in checked:
        if checked.get(d)["status"] == -1:
            blockeddomains.append(d)
    # use dataframe to filter gr to just blocked domains in mdf
    mdf = gr[gr["destination"].isin(blockeddomains)]
    mids = []
    # filter just the id's for the domains that are blocked because domains are deleted by ID.
    mids = mdf.id
    mids = mids.tolist()
    return mids


# Checks if any domains are no longer NSD, returning a list of expired NSD domains to be removed.
def check_for_nsd(checked):
    """Check if Domains are NSD"""
    expired = []
    nsd = "108"
    # check each domain in api response is NOT NSD
    for d in checked:
        if nsd not in checked.get(d)["security_categories"]:
            expired.append(d)
    # compare expired to main list, store just ids
    expireddf = gr[gr["destination"].isin(expired)]
    expiredids = []
    expiredids = expireddf.id
    expiredids = expiredids.tolist()
    return expiredids


# main
if __name__ == '__main__':

    print("Starting Newly Seen Domains Re-Check Script.")

    # dest_id = 12345678 # ( option for automation ) Destination list ID
    gr = []  # reset the get request
    dr = []  # reset the delete request
    domains = []  # reset the domains list.

    # Set these variables in your environment or .bash_profile. Check the README for more information.
    mkey = os.environ["MANAGEMENT_KEY"]  # Umbrella Management API key
    msec = os.environ["MANAGEMENT_SECRET"]  # Umbrella Management API secret
    ipass = os.environ["INVESTIGATE_TOKEN"]  # Umbrella Investigate API token
    orgid = os.environ["ORG_ID"]  # orgID

    # Enter destination list ID
    dest_id = input(
        "Enter your destination list ID for NSD recheck: "
    )

    print("Destination list ID: ", dest_id)

    # generate credentials and a Management API URL containing orgId and destination list ID
    management_api_pass = ""
    management_api_pass = gen_credentials(mkey, msec)
    management_api_url = ""
    management_api_url = gen_management_api_url(orgid, dest_id)

    # Get the list of domains from the destination list then prepare them. Stops script if list of domains is empty.
    gr = get_domains(management_api_pass, management_api_url)
    # gr = gr_prep(gr)

    if len(gr) == 0:  # Stop Script if the list is empty
        sys.exit("No Domains on list. Stopping Script")
    elif len(gr) > 0:
        # If list of domains, prepare the list of domain IDs, check each domain ID with the
        # Investigate API for malware and NSD expiration.
        domains = domain_prep(gr)
        print(f"Checking {len(domains)} Domains")
        checked = check_domains(domains)
        mids = check_for_malware(checked)
        expired_ids = check_for_nsd(checked)

        # Remove Each Malware Domain ID from the destination List ( Malware was allowed )
        print(f"Removing {len(mids)} Domains marked malware.")
        if len(mids) > 0:
            remove_domains(mids)
        # Remove Domains Not Marked NSD from the Destination List because NSD classification has expired.
        print(f"Removing {len(expired_ids)} Expired NSDs.")
        if len(expired_ids) > 0:
            remove_domains(expired_ids)

    print(f"{len(domains) - len(expired_ids) - len(mids)} domains remain for next run.")
    print("Done.")
