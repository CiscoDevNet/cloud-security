# sgt_sync/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Manages application configuration from environment variables."""

    ISE_SERVER: str = os.getenv("ISE_SERVER")
    ISE_USER: str = os.getenv("ISE_USER")
    ISE_PASS: str = os.getenv("ISE_PASS")
    SA_KEY: str = os.getenv("SA_KEY")
    SA_SECRET: str = os.getenv("SA_SECRET")

    BASE_SA_IDENTITY_URL: str = "https://api.sse.cisco.com/deployments/v2/identities"
    BASE_SA_AUTH_URL: str = "https://api.sse.cisco.com/auth/v2/token"
    BASE_ISE_ERS_URL: str = f"https://{ISE_SERVER}:9060/ers/config"

    # WARNING: This should be True in production environments!
    VERIFY_SSL: bool = False

    @classmethod
    def validate(cls):
        """Validates that all required environment variables are set."""
        required_vars = ["ISE_SERVER", "ISE_USER", "ISE_PASS", "SA_KEY", "SA_SECRET"]
        missing_vars = [var for var in required_vars if getattr(cls, var) is None]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. Please set them."
            )
