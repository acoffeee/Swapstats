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
def create_anime_db(pointer):
    anime_table = '''
    CREATE TABLE IF NOT EXISTS ANIMES (
    id INTEGER PRIMARY KEY, 
    english TEXT,
    romaji TEXT,
    native TEXT,
    scores INT,
    tags TEXT,
    format TEXT,
    season TEXT,
    seasonYear INT,
    episodes INT,
    duration INT,
    genres TEXT,
    studio TEXT,
    watchcount INT,
    averagedeviation INT
    );
    '''
    pointer.execute(anime_table)

def add_anime(anime: dict):
    n = anime['media']
    id = n['id']
    if id == 487:
        print(anime['media'])
    english = n['title']['english']
    romaji = n['title']['romaji']
    native = n['title']['native']
    duration = n['duration']
    watch_count = 0
    average_deviation = 0
    scores = 0
    tags = '('
    for tag in n['tags']:
        if tag['rank']>= 70:
            tags += tag['name'] + ", "
        else:
            tags += tag['name'] + ")"
            break
    format = n['format']
    season = n['season']
    seasonYear = n['seasonYear']
    episodes = n['episodes']
    genres = ''
    for genre in n['genres']:
        genres += "(" + genre + ") "
    try:
        studio = n['studios']['edges'][0]['node']['name']
    except:
        studio = 'NuLL'
    query = """INSERT OR IGNORE INTO ANIMES (
    id, english, romaji, native, scores, tags, format, season, seasonYear, episodes, duration, genres, studio, watchcount, averagedeviation
) VALUES (?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    values = (id, english, romaji, native, scores, tags, format, season, seasonYear, episodes, duration, genres, studio, watch_count, average_deviation)
    return query, values
def final_thing(anime: dict):
    results = create_db()
    conn = sqlite3.connect('anime.db')
    pointer = conn.cursor()
    if results == False:
        create_anime_db(pointer)
    query, values = add_anime(anime)
    pointer.execute(query, values)
    conn.commit()
    pointer.close()
    conn.close()
    # print("success")
