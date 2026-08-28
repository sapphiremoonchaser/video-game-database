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


