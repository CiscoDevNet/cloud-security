# sgt_sync/clients/secure_access_client.py
import httpx
import json
import logging
import time
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Optional

from ..config import Config
from ..models.sgt import SecurityGroupTag

logger = logging.getLogger("sgt_sync.sa_client")

class SecureAccessClientError(Exception):
    """Custom exception for Secure Access client errors."""
    pass

class SecureAccessClient:
    """
    Client for interacting with Cisco Secure Access APIs.
    Handles token retrieval, SGT fetching, and SGT updates.
    """
    def __init__(self, config: Config):
        self.config = config
        self._token: Optional[str] = None
        self._token_expiry: Optional[float] = None
        self.client = httpx.Client()

    def _get_token(self) -> str:
        """
        Obtain an OAuth 2.0 token from Cisco Secure Access API.
        Caches the token for subsequent requests and checks for expiration.
        """
        # Check if a token exists and is still valid
        if self._token and self._token_expiry and time.time() < self._token_expiry:
            logger.debug("Using cached Secure Access token.")
            return self._token

        logger.info("Retrieving Secure Access token (or refreshing expired token)...")
        auth = HTTPBasicAuth(self.config.SA_KEY, self.config.SA_SECRET)

        try:
            response = self.client.post(self.config.BASE_SA_AUTH_URL, auth=auth)
            response.raise_for_status()
            token_data = response.json()
            self._token = token_data.get("access_token")
            expires_in = token_data.get("expires_in")

            if not self._token:
                raise SecureAccessClientError("Access token not found in response.")

            if expires_in:
                # Set expiry time a bit before actual expiration to account for network latency/processing time
                self._token_expiry = time.time() + expires_in - 60
                logger.info(f"Secure Access token retrieved successfully, expires in {expires_in} seconds.")
            else:
                self._token_expiry = None
                logger.warning("Secure Access token retrieved, but no 'expires_in' field found. Token validity not tracked.")

            return self._token
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to retrieve Secure Access token: {e.response.status_code} - {e.response.text}"
            )
            # Clear potentially invalid token on failure
            self._token = None
            self._token_expiry = None
            raise SecureAccessClientError("Failed to retrieve Secure Access token.") from e
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting Secure Access token: {e}")
            # Clear potentially invalid token on failure
            self._token = None
            self._token_expiry = None
            raise SecureAccessClientError("Network error during token retrieval.") from e

    def _get_headers(self) -> Dict[str, str]:
        """Returns common headers with the bearer token."""
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
        }

    def get_sgts(self) -> List[SecurityGroupTag]:
        """
        Retrieve all Security Group Tags from Secure Access.
        Handles pagination.
        """
        logger.info("Retrieving Secure Access SGTs...")
        sgt_list: List[SecurityGroupTag] = []
        url = f"{self.config.BASE_SA_IDENTITY_URL}/registrations/securityGroupTag"
        headers = self._get_headers()

        limit = 250  # Max limit allowed by the API
        offset = 0
        total_sgts = -1

        try:
            while total_sgts == -1 or offset < total_sgts:
                params = {"limit": limit, "offset": offset}
                logger.debug(
                    f"Fetching SGTs from SA with offset={offset}, limit={limit}"
                )
                response = self.client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if "data" in data and isinstance(data["data"], list):
                    for sa_sgt_data in data["data"]:
                        try:
                            sgt_list.append(SecurityGroupTag.from_sa_data(sa_sgt_data))
                        except ValueError as ve:
                            logger.warning(f"Skipping malformed SA SGT data: {sa_sgt_data} - {ve}")

                total_sgts = data.get("total", len(sgt_list))
                offset += len(data.get("data", []))

                if not data.get("data") and total_sgts > 0 and offset < total_sgts:
                    logger.warning(
                        "SA API returned no data but total count suggests more items. Breaking loop."
                    )
                    break
                elif total_sgts == 0:
                    break

            logger.info(f"Successfully retrieved {len(sgt_list)} Secure Access SGTs.")
            return sgt_list
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to retrieve Secure Access SGTs: {e.response.status_code} - {e.response.text}"
            )
            raise SecureAccessClientError("Failed to retrieve Secure Access SGTs.") from e
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting Secure Access SGTs: {e}")
            raise SecureAccessClientError("Network error during SA SGT retrieval.") from e

    def put_sgts(self, sgts_to_sync: List[SecurityGroupTag]):
        """
        Add or update Security Group Tags in Secure Access.
        This function batches requests to adhere to the API's maxItems limit (250).
        """
        if not sgts_to_sync:
            logger.info("No SGTs to add/update to Secure Access.")
            return

        logger.info(
            f"Attempting to add/update {len(sgts_to_sync)} SGTs to Secure Access..."
        )
        url = f"{self.config.BASE_SA_IDENTITY_URL}/registrations/securityGroupTag"
        headers = self._get_headers()

        batch_size = 250
        batch_payload = []

        try:
            for i in range(0, len(sgts_to_sync), batch_size):
                batch_sgts = sgts_to_sync[i : i + batch_size]
                batch_payload = [sgt.to_sa_format() for sgt in batch_sgts]

                logger.debug(
                    f"Processing batch {i // batch_size + 1} with {len(batch_payload)} SGTs."
                )
                response = self.client.put(url, headers=headers, json=batch_payload)
                response.raise_for_status()
                result = response.json()
                if result.get("success"):
                    logger.info(f"Successfully processed batch of {len(batch_payload)} SGTs.")
                else:
                    error_msg = result.get("error", "Unknown error")
                    logger.error(
                        f"Failed to process batch of {len(batch_payload)} SGTs. Response: {error_msg}"
                    )
                    raise SecureAccessClientError(f"SA API reported error for batch: {error_msg}")

            logger.info("Finished adding/updating SGTs to Secure Access.")
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to add/update Secure Access SGTs: {e.response.status_code} - {e.response.text}"
            )
            logger.error(f"Request payload: {json.dumps(batch_payload, indent=2)}")
            raise SecureAccessClientError("Failed to update Secure Access SGTs.") from e
        except httpx.RequestError as e:
            logger.error(
                f"An error occurred while requesting to update Secure Access SGTs: {e}"
            )
            raise SecureAccessClientError("Network error during SA SGT update.") from e