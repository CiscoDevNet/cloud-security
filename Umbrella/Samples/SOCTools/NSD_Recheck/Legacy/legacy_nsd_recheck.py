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
        h = {"Authorization": "Basic " + management_api_pass, 
            "Content-Type": "application/json"
            }
        p = {}
        r = requests.request("GET", management_api_url, headers=h, data=p).json()
        return r["data"]


    ''' Remove Domains from the Umbrella destination list.'''
    def remove_domains(management_api_url, management_api_pass, combined_ids):
        url = management_api_url + "/remove"
        h = {
            "Authorization": "Basic " + management_api_pass,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        p = json.dumps(combined_ids)
        r = requests.request("DELETE", url, headers=h, data=p).json()
        return r


    def check_domains(ipass, destinations):
        '''Check Categorization and Classification of Domains with the Investigate API'''
        domains = [i['destination'] for i in destinations]
        url = "https://investigate.api.umbrella.com/domains/categorization"
        p = json.dumps(domains)
        h = {
            "Authorization": "Bearer " + ipass,
            "Content-Type": "application/json",
        }
        checked = requests.request("POST", url, headers=h, data=p).json()
        return checked


    def check_for_blocks(checked, destinations):
        '''Use check_domains data to see if blocked and return a list of domain IDs to be removed.'''
        blocked_ids = []
        blocked_domains = []
        blocked_domains = [i for i in checked if checked[i]["status"] == -1]
        blocked_ids = [i['id'] for i in destinations if i['destination'] in blocked_domains]
        return blocked_ids


    def check_for_nsd(checked, destinations):
        '''Checks if any domains are no longer NSD, returning a list of expired NSD domain IDs to be removed.'''
        expired_ids = []
        expired_domains = []
        nsd = "108"  # Investigate API identifies NSD as "108".
        expired_domains = [i for i in checked if nsd not in checked[i]["security_categories"]]
        expired_ids = [i['id'] for i in destinations if i['destination'] in expired_domains]
        return expired_ids

    def combine(block_ids, expired_ids):
        '''Combines list of IDs for removal'''
        combined = []
        combined = list(set(block_ids + expired_ids))
        return combined

    # main
    if __name__ == '__main__':

        print("Starting Newly Seen Domains Re-Check Script.")

        # dest_id = 12345678 # ( Optionally hard-set the Destination List ID for automation, comment out 122 )
        destinations = []  # reset the get request
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
        destinations = get_domains(management_api_pass, management_api_url)

        if len(destinations) == 0:  # Stop Script if the list is empty
            sys.exit("No Domains on list. Stopping Script")
        elif len(destinations) > 0:
            '''If the list has domains, prepare the list of domain IDs, check each domain ID with the
            Investigate API for malware and NSD expiration.'''
            print(f"Checking {len(destinations)} Domains")
            checked = check_domains(ipass, destinations)
            block_ids = check_for_blocks(checked, destinations)
            expired_ids = check_for_nsd(checked, destinations)
            combined_ids = combine(block_ids, expired_ids)
            # Remove Each Blocked Domain ID from the destination list, because the block would be allowed.
            if len(block_ids) > 0:
                print(f"{len(block_ids)} domains are blocked.")
            # Remove Domains Not Marked NSD from the Destination List because NSD classification has expired.
            if len(expired_ids) > 0:
                print(f"{len(expired_ids)} domains are expired NSDs.")
            if len(combined_ids) > 0:
                print(f"{len(combined_ids)} total domains for removal.")
                removal_response = remove_domains(management_api_url, management_api_pass, combined_ids)
                print('Result : ' + str((removal_response['status'])))
                print("Domains remaining for next run : " + str(removal_response['data']['meta']['destinationCount']))
            else:
                print("No domains to remove.")
        print("Done.")