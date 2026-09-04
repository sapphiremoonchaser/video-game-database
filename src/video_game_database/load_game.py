"""File for loading video game data to database."""
from datetime import datetime
import os
from unittest import result

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
        total_rating,
        genres,
        platforms,
        franchises;
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


def get_genres(
    client: IgdbClient,
    genre_ids: list[int]
) -> list[dict]:
    genres = []

    for genre_id in genre_ids:
        query = f"""
        fields
            id,
            name;
        where id = {genre_id};
        """

        result = client.query(
            endpoint="genres",
            query=query,
        )

        genres.extend(result)

    return genres


def insert_genre(
    conn: psycopg2.extensions.connection,
    genre: dict
) -> None:

    query = """
    INSERT INTO genres (
        genre_id,
        name
    )
    VALUES (%s, %s)
    ON CONFLICT (genre_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (
                genre["id"],
                genre["name"],
            ),
        )
    conn.commit()


def insert_game_genre(
    conn: psycopg2.extensions.connection,
    game_id: int,
    genre_id: int
) -> None:

    query = """
        INSERT INTO game_genres (
            game_id,
            genre_id
        )
        VALUES (%s, %s)
        ON CONFLICT (game_id, genre_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (
                game_id,
                genre_id
            )
        )
    conn.commit()


def get_platforms(
    client: IgdbClient,
    platform_ids: list[int]
) -> list[dict]:

    platforms = []

    for platform_id in platform_ids:
        query = f"""
        fields
            id,
            name;
        where id = {platform_id};
        """

        result = client.query(
            endpoint="platforms",
            query=query
        )

        platforms.extend(result)

    return platforms


def insert_platform(
    conn: psycopg2.extensions.connection,
    platform: dict,
) -> None:

    query = """
        INSERT INTO platforms (
            platform_id,
            name
        )
        VALUES (%s, %s)
        ON CONFLICT (platform_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (
                platform["id"],
                platform["name"],
            ),
        )

    conn.commit()


def insert_game_platform(
    conn: psycopg2.extensions.connection,
    game_id: int,
    platform_id: int
) -> None:
    query = """
            INSERT INTO game_platforms (
                game_id,
                platform_id
            )
            VALUES (%s, %s) 
            ON CONFLICT (game_id, platform_id) DO NOTHING; \
            """

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (
                game_id,
                platform_id
            )
        )
    conn.commit()


def get_franchises(
    client: IgdbClient,
    franchise_ids: list[int]
) -> list[dict]:

    franchises = []

    for franchise_id in franchise_ids:
        query = f"""
        fields
            id,
            name;
        where id = {franchise_id};
        """

        result = client.query(
            endpoint="franchises",
            query=query
        )

        franchises.extend(result)

    return franchises


def insert_franchise(
    conn: psycopg2.extensions.connection,
    franchise: dict,
) -> None:

    query = """
        INSERT INTO franchises (
            franchise_id,
            name
        )
        VALUES (%s, %s)
        ON CONFLICT (franchise_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (
                franchise["id"],
                franchise["name"],
            ),
        )

    conn.commit()


def insert_game_franchise(
    conn: psycopg2.extensions.connection,
    game_id: int,
    franchise_id: int
) -> None:
    query = """
            INSERT INTO game_franchises (
                game_id,
                franchise_id
            )
            VALUES (%s, %s) 
            ON CONFLICT (game_id, franchise_id) DO NOTHING;
            """

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (
                game_id,
                franchise_id
            )
        )
    conn.commit()



if __name__ == "__main__":
    igdb = get_igdb_client()
    conn = get_connection()

    # Get game from IGDB
    game = get_game(igdb, 7346)[0]

    # Insert the game into the database
    insert_game(conn, game)

    # Insert genres
    genres = get_genres(
        igdb,
        game["genres"],
    )

    for genre in genres:
        insert_genre(conn, genre)

        insert_game_genre(
            conn,
            game["id"],
            genre["id"]
        )

    # Insert platforms
    platforms = get_platforms(
        igdb,
        game["platforms"]
    )

    for platform in platforms:
        insert_platform(conn, platform)

        insert_game_platform(
            conn,
            game["id"],
            platform["id"]
        )

    # Insert franchises
    franchises = get_franchises(
        igdb,
        game["franchises"]
    )

    for franchise in franchises:
        insert_franchise(conn, franchise)

        insert_game_franchise(
            conn,
            game["id"],
            franchise["id"]
        )

    conn.close()

    print("Genres inserted successfully")
