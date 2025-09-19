import os

try:
    from devtools import pprint

    _use_pprint = True
except ImportError:
    pprint = print
    _use_pprint = False
from access_token import generate_access_token
from secure_access.configuration import Configuration
from secure_access.api_client import ApiClient
from secure_access.api import APIKeysApi, RoamingComputersApi
from secure_access.models import (
    CreateAPIKeysRequest,
    PatchAPIKeyRequest,
    KeysResponseList,
    KeyResponse,
    KeyResponseRefreshSecret,
)
from typing import Optional, List


class KeyAdminApi:
    """
    Handles Secure Access API key administration operations.
    """

    def __init__(self) -> None:
        """
        Initializes the KeyAdminApi, checks required environment variables, and sets up API clients.

        Raises:
            ValueError: If required environment variables are missing.
            RuntimeError: If access token generation fails.
        """
        missing_vars: List[str] = []
        for var in ["CLIENT_ID", "CLIENT_SECRET"]:
            if os.environ.get(var) is None:
                missing_vars.append(var)
        if missing_vars:
            raise ValueError(
                f"Required environment variable(s) not set: {', '.join(missing_vars)}"
            )

        try:
            self.access_token: str = generate_access_token()
        except Exception as e:
            raise RuntimeError(f"Failed to generate access token: {e}")
        self.configuration: Configuration = Configuration(
            access_token=self.access_token
        )
        self.api_client: ApiClient = ApiClient(configuration=self.configuration)
        self.api_keys_api: APIKeysApi = APIKeysApi(api_client=self.api_client)

    def get_api_keys(self) -> "KeysResponseList":
        """
        Retrieves all API keys for the organization.

        Returns:
            KeysResponseList: The API keys response object.

        Raises:
            Exception: If the API call fails.
        """
        return self.api_keys_api.get_api_keys()

    def post_api_keys(
        self,
        name: str,
        scopes: list,
        description: Optional[str] = None,
        expire_at: Optional[str] = None,
    ) -> dict:
        """
        Creates a new Secure Access API key using the SDK's 'without preload content' method.

        Args:
            name (str): The name of the API key.
            scopes (list): List of scopes for the API key.
            description (Optional[str]): Description of the API key.
            expire_at (Optional[str]): Expiration timestamp or empty string.

        Returns:
            dict: The parsed JSON response from the API.

        Raises:
            ValueError: If name or scopes are not provided.
            RuntimeError: If the API call fails (non-2xx status).
        """
        if not name or not scopes:
            raise ValueError(
                "name and scopes are required to create the Secure Access API key."
            )
        payload = CreateAPIKeysRequest(
            name=name,
            scopes=scopes,
            description=description,
            expire_at=expire_at or "",
        )
        response = self.api_keys_api.create_api_keys_without_preload_content(payload)
        if not (200 <= response.status < 300):
            raise RuntimeError(
                f"Failed to create API key. Status: {response.status}, Response: {response.data.decode('utf-8')}"
            )
        return response.json()

    def get_api_key(self, api_key_id: str) -> "KeyResponse":
        """
        Retrieves the properties of a specific API key.

        Args:
            api_key_id (str): The API key identifier.

        Returns:
            KeyResponse: The API key response object.

        Raises:
            ValueError: If api_key_id is not provided.
            Exception: If the API call fails.
        """
        if not api_key_id:
            raise ValueError("id is required to get the API key.")
        return self.api_keys_api.get_api_key(api_key_id)

    def patch_api_keys(
        self,
        api_key_id: str,
        name: Optional[str] = None,
        scopes: Optional[list] = None,
        description: Optional[str] = None,
        allowed_ips: Optional[list] = None,
    ) -> dict:
        """
        Updates a Secure Access API key using the SDK's 'without preload content' method.

        Args:
            api_key_id (str): The API key identifier.
            name (Optional[str]): The new name for the API key.
            scopes (Optional[list]): The new scopes for the API key.
            description (Optional[str]): The new description.
            allowed_ips (Optional[list]): Allowed IPs for the API key.

        Returns:
            dict: The parsed JSON response from the API.

        Raises:
            ValueError: If no update fields are provided or api_key_id is missing.
            RuntimeError: If the API call fails (non-2xx status).
        """
        if not api_key_id:
            raise ValueError("id is required to update the API key.")
        if not name or not scopes:
            raise ValueError(
                "name and scopes are required to update the Secure Access API key."
            )
        payload = PatchAPIKeyRequest(
            name=name,
            scopes=scopes,
            description=description,
            allowed_ips=allowed_ips,
        )
        response = self.api_keys_api.patch_api_key_without_preload_content(
            api_key_id, payload
        )
        if not (200 <= response.status < 300):
            raise RuntimeError(
                f"Failed to update API key. Status: {response.status}, Response: {response.data.decode('utf-8')}"
            )
        return response.json()

    def delete_api_keys(self, api_key_id: str) -> None:
        """
        Deletes a Secure Access API key.

        Args:
            api_key_id (str): The API key identifier.

        Raises:
            ValueError: If api_key_id is not provided.
            Exception: If the API call fails.
        """
        if not api_key_id:
            raise ValueError("id is required to delete the API key.")
        self.api_keys_api.delete_api_key(api_key_id)

    def refresh_api_keys(self, api_key_id: str) -> "KeyResponseRefreshSecret":
        """
        Refreshes a Secure Access API key.

        Args:
            api_key_id (str): The API key identifier.

        Returns:
            KeyResponseRefreshSecret: The refreshed API key response object.

        Raises:
            ValueError: If api_key_id is not provided.
            Exception: If the API call fails.
        """
        if not api_key_id:
            raise ValueError("id is required to refresh the Secure Access API key.")
        return self.api_keys_api.refresh_api_key(
            api_key_id, _headers={"content-type": "application/json"}
        )


