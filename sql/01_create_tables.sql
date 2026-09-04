CREATE TABLE games (
    game_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    first_release_date DATE,
    total_rating NUMERIC(5,2)
);


CREATE TABLE genres (
    genre_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE platforms (
    platform_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    abbreviation VARCHAR(50)
);


CREATE TABLE game_modes (
    game_mode_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE player_perspectives (
    player_perspective_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE franchises (
    franchise_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);


CREATE TABLE developers (
    developer_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);


CREATE TABLE publishers (
    publisher_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);


CREATE TABLE game_genres (
    game_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,

    PRIMARY KEY (game_id, genre_id),

    FOREIGN KEY (game_id)
        REFERENCES games(game_id),

    FOREIGN KEY (genre_id)
        REFERENCES genres(genre_id)
);


CREATE TABLE game_platforms (
    game_id INTEGER NOT NULL,
    platform_id INTEGER NOT NULL,

    PRIMARY KEY (game_id, platform_id),

    FOREIGN KEY (game_id)
        REFERENCES games(game_id),

    FOREIGN KEY (platform_id)
        REFERENCES platforms(platform_id)
);


CREATE TABLE game_game_modes (
    game_id INTEGER NOT NULL,
    game_mode_id INTEGER NOT NULL,

    PRIMARY KEY (game_id, game_mode_id),

    FOREIGN KEY (game_id)
        REFERENCES games(game_id),

    FOREIGN KEY (game_mode_id)
        REFERENCES game_modes(game_mode_id)
);


CREATE TABLE game_player_perspectives (
    game_id INTEGER NOT NULL,
    player_perspective_id INTEGER NOT NULL,

    PRIMARY KEY (game_id, player_perspective_id),

    FOREIGN KEY (game_id)
        REFERENCES games(game_id),

    FOREIGN KEY (player_perspective_id)
        REFERENCES player_perspectives(player_perspective_id)
);


CREATE TABLE game_franchises (
    game_id INTEGER NOT NULL,
    franchise_id INTEGER NOT NULL,

    PRIMARY KEY (game_id, franchise_id),

    FOREIGN KEY (game_id)
        REFERENCES games(game_id),

    FOREIGN KEY (franchise_id)
        REFERENCES franchises(franchise_id)
);


CREATE TABLE game_developers (
    game_id INTEGER NOT NULL,
    developer_id INTEGER NOT NULL,

    PRIMARY KEY (game_id, developer_id),

    FOREIGN KEY (game_id)
        REFERENCES games(game_id),

    FOREIGN KEY (developer_id)
        REFERENCES developers(developer_id)
);


CREATE TABLE game_publishers (
    game_id INTEGER NOT NULL,
    publisher_id INTEGER NOT NULL,

    PRIMARY KEY (game_id, publisher_id),

    FOREIGN KEY (game_id)
        REFERENCES games(game_id),

    FOREIGN KEY (publisher_id)
        REFERENCES publishers(publisher_id)
);

