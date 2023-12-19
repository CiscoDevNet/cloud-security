# Newly Seen Domains Recheck Script

Newly Seen Domains (NSDs) are domains that are new or unknown to the Umbrella DNS resolvers. You can set an Umbrella DNS Policy to block the Newly Seen Domains classification. Blocking NSDs improves the security of your networks.

## Maintain a Newly Seen Domain Exemption List

You may need to temporarily allow domains that are categorized as an NSD. Umbrella does not check allowed domains for future security classification. It is important that exemptions are removed so regular Umbrella protection can apply if the domain ever changes. Because NSD categorization typically expires after a few days, we recommend keeping your NSD exemption list trimmed. The NSDs Recheck (`nsd_recheck.py`) script helps you to automate that maintenance for an Umbrella destination list that contains NSDs. The NSD Recheck script integrates with the Umbrella Investigate API and Open API to manage the NSDs in your destination list.

The NSDs Recheck script:

* Uses the Umbrella Open API to query all domains on a specific destination list.
* Uses the Umbrella Investigate API to check all domains on the destination list.
* Removes any domains blocked by Cisco Umbrella with a security classification of malware, phishing, or command and control.
* Removes all other domains except for those still classified as NSD.

We recommended that you run the `nsd_recheck.py` script regularly and automate maintenance of your NSD allow list.

**Note:** You should run the `nsd_recheck.py` script on a custom allow list that contains **only** newly seen domains. Do not use this script on an allow list containing domains for any other exemption reasons.

## Prerequisites

* You must have a subscription to the Cisco Umbrella that includes use of Umbrella Investigate API.
The Umbrella Investigate API license is an add-on package and is not included in the Umbrella Advantage or Essentials Packages. For more information, see [Umbrella Investigate](https://umbrella.cisco.com/products/umbrella-investigate).
* Python 3.x

## Step 1: Create Umbrella API Keys

* Create an Umbrella Investigate API token. For more information, see [Create Umbrella Investigate API Token.](https://developer.cisco.com/docs/cloud-security/#!investigate-getting-started)
* Create an Umbrella Open API key and secret. For more information, see [Create Umbrella Generate Key and Secret](https://developer.cisco.com/docs/cloud-security/#!authentication/create-an-api-key).
* Assign this Umbrella Open API key the permission `policies:read,write`.

## Step 2: Set Environment Variables

In your system, export the environment variables used by the **NSDs Recheck** script.

* `API_KEY`—Your Umbrella Open API key.
* `API_SECRET`—Your Umbrella Open API secret.
* `INVESTIGATE_TOKEN`—Your Umbrella Investigate API token.

Set up the environment variables for the `nsd_recheck.py` script in your `.bash_profile` or Windows Environment Variable:

```bash
export API_KEY="insert your Umbrella Open API key"
export API_SECRET="insert your Umbrella Open API secret"
export INVESTIGATE_TOKEN="insert your Umbrella Investigate API token"
```

## Step 3: Create an Umbrella Destination List

* You must create an Umbrella destination list with the `access` type of `allow` and `dns`. Add NSDs that you do not want blocked to this allow destination list. For more information, see [Create an Allow list](https://docs.umbrella.com/deployment-umbrella/docs/add-a-new-destination-list).

## Step 4: Run the NSDs Recheck Script

```shell
python3 nsd_recheck.py
```

The output is similar to:

```commandline
Starting Newly Seen Domains Re-Check Script.
Enter your destination list ID for NSD recheck: 3174032
Destination list ID:  3174032
Checking 91 Domains
Removing 0 domains that are blocked.
Removing 30 expired NSDs.
Result : {'code': 200, 'text': 'OK'}
Domains remaining for next run : 61
Done.
```
