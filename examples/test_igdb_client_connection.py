from xmlrpc import client

from src.video_game_database.api.igdb_client import IgdbClient


client = IgdbClient()

query = """
fields
    name,
    first_release_date,
    rating;
"""

games = client.query(
    endpoint="games",
    query=query,
    limit=100,
    max_results=1000
)

for game in games:
    print(game["name"])