# Newly Seen Domains (NSD) Re-Check Script. Used to maintain an allow list only used for NSD temporary exemptions.

# Library Imports
import requests, json
import base64
import pandas as pd
import os

# These variables are expected in the .bash_profile. How-To Guide in README.md
print("Starting Newly Seen Domains Re-Check Script.")
mkey = os.environ["MANAGEMENT_KEY"]  # Umbrella Management API key
msec = os.environ["MANAGEMENT_SECRET"]  # Umbrella Management API secret
ipass = os.environ["INVESTIGATE_TOKEN"]  # Umbrella Investigate API token
orgid = os.environ["ORG_ID"]  # orgID

destid = input(
    "Please input your destination list ID for NSD recheck: "
)  # Asks for DestinationlistID

# destid = 12345678 # ( option for automation ) Destination list ID here instead of input in line 16-18.
gr = []  # reset the get request
dr = []  # reset the delete request
domains = []  # reset the domains list.


# Generates URL for Management API, including orgid and destid
def gen_murl(orgid, destid):
    """Gen URL for Destlist on Management API"""
    murl = (
        "https://management.api.umbrella.com/v1/organizations/"
        + orgid
        + "/destinationlists/"
        + destid
        + "/destinations"
    )
    return murl


# Generates base64 encoded key and secret for passing credentials to the management api
def gen_pass(mkey, msec):
    """Gen Base64 API Token"""
    mkp = mkey + ":" + msec
    mpass = base64.b64encode(mkp.encode()).decode()
    return mpass


# GET Request for all domains from the specified NSD Destination List
def get_domains(mpass, murl):
    """GET Request destinations from Umbrella API"""
    headers = {"Authorization": "Basic " + mpass, "Content-Type": "application/json"}
    payload = None
    print("Getting Domains from Destination List")
    # get request
    gr = requests.request("GET", murl, headers=headers, data=payload)
    return gr


# Cleans up the Response from get_domains
def gr_prep(gr):
    """API Response into Dataframe"""
    gr = gr.json()
    gr = gr["data"]
    gr = pd.DataFrame.from_dict(gr)
    return gr


# Creates a list of domains that should reviewed by Investigate API
def domain_prep(gr):
    """Sort Domains"""
    domains = []
    domains = gr.destination
    domains = domains.tolist()
    return domains


# Removes Domains from the Destination list which are checked by check_for_nsd and check_for_malware
def rem_domains(domainid):
    """Remove from Umbrella Destination List"""
    durl = murl + "/remove"
    headers = {
        "Authorization": "Basic " + mpass,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = json.dumps(domainid)
    # delete request
    dr = requests.request("DELETE", durl, headers=headers, data=payload)
    return dr.text


# Check Categorization and Classification of Domains with the Investigate API
def check_domains(domains):
    """Bulk Check Domains on Investigate API"""
    icaturl = "https://investigate.api.umbrella.com/domains/categorization"
    payload = json.dumps(domains)

    ih = {
        # 'Authorization': 'Bearer %s' % ipass,
        "Authorization": "Bearer " + ipass,
        "Content-Type": "application/json",
    }
    #investigate request for bulk domain list categorization
    ir = requests.request("POST", icaturl, headers=ih, data=payload)
    checked = ir.json()
    return checked


# Checks Results from check_domains to see if Malware returning a list of domains to be removed.
def check_for_malware(checked):
    """Check if Domains are Malware"""
    blockeddomains = []
    for eachdomain in checked:
        if checked.get(eachdomain)["status"] == -1:
            blockeddomains.append(eachdomain)
    mdf = gr[gr["destination"].isin(blockeddomains)]
    mids = []
    mids = mdf.id
    mids = mids.tolist()
    return mids


# Checks if any domains are no longer NSD, returning a list of expired NSD domains to be removed.
def check_for_nsd(checked):
    """Check if Domains are NSD"""
    expired = []
    nsd = "108"
    # check each domain in api response is NOT NSD
    for each in checked:
        if nsd not in checked.get(each)["security_categories"]:
            expired.append(each)
    # compare expired to main list, store just ids
    expireddf = gr[gr["destination"].isin(expired)]
    expiredids = []
    expiredids = expireddf.id
    expiredids = expiredids.tolist()
    return expiredids

# generate credentials and a Management API URL cotaining orgid and destination list id
mpass = gen_pass(mkey, msec)
murl = gen_murl(orgid, destid)

# Gets the list of domains for checking from the destination list then prepares them. Stops script if list is empty.
gr = get_domains(mpass, murl)
gr = gr_prep(gr)
if len(gr) == 0:  # Stop Script if the list is empty
    print("No Domains on list. Stopping Script")

# If List has domains, prepare the list of domain IDs, check each with Investigate for Malware and NSD Expiration.
elif len(gr) > 0:
    domains = domain_prep(gr)
    print(f"Checking {len(domains)} Domains")
    checked = check_domains(domains)
    mids = check_for_malware(checked)
    expiredids = check_for_nsd(checked)

    # Remove Each Malware Domain ID from the destination List ( they are allowed! )
    print(f"Removing {len(mids)} Domains marked malware.")
    if len(mids) > 0:
        for eachmids in mids:
            rem_domains(mids)
    # Remove Domains Not Marked NSD from the Destination List because NSD classification has expired.
    print(f"Removing {len(expiredids)} Expired NSDs.")
    if len(expiredids) > 0:
        for eachid in expiredids:
            rem_domains(expiredids)
    print(f"{len(domains) - len(expiredids) - len(mids)} NSD domains remain for next run.")

print("Done.")
