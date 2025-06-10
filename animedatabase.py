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
    id = anime['id']
    n = anime['media']
    name = (n['title']['english'], n['title']['romanji'], n['title']['Native'])
    scores = 0

    tags = '('
    for tags in n['tags']:
        for tag, rank in tags:
            if rank >= 70:
                tags.join(tag + ",")
            else:
                tags.join(tag + ")")
                break
    format = n['format']
    season = n['season']
    seasonYear = n['seasonYear']
    episodes = n['episodes']
    genres = ''
    for genre in n['genres']:
        genres.join("(" + genre + ")")
    global_score  = n['averageScore']
    studio = n['studios']['edges']['0']['node']['name']

    add_statement = f''' 
    INSERT OR IGNORE INTO anime_table (id, name, scores, tags, format, season, seasonYear, episodes, genres, global_score, studio) VALUES ({id}, {name}, {scores}, {tags}, {format}, {season}, {seasonYear}, {episodes}, {genres}, {global_score}, {studio});'''
def final_thing():
    results = create_db()
    conn = connect()
    if results == False:
        create_anime_db()
    
    conn.commit()