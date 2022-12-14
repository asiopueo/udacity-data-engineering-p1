import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: Extracts song data from source, transforms it, and inserts it row by row 
    into the songs_dim and artists_dim tables of the target database.

    Arguments:
        cur: the cursor object
        filepath: song data file path

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id', 'year', 'duration']].values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: Reads log data from source, transforms it, and inserts it row by row 
    into the time_dim and users_dim tables in the target database. In particular, the time column `ts` which measures
    the time which has passed since the 01/01/1970 in milliseconds, is transformed into a postgres TIMESTAMP from which
    the other time values are derived.

    Arguments:
        cur: the cursor object
        filepath: log data file path

    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query("page=='NextSong'")

    # convert timestamp column to datetime
    t = df['ts']
    
    # insert time data records
    time_stamp = pd.Series(pd.to_datetime(t, unit='ms'))
    time_data = (time_stamp, time_stamp.dt.hour, time_stamp.dt.day, time_stamp.dt.week, time_stamp.dt.month, time_stamp.dt.year, time_stamp.dt.weekday)
    column_labels = ('timestamp', 'hour', 'day', 'week of year', 'month', 'year', 'weekday')
    timedata_dict = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame.from_dict(timedata_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: Traverses the subdirectories in `filepath` and appends each json-file it encounters to a list.
    Proceeds to process them one by one by utilizing the function `func`

    Arguments:
        cur: the cursor object
        conn: database connection object
        filepath: file path to the source data
        func: function object

    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()