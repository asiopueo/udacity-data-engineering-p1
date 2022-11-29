# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays_fact"
user_table_drop = "DROP TABLE IF EXISTS users_dim"
song_table_drop = "DROP TABLE IF EXISTS songs_dim"
artist_table_drop = "DROP TABLE IF EXISTS artists_dim"
time_table_drop = "DROP TABLE IF EXISTS time_dim"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays_fact (
        songplay_id     SERIAL PRIMARY KEY, 
        start_time      TIMESTAMP NOT NULL, 
        user_id         INT NOT NULL, 
        level           VARCHAR, 
        song_id         VARCHAR,
        artist_id       VARCHAR,
        session_id      INT, 
        location        VARCHAR, 
        user_agent      VARCHAR
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users_dim (
        user_id         INT PRIMARY KEY, 
        first_name      VARCHAR, 
        last_name       VARCHAR, 
        gender          CHAR, 
        level           VARCHAR
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs_dim (
        song_id         VARCHAR PRIMARY KEY, 
        title           VARCHAR NOT NULL, 
        artist_id       VARCHAR, 
        year            INT, 
        duration        DECIMAL(9,5) NOT NULL
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists_dim (
        artist_id       VARCHAR PRIMARY KEY, 
        name            VARCHAR NOT NULL, 
        location        VARCHAR, 
        latitude        DOUBLE PRECISION, 
        longitude       DOUBLE PRECISION
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time_dim (
        starttime TIMESTAMP PRIMARY KEY, 
        hour           INT, 
        day            INT, 
        week           INT, 
        month          INT, 
        year           INT, 
        weekday        INT
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays_fact (
        start_time, 
        user_id, 
        level, 
        song_id, 
        artist_id, 
        session_id, 
        location, 
        user_agent
    ) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s) 
    ON CONFLICT DO NOTHING
""")

user_table_insert = ("""
    INSERT INTO users_dim (
        user_id, 
        first_name, 
        last_name, 
        gender, 
        level
    ) 
    VALUES (%s,%s,%s,%s,%s) 
    ON CONFLICT (user_id)
    DO UPDATE SET level=EXCLUDED.level
""")

song_table_insert = ("""
    INSERT INTO songs_dim (
        song_id, 
        title, 
        artist_id, 
        year, 
        duration
    ) 
    VALUES (%s,%s,%s,%s,%s) 
    ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
    INSERT INTO artists_dim (
        artist_id, 
        name, 
        location, 
        latitude, 
        longitude
    ) 
    VALUES (%s,%s,%s,%s,%s) 
    ON CONFLICT DO NOTHING
""")


time_table_insert = ("""
    INSERT INTO time_dim (
        starttime, 
        hour, 
        day, 
        week, 
        month, 
        year, 
        weekday
    ) 
    VALUES (%s,%s,%s,%s,%s,%s,%s) 
    ON CONFLICT (start_time) DO NOTHING
""")


# FIND SONGS

song_select = ("""
    SELECT s.song_id, s.artist_id 
    FROM songs_dim s 
    JOIN artists_dim a ON s.artist_id = a.artist_id 
    WHERE title=%s AND name=%s AND duration=%s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]