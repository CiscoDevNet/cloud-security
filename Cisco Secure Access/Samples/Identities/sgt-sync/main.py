"""
Copyright (c) 2025 Cisco and/or its affiliates.
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
"""

# main.py
import sys
import argparse
from sgt_sync.config import Config
from sgt_sync.logging_config import setup_logging
from sgt_sync.clients.ise_client import IseClient, IseClientError
from sgt_sync.clients.secure_access_client import (
    SecureAccessClient,
    SecureAccessClientError,
)
from sgt_sync.synchronizer import SgtSynchronizer
from sgt_sync.models.sgt import SecurityGroupTag

# Configure logging for the entire application
logger = setup_logging()


def print_sgts(title: str, sgts: list[SecurityGroupTag]):
    """Helper function to print a list of SGTs in a readable format."""
    if not sgts:
        logger.info(f"No {title} SGTs found.")
        return

    logger.info(f"\n--- {title} ({len(sgts)} SGTs) ---")
    for sgt in sgts:
        logger.info(
            f"  Key: {sgt.key}, Label: '{sgt.label}', Tag ID: {sgt.tag_id}, Status: {sgt.status}"
        )
    logger.info(f"--- End of {title} ---")


def main():
    """Main function to run the SGT synchronization or perform CLI actions."""
    parser = argparse.ArgumentParser(
        description="Synchronize Security Group Tags from ISE to Cisco Secure Access, or perform diagnostic actions."
    )

    # Create a mutually exclusive group for commands that should not run together
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--list-ise",
        action="store_true",
        help="List all Security Group Tags found in Cisco Identity Services Engine (ISE).",
    )
    group.add_argument(
        "--list-sa",
        action="store_true",
        help="List all Security Group Tags found in Cisco Secure Access (active and inactive).",
    )
    group.add_argument(
        "--list-sa-inactive",
        action="store_true",
        help="List only the INACTIVE Security Group Tags found in Cisco Secure Access.",
    )
    group.add_argument(
        "--diff-only",
        action="store_true",
        help="Show the difference between ISE and Secure Access SGTs without performing any synchronization (no changes applied).",
    )
    args = parser.parse_args()

    try:
        # Load and validate configuration
        Config.validate()
        config = Config()
        logger.info("Configuration loaded and validated.")

        # Initialize clients
        ise_client = IseClient(config)
        sa_client = SecureAccessClient(config)
        logger.info("API clients initialized.")

        # Handle CLI arguments
        if args.list_ise:
            logger.info("Fetching SGTs from ISE...")
            ise_sgts = ise_client.get_sgts()
            print_sgts("ISE SGTs", ise_sgts)
            sys.exit(0)

        elif args.list_sa:
            logger.info("Fetching SGTs from Secure Access (all statuses)...")
            sa_sgts = sa_client.get_sgts()
            print_sgts("Secure Access SGTs (All)", sa_sgts)
            sys.exit(0)

        elif args.list_sa_inactive:
            logger.info("Fetching INACTIVE SGTs from Secure Access...")
            all_sa_sgts = sa_client.get_sgts()
            inactive_sa_sgts = [sgt for sgt in all_sa_sgts if sgt.status == "inactive"]
            print_sgts("Secure Access SGTs (Inactive)", inactive_sa_sgts)
            sys.exit(0)

        elif args.diff_only:
            logger.info(
                "Performing SGT difference analysis (diff-only mode). No changes will be applied."
            )
            ise_sgts = ise_client.get_sgts()
            sa_sgts = sa_client.get_sgts()

            synchronizer = SgtSynchronizer(ise_client, sa_client)
            sgts_to_add_update, sgts_to_mark_inactive = synchronizer.diff_sgts(
                ise_sgts, sa_sgts
            )

            print_sgts(
                "SGTs to Add/Update in Secure Access (would be added/modified)",
                sgts_to_add_update,
            )
            print_sgts(
                "SGTs to Mark Inactive in Secure Access (would be set to inactive)",
                sgts_to_mark_inactive,
            )
            sys.exit(0)

        # Full synchronization if no specific CLI arguments are provided
        else:
            logger.info(
                "No specific CLI arguments provided. Proceeding with full SGT synchronization."
            )
            synchronizer = SgtSynchronizer(ise_client, sa_client)
            synchronizer.sync_sgts()
            logger.info("SGT synchronization finished successfully.")

    except ValueError as e:
        logger.critical(f"Configuration Error: {e}")
        sys.exit(1)
    except (IseClientError, SecureAccessClientError) as e:
        logger.critical(f"API Client Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