if __name__ == "__main__":
    key_admin_api = KeyAdminApi()
    try:
        print("Getting Secure Access API keys...")
        api_keys_response = key_admin_api.get_api_keys()
        print("Success. GET API Keys:")
        pprint(api_keys_response)

        print("Creating a new Secure Access API key...")
        name = "roaming computers api key"
        scopes = ["deployments.roamingcomputers:read"]
        create_response_json = key_admin_api.post_api_keys(name, scopes)
        print("Success. POST API Keys:")
        pprint(create_response_json)

        print("Extracting API key id from creation response...")
        api_key_id = None
        if (
            create_response_json
            and "key" in create_response_json
            and create_response_json["key"]
        ):
            api_key_id = create_response_json["key"].get("id")
        if not api_key_id:
            print("Failed to retrieve API key id from creation response.")
            exit(1)

        print("Getting the created API key details...")
        api_key_response = key_admin_api.get_api_key(api_key_id)
        print("Success. GET API Key:")
        pprint(api_key_response)

        print("Updating the Secure Access API key...")
        name = "second update api key for roaming computers"
        scopes.append("deployments.roamingcomputers:write")
        patch_response = key_admin_api.patch_api_keys(api_key_id, name, scopes)
        print("Success. PATCH API Key:")
        pprint(patch_response)

        print("Refreshing the Secure Access API key credentials...")
        refresh_response = key_admin_api.refresh_api_keys(api_key_id)
        print("Success. REFRESH API Key:")
        pprint(refresh_response)

        print("Extracting client_id and client_secret from refresh response...")
        api_key_client_id = None
        api_key_client_secret = None
        if (
            refresh_response
            and hasattr(refresh_response, "key")
            and refresh_response.key
        ):
            api_key_client_id = getattr(refresh_response.key, "client_id", None)
            api_key_client_secret = getattr(refresh_response.key, "client_secret", None)
        if not api_key_client_id or not api_key_client_secret:
            print("Failed to retrieve client_id/client_secret from refresh response.")
            exit(1)

        print(
            "Using the created Secure Access API key to get a list of the roaming computers..."
        )
        keyadmin_access_token = generate_access_token(
            client_id=api_key_client_id, client_secret=api_key_client_secret
        )
        keyadmin_configuration = Configuration(access_token=keyadmin_access_token)
        keyadmin_api_client = ApiClient(configuration=keyadmin_configuration)
        roaming_computers_api = RoamingComputersApi(api_client=keyadmin_api_client)
        try:
            print("Getting roaming computers...")
            roaming_computers = roaming_computers_api.list_roaming_computers()
            print("Success. GET Roaming Computers:")
            pprint(roaming_computers)
        except Exception as e:
            print(f"An error occurred while getting roaming computers: {e}")

        print(
            "Deleting the Secure Access API key created to get the roaming computers..."
        )
        key_admin_api.delete_api_keys(api_key_id)
        print(f"No Content. DELETE API Key {api_key_id}.")
    except Exception as e:
        print(e)
