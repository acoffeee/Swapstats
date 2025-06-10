#animedatabase.py
import sqlite3
import os

def create_db() -> bool:
    if os.path.exists("anime.db"):
        return True
    else:
        with open("anime.db", 'w'):
            pass
        return False
def create_anime_db():
    anime_table = '''
    CREATE TABLE IF NOT EXISTS ANIMES (
    id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL,
    scores INT,
    tags TEXT,
    format TEXT,
    season TEXT,
    seasonYear INT,
    episodes INT,
    genres TEXT,
    global_score INT,
    studio TEXT
    );
    '''
    conn.execute(anime_table)
def connect():
    try:
        with sqlite3.connect("anime.db") as conn:
            return conn

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def add_anime(anime: dict):
    n = anime['media']
    id = n['id']
    name = (n['title']['english'], n['title']['romaji'], n['title']['native'])
    scores = 0

    tags = '('
    for tag in n['tags']:
        if tag['rank']>= 70:
            tags.join(tag['name'] + ",")
        else:
            tags.join(tag['name'] + ")")
            break
    format = n['format']
    season = n['season']
    seasonYear = n['seasonYear']
    episodes = n['episodes']
    genres = ''
    for genre in n['genres']:
        genres.join("(" + genre + ")")
    global_score  = n['averageScore']
    studio = n['studios']['edges'][0]['node']['name']

    add_statement = f''' 
    INSERT OR IGNORE INTO anime_table (id, name, scores, tags, format, season, seasonYear, episodes, genres, global_score, studio) VALUES ({id}, {name}, {scores}, {tags}, {format}, {season}, {seasonYear}, {episodes}, {genres}, {global_score}, {studio});'''

def final_thing(anime: dict):
    results = create_db()
    conn = connect()
    if results == False:
        create_anime_db()
    add_anime(anime)
    conn.commit()
    conn.close()