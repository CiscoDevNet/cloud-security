# sgt_sync/clients/ise_client.py
import httpx
import json
import logging
from requests.auth import HTTPBasicAuth
from typing import List

from ..config import Config
from ..models.sgt import SecurityGroupTag

logger = logging.getLogger("sgt_sync.ise_client")

class IseClientError(Exception):
    """Custom exception for ISE client errors."""
    pass

class IseClient:
    """
    Client for interacting with Cisco Identity Services Engine (ISE) ERS APIs.
    Handles SGT fetching.
    """
    def __init__(self, config: Config):
        self.config = config
        self.auth = HTTPBasicAuth(self.config.ISE_USER, self.config.ISE_PASS)
        self.headers = {
            "Accept": "application/JSON",
            "Content-Type": "application/JSON",
        }
        self.client = httpx.Client(verify=self.config.VERIFY_SSL)

    def get_sgts(self) -> List[SecurityGroupTag]:
        """
        Retrieve all Security Group Tags from ISE using the ERS API.
        Handles pagination and fetches full SGT details by following links.
        """
        logger.info(f"Retrieving ISE SGTs from {self.config.BASE_ISE_ERS_URL}/sgt...")
        ise_sgt_list: List[SecurityGroupTag] = []
        url = f"{self.config.BASE_ISE_ERS_URL}/sgt"

        current_start_index = 0
        page_size = 100
        total_sgts = -1

        try:
            while total_sgts == -1 or current_start_index < total_sgts:
                params = {"size": page_size, "startIndex": current_start_index}
                logger.debug(
                    f"Fetching ISE SGTs with startIndex={current_start_index}, size={page_size}"
                )

                response = self.client.get(url, auth=self.auth, params=params, headers=self.headers)
                response.raise_for_status()

                data = response.json()
                search_result = data.get("SearchResult", {})
                resources = search_result.get("resources", [])

                if not resources:
                    logger.debug("No more resources found in ISE response.")
                    break

                for resource in resources:
                    sgt_detail_link = resource.get("link", {}).get("href")

                    if sgt_detail_link:
                        sgt_detail_response = self.client.get(
                            sgt_detail_link, auth=self.auth, headers=self.headers
                        )
                        sgt_detail_response.raise_for_status()

                        sgt_data = sgt_detail_response.json().get("Sgt")

                        if sgt_data:
                            try:
                                ise_sgt_list.append(SecurityGroupTag.from_ise_data(sgt_data))
                            except ValueError as ve:
                                logger.warning(f"Skipping malformed ISE SGT data: {sgt_data} - {ve}")
                    else:
                        logger.warning(
                            f"Could not find link for ISE SGT resource: {resource}"
                        )

                total_sgts = search_result.get("total", len(ise_sgt_list))
                current_start_index += len(resources)
                logger.debug(
                    f"Current ISE SGTs retrieved: {len(ise_sgt_list)}, Total expected: {total_sgts}"
                )

            logger.info(f"Successfully retrieved {len(ise_sgt_list)} SGTs from ISE.")
            return ise_sgt_list
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to retrieve ISE SGTs (HTTP Status {e.response.status_code}): {e.response.text}"
            )
            raise IseClientError("Failed to retrieve ISE SGTs.") from e
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response from ISE: {e}")
            raise IseClientError("Invalid JSON response from ISE.") from e
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting ISE SGTs: {e}")
            raise IseClientError("Network error during ISE SGT retrieval.") from e