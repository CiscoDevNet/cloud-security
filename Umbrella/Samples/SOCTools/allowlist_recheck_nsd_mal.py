# Check destination list for malware, or expired NSD classification
# If expired or malware, remove from list. 
# Use this on an Allowlist you've created for allowing Newly Seen Domains.
# Requires Umbrella Management API as well as Investigate API access.

# SETUP - libraries and access
import requests, json
import base64
import pandas as pd
import os

## Variables Expected in .bash_profile
mkey = os.environ['mgmtkey'] # management API key
msec = os.environ['mgmtsec'] # management API secret
ipass = os.environ['invpass'] # investigate API token
orgid = os.environ['orgid'] # orgID
destid = input('Please input your destinationlist ID for NSD recheck: ')
gr = []


# Get Domains and Prep them for Re-Check

def gen_murl(orgid, destid):
        '''Gen URL for Destlist on Management API'''
        murl = ( 'https://management.api.umbrella.com/v1/organizations/'
                    + orgid +
                    '/destinationlists/'
                    + destid +
                    '/destinations'
                    )
        return murl
def gen_pass(mkey, msec):
    '''Gen Base64 API Token'''
    mkp = mkey + ':' + msec
    mpass = base64.b64encode(mkp.encode()).decode()
    return mpass

def get_domains(mpass, murl):
    '''GET Request destinations from Umbrella API'''
    headers = {
              'Authorization': 'Basic ' + mpass,
              'Content-Type': 'application/json'
              }
    payload = None
    print('Pulling Domains from Destination List')
    gr = requests.request("GET", murl, headers=headers, data=payload)
    return gr


def gr_prep(gr):
    '''API Response into Dataframe'''
    gr = gr.json()
    gr = gr['data']
    gr = pd.DataFrame.from_dict(gr)
    return gr

def domain_prep(gr):
    '''Sort Domains'''
    domains = []
    domains = gr.destination
    domains = domains.tolist()
    return domains

def rem_domains(domainid):
    '''Remove from Umbrella Destination List '''
    durl = murl + '/remove'
    headers = {
              'Authorization': 'Basic ' + mpass,
              'Accept': 'application/json',  
              'Content-Type': 'application/json'
              }
    payload = json.dumps(domainid)
    dr = requests.request("DELETE", durl, headers=headers, data=payload)
    return dr.text



################################
# Execute Domain Check and Sort

mpass = gen_pass(mkey,msec)
murl = gen_murl(orgid, destid)
gr = get_domains(mpass, murl)
gr = gr_prep(gr)
domains = domain_prep(gr)
# domainids = domainid_prep(gr)
print(f'Prepping {len(domains)} Domains')
    
    
################################

# Check Domains with Investigate API for Malware and NSD Expiration

def check_domains(domains):
    '''Bulk Check Domains on Investigate API'''
    icaturl = "https://investigate.api.umbrella.com/domains/categorization"
    payload = json.dumps(domains)
    
    ih = {
          # 'Authorization': 'Bearer %s' % ipass,
          'Authorization': 'Bearer ' + ipass,
          'Content-Type':'application/json'
          }

    ir = requests.request("POST", icaturl, headers=ih, data=payload)
    checked = ir.json()
    return checked
    
    
def check_for_malware(checked):
    '''Check if Domains are Malware'''
    blockeddomains = []
    for eachdomain in checked:
        if checked.get(eachdomain)['status'] == -1:
            blockeddomains.append(eachdomain)
    mdf = gr[gr['destination'].isin(blockeddomains)]
    mids = []
    mids = mdf.id
    mids = mids.tolist()
    return(mids)

def check_for_nsd(checked):
    '''Check if Domains are NSD'''
    expired = []
    nsd = '108'
    # check each domain in api response is NOT NSD
    for each in checked:
        if nsd not in checked.get(each)['security_categories']:
            expired.append(each)
    # compare expired to main list, store just ids
    expireddf = gr[gr['destination'].isin(expired)]
    expiredids = []
    expiredids = expireddf.id
    expiredids = expiredids.tolist()
    return(expiredids)
    
################################

checked = check_domains(domains)
mids = check_for_malware(checked)
expiredids = check_for_nsd(checked)

print(f'Removing {len(mids)} Domains marked malware.')
if len(mids) > 0:
    for eachmids in mids:
        rem_domains(mids)

print(f'Removing {len(expiredids)} Expired NSDs.')
if len(expiredids) > 0:
    for eachid in expiredids:
        rem_domains(expiredids)

################################
print('Done.')
