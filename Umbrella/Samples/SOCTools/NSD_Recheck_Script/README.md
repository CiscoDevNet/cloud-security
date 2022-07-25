## Newly Seen Domains Re-check Script

---

Newly Seen Domains (NSD) provides Umbrella DNS customers with the ability to block domains that are new to Umbrella's 
resolvers. The security benefits of blocking new and unknown cannot be overstated. Using Umbrella's
`Investigate API` and `Management API` we hope to help get you **started** with maintaining an NSD exemption list.

When opting to block NSD, you will occasionally need to temporarily allow a domain. Allowed domains are no longer 
checked for future security classification. Because NSD categorization expires after a few days, domains should not be 
left on this allow list. This script attempts to automate the maintenance of an NSD allow-list.

- Uses `Management API` to query all domains on a specific destination list.
- Checks all domains on the destination list against the Umbrella Investigate API.
- **Removes** any domains blocked by Cisco Umbrella for Security Classification ( malware, phishing, command and control )
- **Removes** all domains except those still classified as NSD.

Customers are recommended to run this script regularly and automate maintenance of their NSD Allow list.

**Note:** You should only use this on a custom allow-list that allows only Newly Seen Domains. Do not use this script on
an allow list containing domains for any other exemption reasons.

---
### Prerequisites and Docs

- [Create an Allow list](https://docs.umbrella.com/deployment-umbrella/docs/add-a-new-destination-list) that is **only** used for Newly Seen Domains exemptions.
- Umbrella Management API `Key:Secret` stored in `.bash_profile`. [Getting Started with the Umbrella Management API.](https://developer.cisco.com/docs/cloud-security/#!getting-started-overview) 
- An Umbrella `Investigate API Token` stored in `.bash_profile` [Getting Started with the Umbrella Investigate API.](https://developer.cisco.com/docs/cloud-security/#!investigate-getting-started)
- Investigate API usually requires a separate Investigate License which includes access to the Investigate API.
- While other credential storage options will work, if you are new to using credentials in a .bash_profile here is a [how-to guide](https://medium.com/geekculture/how-to-protect-your-credentials-using-environment-variables-with-python-25e6cb4d135c)  to get you started.
- Umbrella [Dashboard Org ID](https://developer.cisco.com/docs/cloud-security/#!getting-started-overview/get-organization-information) number.
- Umbrella NSD Allow List [Destination ID](https://developer.cisco.com/docs/cloud-security/#!destination-lists/get-destination-lists) number.
- Python 3.9+
