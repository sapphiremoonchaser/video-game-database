import os

import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("IGDB_CLIENT_ID")
client_secret = os.getenv("IGDB_CLIENT_SECRET")


# Get Twitch access token
token_response = requests.post(
    "https://id.twitch.tv/oauth2/token",
    params={
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    },
)

token_response.raise_for_status()

access_token = token_response.json()["access_token"]

print("Authentication successful!")


# Query IGDB
headers = {
    "Client-ID": client_id,
    "Authorization": f"Bearer {access_token}",
}

limit = 10
offset = 0

all_games = []

for page in range(n):
    query = f"""
    fields
        name,
        first_release_date,
        rating;
    limit {limit};
    offset {offset};
    """

    response = requests.post(
        "https://api.igdb.com/v4/games/",
        headers=headers,
        data=query,
    )

    response.raise_for_status()

    games = response.json()

    all_games.extend(games)

    offset += limit

print(f"Retrieved {len(all_games)} games")

for game in all_games:
    print(game["name"])