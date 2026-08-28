from xmlrpc import client

from src.video_game_database.api.igdb_client import IgdbClient


client = IgdbClient()

query = """
fields
    name,
    first_release_date,
    rating;
limit 10;
"""

games = client.query("games", query)

for game in games:
    print(game["name"])