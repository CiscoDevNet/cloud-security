# sgt_sync/synchronizer.py
import logging
from typing import List, Tuple, Dict

from .clients.ise_client import IseClient
from .clients.secure_access_client import SecureAccessClient
from .models.sgt import SecurityGroupTag

logger = logging.getLogger("sgt_sync.synchronizer")


class SgtSynchronizer:
    """
    Orchestrates the synchronization of Security Group Tags from ISE (source of truth)
    to Cisco Secure Access.
    """

    def __init__(self, ise_client: IseClient, sa_client: SecureAccessClient):
        self.ise_client = ise_client
        self.sa_client = sa_client

    def diff_sgts(
        self, ise_sgts: List[SecurityGroupTag], sa_sgts: List[SecurityGroupTag]
    ) -> Tuple[List[SecurityGroupTag], List[SecurityGroupTag]]:
        """
        Public method to compare SGTs from ISE and Secure Access to determine
        necessary synchronization actions without performing them.

        Returns:
            tuple[list, list]:
                1. SGTs to be added or updated in Secure Access.
                2. SGTs to be marked 'inactive' in Secure Access (no longer exist in ISE).
        """
        logger.info("Diffing SGTs between ISE and Secure Access...")
        sgts_to_add_update: List[SecurityGroupTag] = []
        sgts_to_mark_inactive: List[SecurityGroupTag] = []

        sa_sgts_map: Dict[str, SecurityGroupTag] = {sgt.key: sgt for sgt in sa_sgts}
        ise_keys_set = {sgt.key for sgt in ise_sgts}

        # Identify SGTs to Add or Update in Secure Access
        for ise_sgt in ise_sgts:
            sa_sgt = sa_sgts_map.get(ise_sgt.key)

            if sa_sgt:
                # SGT exists in Secure Access, check if it needs updating
                if (
                    ise_sgt.label != sa_sgt.label
                    or ise_sgt.tag_id != sa_sgt.tag_id
                    or ise_sgt.status != sa_sgt.status
                ):
                    logger.info(
                        f"SGT '{ise_sgt.label}' (key: {ise_sgt.key}) in SA has incorrect values. Marking for update."
                    )
                    logger.debug(
                        f"ISE: Label='{ise_sgt.label}', TagId={ise_sgt.tag_id}, Status='{ise_sgt.status}'"
                    )
                    logger.debug(
                        f"SA : Label='{sa_sgt.label}', TagId={sa_sgt.tag_id}, Status='{sa_sgt.status}'"
                    )
                    sgts_to_add_update.append(ise_sgt)
                else:
                    logger.debug(
                        f"SGT '{ise_sgt.label}' (key: {ise_sgt.key}) is already up-to-date in Secure Access."
                    )
            else:
                # SGT does not exist in Secure Access, mark for addition
                logger.info(
                    f"SGT '{ise_sgt.label}' (key: {ise_sgt.key}) not found in Secure Access. Marking for addition."
                )
                sgts_to_add_update.append(ise_sgt)

        # Identify SGTs to Mark Inactive (exist in SA but not in ISE)
        for sa_key, sa_sgt in sa_sgts_map.items():
            if sa_key not in ise_keys_set:
                # Only mark for inactive if its current status is 'active' to avoid redundant updates
                if sa_sgt.status == "active":
                    logger.info(
                        f"SGT '{sa_sgt.label}' (key: {sa_key}) exists in Secure Access but not in ISE. Marking for 'inactive'."
                    )

                    # Create a new SGT object with 'inactive' status for deletion
                    sgts_to_mark_inactive.append(
                        SecurityGroupTag(
                            key=sa_sgt.key,
                            label=sa_sgt.label,
                            tag_id=sa_sgt.tag_id,
                            status="inactive",
                        )
                    )
                else:
                    logger.debug(
                        f"SGT '{sa_sgt.label}' (key: {sa_key}) exists in SA but not ISE, and is already 'inactive'. No action needed."
                    )

        logger.info(
            f"Found {len(sgts_to_add_update)} SGTs that need to be added or updated in Secure Access."
        )
        logger.info(
            f"Found {len(sgts_to_mark_inactive)} SGTs that need to be marked 'inactive' in Secure Access."
        )

        return sgts_to_add_update, sgts_to_mark_inactive

    def sync_sgts(self):
        """
        Executes the full SGT synchronization process.
        """
        logger.info("Starting SGT synchronization process.")

        ise_sgts = self.ise_client.get_sgts()
        logger.info(f"Retrieved {len(ise_sgts)} SGTs from ISE.")

        sa_sgts = self.sa_client.get_sgts()
        logger.info(f"Retrieved {len(sa_sgts)} SGTs from Secure Access.")

        sgts_to_add_update, sgts_to_mark_inactive = self.diff_sgts(ise_sgts, sa_sgts)

        if sgts_to_add_update:
            logger.info(
                f"Initiating synchronization for {len(sgts_to_add_update)} SGTs (add/update) to Secure Access..."
            )
            self.sa_client.put_sgts(sgts_to_add_update)
            logger.info(
                "SGT add/update synchronization to Secure Access completed successfully."
            )
        else:
            logger.info("No SGTs needed to be added or updated in Secure Access.")

        if sgts_to_mark_inactive:
            logger.info(
                f"Initiating marking inactive for {len(sgts_to_mark_inactive)} SGTs in Secure Access..."
            )
            self.sa_client.put_sgts(sgts_to_mark_inactive)
            logger.info(
                "SGT marking inactive sync to Secure Access completed successfully."
            )
        else:
            logger.info("No SGTs needed to be marked 'inactive' in Secure Access.")

        logger.info("SGT synchronization process completed.")
