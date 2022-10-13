# Legacy Newly Seen Domains Recheck Script

Newly Seen Domains (NSDs) are domains that are new or unknown to the Umbrella DNS resolvers. You can set an Umbrella DNS Policy to block the Newly Seen Domains classification. Blocking NSDs improves the security of your networks.

## Updates ( Oct 5, 2022)

If you're looking to move away from the soon to be EOL Umbrella Management API, please click [here](https://github.com/CiscoDevNet/cloud-security/tree/master/Umbrella/Samples/SOCTools/NSD_Recheck#readme) for the OpenAPI version of this script!

## Maintain an NSD Exemption List

When you choose to block an NSD, you may occasionally need to temporarily allow a domain. Allowed domains are no longer checked for future security classification. Because NSD categorization expires after a few days, you must not leave domains on your NSD allow list. The NSDs Recheck (`legacy_nsd_recheck.py`) script helps you to automate the maintenance of an Umbrella destination list that contains NSDs.

You can use the NSDs Recheck script to maintain an NSD exemption list. The NSD Recheck script integrates with the Umbrella Investigate API and Management API to manage the NSDs in your destination list. 

The NSDs Recheck script:

* Uses the (Legacy) Umbrella Management API to query all domains on a specific destination list.
* Uses the Umbrella Investigate API to check all domains on the destination list.
* Removes any domains blocked by Cisco Umbrella with a security classification of: malware, phishing, command and control.
* Removes all domains except those still classified as NSD.

We recommended that you run the `legacy_nsd_recheck.py` script regularly and automate maintenance of your NSD allow list.

**Note:** You should only run the `legacy_nsd_recheck.py` script on a custom allow list that contains only NSDs. Do not use this script on an allow list containing domains for any other exemption reasons.

## Prerequisites

* You must have a subscription to the Cisco Umbrella Investigate API to use the Umbrella Investigate API.
The Umbrella Investigate API license is an add-on package and is not included in the Umbrella Advantage or Essentials Packages. For more information, see [Umbrella Investigate](https://umbrella.cisco.com/products/umbrella-investigate).
* Python 3.x

## Step 1: Create Umbrella API Keys

* Create an Umbrella Investigate API token. For more information, see [Create Umbrella Investigate API Token.](https://developer.cisco.com/docs/cloud-security/#!investigate-getting-started)
* Create an (Legacy) Umbrella Management API key and secret. For more information, see [Create Umbrella Generate Key and Secret](https://developer.cisco.com/docs/cloud-security/#!getting-started-overview).

## Step 2: Set Environment Variables

In your system, export the environment variables used by the **NSDs Recheck** script.

* `ORG_ID`—Your organization ID. For more information, see [Find Your Organization ID](https://developer.cisco.com/docs/cloud-security/#!getting-started-overview/get-organization-information).
* `MANAGEMENT_KEY`—Your Umbrella Management API key.
* `MANAGEMENT_SECRET`—Your (Legacy) Umbrella Management API secret.
* `INVESTIGATE_TOKEN`—Your Umbrella Investigate API token.

Set up the environment variables for the `legacy_nsd_recheck.py` script in your `.bash_profile`:

```bash
export ORG_ID="insert your Umbrella organization ID"
export MANAGEMENT_KEY="insert your Umbrella Management API key"
export MANAGEMENT_SECRET="insert your Umbrella Management API secret"
export INVESTIGATE_TOKEN="insert your Umbrella Investigate API token"
```

## Step 3: Create an Umbrella Destination List

* You must create an Umbrella destination list with the `access` type of `allow` and `dns`. Add NSDs that you do not want blocked to your allow destination list. For more information, see [Create an Allow list](https://docs.umbrella.com/deployment-umbrella/docs/add-a-new-destination-list).

## Step 4: Run the NSDs Recheck Script

```shell
python3 legacy_nsd_recheck.py
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
