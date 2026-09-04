import os

import requests
from dotenv import load_dotenv


class IgdbClient:
    """Client for interacting with the IGDB API"""

    TOKEN_URL = "https://id.twitch.tv/oauth2/token"
    API_URL = "https://api.igdb.com/v4"

    def __init__(self):
        load_dotenv()

        self.client_id = os.getenv("IGDB_CLIENT_ID")
        self.client_secret = os.getenv("IGDB_CLIENT_SECRET")

        if not self.client_id:
            raise ValueError("IGDB_CLIENT_ID environment variable not set")

        if not self.client_secret:
            raise ValueError("IGDB_CLIENT_SECRET environment variable not set")

        self.access_token = self._get_access_token()

        self.headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }


    def _get_access_token(self) -> str:
        """Get an access token from Twitch."""

        response = requests.post(
            self.TOKEN_URL,
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
        )

        response.raise_for_status()

        return response.json()["access_token"]


    def query(
        self,
        endpoint: str,
        query: str,
        limit: int = 500,
        max_results: int | None = None,
    ) -> list[dict]:
        """Send a query to an IGDB endpoint."""

        response = requests.post(
            f"{self.API_URL}/{endpoint}",
            headers=self.headers,
            data=query
        )

        response.raise_for_status()

        return response.json()