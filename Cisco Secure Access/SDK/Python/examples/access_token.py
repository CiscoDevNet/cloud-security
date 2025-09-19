"""
Module for generating an access token for Cisco SSE API authentication.

This module provides a function to obtain an OAuth2 access token using client credentials stored in environment variables.

Usage:
    from access_token import generate_access_token
    token = generate_access_token()

What it does:
- Reads CLIENT_ID and CLIENT_SECRET from environment variables.
- Encodes credentials in base64 and requests an access token from the Cisco SSE API.
- Returns the access token string for use in API authentication.

Requirements:
- Set CLIENT_ID and CLIENT_SECRET environment variables before use.
- Ensure all dependencies in requirements.txt are installed.

Raises:
- ValueError if required environment variables are missing.
- Exception if token generation fails.
"""

import os
import base64
from secure_access.api.token_api import TokenApi
from typing import Optional


def generate_access_token(
    client_id: Optional[str] = None, client_secret: Optional[str] = None
) -> str:
    """
    Generates an OAuth2 access token for Cisco SSE API authentication.

    Args:
        client_id (Optional[str]): The client ID to use. If not provided, uses CLIENT_ID env var.
        client_secret (Optional[str]): The client secret to use. If not provided, uses CLIENT_SECRET env var.

    Returns:
        str: The access token string.

    Raises:
        ValueError: If neither parameters nor environment variables are set.
        Exception: If token generation fails.
    """
    cid = client_id or os.getenv("CLIENT_ID")
    csecret = client_secret or os.getenv("CLIENT_SECRET")
    if not cid or not csecret:
        raise ValueError(
            "CLIENT_ID and CLIENT_SECRET must be provided as arguments or set as environment variables."
        )
    token_api = TokenApi()
    base64_credentials = base64.b64encode(f"{cid}:{csecret}".encode()).decode()
    try:
        response = token_api.create_auth_token(
            grant_type="client_credentials",
            _headers={"Authorization": f"Basic {base64_credentials}"},
        )
        return response.access_token
    except Exception as e:
        print(f"An error occurred while creating the access token: {e}")
        raise Exception("Failed to generate access token") from e
