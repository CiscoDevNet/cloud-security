# Cisco Secure Access Python SDK

A Python SDK for interacting with Cisco Secure Access APIs.

## Requirements

- Python 3.9 or higher
- Valid API credentials

## Installation

### Prerequisites

First, install the required dependencies:

```sh
pip install -r requirements.txt
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```

## Configuration

Set up your API credentials by using environment variables:

### Environment Variables

```bash
export CLIENT_ID="your_client_id"
export CLIENT_SECRET="your_client_secret"
```

## Examples

The `examples/` folder contains sample scripts demonstrating various use cases with the Cisco Secure Access SDK:

### Access Rule Backup and Restore
Backup and restore access rules
```sh
python examples/access_rule_backup_restore.py -h
usage: access_rule_backup_restore.py [-h] -t {backup,restore} [-o OFFSET] [-l LIMIT] [-r RULES [RULES ...]]

Utility to backup and restore access rules

options:
  -h, --help            show this help message and exit
  -t {backup,restore}, --type {backup,restore}
                        Type of the operation to be performed i.e. either backup or restore the access rules.
  -o OFFSET, --offset OFFSET
                        Starting offset to fetch the access rules
  -l LIMIT, --limit LIMIT
                        limit to fetch the access rules in a call
  -r RULES [RULES ...], --rules RULES [RULES ...]
                        list of rule id's to filter the Access Rules
```

### Roaming Computers Backup
Backup roaming computer configurations
```sh
python examples/roaming_computers_backup.py -h
usage: roaming_computers_backup.py [-h] --operation {backup,filter,complex-filter,analyze} [--page-size PAGE_SIZE] [--name NAME]
                                   [--status STATUS] [--swg-status SWG_STATUS] [--last-sync-before LAST_SYNC_BEFORE]
                                   [--last-sync-after LAST_SYNC_AFTER] [--filter-key FILTER_KEY] [--filter-value FILTER_VALUE]
                                   [--filter-expression FILTER_EXPRESSION] [--backup-file BACKUP_FILE] [--apply-simple-filter]
                                   [--apply-complex-filter]

Utility to backup roaming computers and apply filters

options:
  -h, --help            show this help message and exit
  --operation {backup,filter,complex-filter,analyze}
                        Operation to perform
  --page-size PAGE_SIZE
                        Number of records per page (max: 100)
  --name NAME           Filter by roaming computer name
  --status STATUS       Filter by DNS-layer security status
  --swg-status SWG_STATUS
                        Filter by Internet security (SWG) status
  --last-sync-before LAST_SYNC_BEFORE
                        Filter by last sync before this date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
  --last-sync-after LAST_SYNC_AFTER
                        Filter by last sync after this date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
  --filter-key FILTER_KEY
                        Key to filter on (supports dot notation for nested keys)
  --filter-value FILTER_VALUE
                        Value to match for filtering
  --filter-expression FILTER_EXPRESSION
                        Complex filter expression with logical operators and time functions
  --backup-file BACKUP_FILE
                        Custom backup file name
  --apply-simple-filter
                        Apply simple filter immediately after backup
  --apply-complex-filter
                        Apply complex filter immediately after backup
```

### Destination Lists Manager
Manage destination lists
```sh
python examples/destination_lists_manager.py -h
usage: destination_list_manager.py [-h] {destination-lists,destinations} ...

Cisco Secure Access Destination Management Tool

positional arguments:
  {destination-lists,destinations}
                        Available commands
    destination-lists   Manage destination lists
    destinations        Manage destinations

options:
  -h, --help            show this help message and exit
```

### Key Admin API Management
Manage API keys and administrative functions
```sh
python examples/key_admin_api.py
```