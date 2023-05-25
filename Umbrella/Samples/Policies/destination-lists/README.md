# Manage Your Cisco Umbrella Destination Lists

Learn how to use the Umbrella Destination Lists API to programmatically manage your destination lists and allow or block destinations—domains, IPs, and URLs. The Umbrella Destination Lists API follows RESTful principles and uses JSON for requests and responses.

## Use Cases

* [Get Destination Lists Summary Information and Export to CSV File](#get-summary-information)
* [Get Destinations and Export to CSV File](#get-destinations-and-export)
* [Import Destinations from a CSV File and Add to Destination List](#import-destinations-and-add)
* [Import Destinations from a CSV File and Remove from Destination List](#import-destinations-and-remove)

## Prerequisites

* A valid Cisco Umbrella subscription
* Full admin access to the Umbrella dashboard
* Python 3.x
* Access to the Python package manager `pip`

## Before You Begin

* Create an Umbrella API key configured with access to the Umbrella Destination Lists `policies.destinations:read` and `policies.destinations:write` API key scopes. For more information, see [Umbrella Authentication](https://developer.cisco.com/docs/cloud-security/#!authentication).
* Install the Python libraries required by the sample scripts.

  ```shell
   pip install -r requirements.txt
  ```

<a name="set-up-sample-directory"></a>

### Set Up Sample Directory and Destination Lists Library

The Umbrella Destination Lists library provides the functions to manage your Umbrella API credentials and token generation API request session, and support the destination lists tasks.

1. Create a destination lists sample directory to hold the Umbrella Destination Lists library and the sample scripts. The scripts generate directories to contain your exported destination list and destination data.
1. Export the location of your destination lists sample directory to the `CISCO_SAMPLE_DIR` environment variable.

   ```shell
   export CISCO_SAMPLE_DIR=<substitute-your-local-sample-directory-name>
   ```
1. Copy the `umbrella` directory and its contents from this repository location to the `$CISCO_SAMPLE_DIR` on your local system.
   * The `umbrella` directory contains `__init__.py` and `destination_lists.py`.

<a name="get-summary-information"></a>

## Get Destination Lists Summary Information and Export to CSV File

The `get_summary_info_destination_lists.py` script gets the destinations lists in your organization from Umbrella using the Umbrella Destination Lists API and exports the summary information to a CSV file.

### Set Up Environment Variables

Set up the script's required environment variables on your local system:

* `API_KEY`—Umbrella API key created in the Umbrella dashboard.
* `API_SECRET`—Umbrella API secret created in the Umbrella dashboard.

**Note:** You must set the `CISCO_SAMPLE_DIR` environment variable. See [Set Up Sample Directory and Destination Lists Library](#set-up-sample-directory).

### Run `get_summary_info_destination_lists.py`

```shell
  python3 get_summary_info_destination_lists.py
```

<a name="get-destinations-and-export"></a>

## Get Destinations and Export to CSV File

The `get_destinations_in_destination_lists.py` script gets the destinations lists in your organization from Umbrella using the Umbrella Destination Lists API and exports the destinations in each destination list to a CSV file.

### Set Up Environment Variables

Set up the script's required environment variables on your local system:

* `API_KEY`—Umbrella API key created in the Umbrella dashboard.
* `API_SECRET`—Umbrella API secret created in the Umbrella dashboard.

**Note:** You must set the `CISCO_SAMPLE_DIR` environment variable. See [Set Up Sample Directory and Destination Lists Library](#set-up-sample-directory).

### Run `get_destinations_in_destination_lists.py`

```shell
  python3 get_destinations_in_destination_lists.py
```

<a name="import-destinations-and-add"></a>

## Import Destinations from CSV File and Add to Destination List

The `add_destinations_in_destination_lists.py` script reads the destination data from a local CSV file and adds the destinations to Umbrella using the Umbrella Destination Lists API.

### Set Up Environment Variables

Set up the script's required environment variables on your local system:

* `API_KEY`—Umbrella API key created in the Umbrella dashboard.
* `API_SECRET`—Umbrella API secret created in the Umbrella dashboard.
* `UMBRELLA_DL_ID`—An Umbrella Destination List ID.
* `DESTINATIONS_FILENAME`—A filename of one of your CSV files that contains the destination data.

**Note:** You must set the `CISCO_SAMPLE_DIR` environment variable. See [Set Up Sample Directory and Destination Lists Library](#set-up-sample-directory).

### Run `add_destinations_in_destination_lists.py`

```shell
  python3 add_destinations_in_destination_lists.py
```

<a name="import-destinations-and-remove"></a>

## Import Destinations from CSV File and Remove from Destination List

The `delete_destinations_in_destination_lists.py` script reads the destination data from a local CSV file and removes the destinations from an Umbrella destination list using the Umbrella Destination Lists API.

### Set Up Environment Variables

Set up the script's required environment variables on your local system:

* `API_KEY`—Umbrella API key created in the Umbrella dashboard.
* `API_SECRET`—Umbrella API secret created in the Umbrella dashboard.
* `UMBRELLA_DL_ID`—An Umbrella Destination List ID.
* `DESTINATIONS_FILENAME`—A filename of one of your CSV files that contains the destination data.

**Note:** You must set the `CISCO_SAMPLE_DIR` environment variable. See [Set Up Sample Directory and Destination Lists Library](#set-up-sample-directory).

### Run `delete_destinations_in_destination_lists.py`

```shell
  python3 delete_destinations_in_destination_lists.py
```

## Troubleshooting

* Check that your Umbrella API key has not expired.
* Check that your Umbrella API key is configured with the `policies.destinations:read` and `policies.destinations:write` Umbrella Destination Lists key scopes.
* Check that you can use your Umbrella API key to request a Bearer token from the Umbrella Token Authorization API. The Umbrella Destination Lists library supports the Umbrella API token generation lifecycle.
* Check that you have permission to write to the directory where you installed the Umbrella Destination Lists library.
* Check that you met the prerequisites to run the scripts and that you set the required environment variables.

## Copyright

Copyright (c) 2023 Cisco and/or its affiliates.
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
