# Project: Data Modeling with PostGres
This project is concerned with the modeling of an *analytical database* for the data analystics team of the fictional music streaming startup *Sparkify Ltd.* 
The analytics team is interested in different business related-questions, such as, what songs the individual users are listening to, in order to make them recommendations for new songs and artists.

Closely related to this question is the ETL process, i.e. establishing a pipeline which extracts the raw data from the original operational database, transforms it, and loads it into the freshly designed analytical DB. Within this project, the target database will be loaded in a python script raw by raw using for loops and SQL-`INSERT` statements. The main data engineering tool here, apart from `Python`, is [Pandas](https://pandas.pydata.org/). The implemented ETL-process is slow and cumbersome, but we will learn more efficient methods during the course of the data engineering nanodegree program. 

## Quick Start

In order to create the analytical database and tables, launch the python (>=3.6.3) script from a terminal:
```bash
foo@bar:~$ python create_tables.py
```
The ETL-process can be started by lauching:
```
foo@bar:~$ python etl.py
```

The two Jupyter notebooks can be launched using either a JupyterLab or JupyterNotebook server, e.g.
```
foo@bar:~$ jupyter-notebook etl.ipynb
```


## Purpose of the Analytical Database
The purpose of the analytical database and hence the corresponding ETL process is to enable the Sparkify's data analysis team to do fast and efficient queries about business related questions in a flexible manner.

The songs of a user can be easily extracted from the fact table `fact_table`, and ranked using their number of plays. We interpret a song as highly liked by the user if the song has been played a high number of times, in relative terms (cf. example queries below).

This can be used for a recommender system, for example: If the most liked songs of one user match the most liked songs of another user, measured by an appropriate metric, then an additional liked song by the second song may be recommended to the first user. 

A standard example of such a [recommender system](https://en.wikipedia.org/wiki/Recommender_system) is the use of [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity).

Other than that, the database enables Sparkify's the analytical fast and free queries, in order to find songs to promote to a wide audience, do analytical queries on the demographics of the listeners etc.


## Database Scheme and Design
We are using a PostGres-database server. The database itself is called `sparkifydb`. The tables within this database follow the star schema, enabling fast analytical querying.

There are five tables within this DB. These are: 
 - `songplays_fact` the **fact table** in the center of the 'star'

The **dimensional tables** are:
 - `users_dim` - the  containing,
 - `songs_dim` - information about the respective songs, and
 - `artists_dim` - Information about the artists,
 - `time_dim` - more detailed infos about the time when the songplay occurred


The schema relationships are as follows:

<img src='./images/er_diagram.png'>


## ETL-Pipeline
The final ETL-pipeline which populates the analytical database is implemented in `etl.py` and consists of stages:

 1. Process raw song data,
 2. Process raw log data.

In the first stage, the song data is imported using `Pandas` and converted to a Python-`list`, selecting only a subset of five attributes which are necessary to fill `songs_dim`. The same is done with `artists_dim`, slecting also here a subset of five attributes from the raw data and inserting into the table using a `for`-loop.

The second stage is more interesting. Firstly, the tables `time_dim` and `user_dim` are being populated. In order to populate `time_dim`, the timestamp `ts` from the log data is extracted and transformed using Pandas into the appropriate tuple 
```
('timestamp', 'hour', 'day', 'week of year', 'month', 'year', 'weekday')
```
Then, we insert `user_dim` in the direct way again, only selecting the specified columns from the log data, as we have dome in the two dim-tables in the first stage. 

Finally, `fact_songs` is being populated by making an inner join of `artists_dim` with `songs_dim` on `artist_id`.



## Repository
This repository contains the following files and directories:

```
├── data/
├── images/
├── create_tables.py
├── etl.ipynb
├── etl.py
├── test.ipynb
├── sql_queries.py
└── README.md
```

- `data/`: Contains the raw data set and is organized as follows:

 - `create_tables.py`: Contains function to create. These are `create_database()`, `drop_tables()`, `create_tables()`, and finally a `main()`-function which creates a database, and subsequently drops and creates tables again.

- `sql_queries.py`: This file contains a multitude of SQL query commands, encoded as python strings, which are organized into four blocks: `DROP_TABLES`, `CREATE_TABLES`, `INSERT_RECORD`, `FIND_SONGS`.
Finally, two lists, `create_list_queries`, and `drop_table_queries` are 

 - `etl.ipynb`: The Jupyter notebook file which is used for discovery and experimentation.

 - `etl.py`: `process_song_file()` `process_log_file()` `process_data()`. Finally, the `main()`-function knits everything together.

 - `test.ipynb`: Contains a number of sanity checks before 

 - `README.md`: The file you are currently reading.




## Example Queries
Extract the songplays by a user:
``` sql
    SELECT FROM
```

Extract the songplays by a user and rank them by the number of songplays:
``` sql
    SELECT FROM
```


