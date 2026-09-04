"""File for loading video game data to database."""
from datetime import datetime
import os

import psycopg2
from dotenv import load_dotenv

from api.igdb_client import IgdbClient

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def get_igdb_client() -> IgdbClient:
    return IgdbClient()


def get_game(
    client: IgdbClient,
    game_id: int,
) -> list[dict]:
    query = f"""
    fields
        id,
        name,
        slug,
        first_release_date,
        total_rating;
    where id = {game_id};
    """

    return client.query(
        endpoint="games",
        query=query,
    )


def insert_game(
    conn: psycopg2.extensions.connection,
    game: dict,
) -> None:
    query = """
        INSERT INTO games (
            game_id,
            name,
            slug,
            first_release_date,
            total_rating
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (game_id) DO NOTHING;
    """

    # Convert Unix timestamp to a Python date
    first_release_date = None

    if game.get("first_release_date"):
        first_release_date = datetime.fromtimestamp(
            game["first_release_date"]
        ).date()

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (
                game["id"],
                game["name"],
                game["slug"],
                first_release_date,
                game["total_rating"],
            ),
        )

    conn.commit()


if __name__ == "__main__":
    igdb = get_igdb_client()
    conn = get_connection()

    game = get_game(igdb, 7346)

    insert_game(conn, game[0])

    conn.close()

    print("Game inserted successfully!")
