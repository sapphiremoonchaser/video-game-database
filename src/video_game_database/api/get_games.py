"""
This module provides a way to query while limiting the amount of data pulled.
"""


def get_games(
        limit: int = 500,
        offset: int = 0,
        n: int = 0
):
    """
    This function gets a list of games, limited to a specified number of records.

    :param limit: The number of records to pull
    :param offset: Where to start pulled records
    :param n: The number of times to pull records
    :return: dict with game, release date, and rating
    """
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