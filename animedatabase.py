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
    pointer.execute(anime_table)

def add_anime(anime: dict):
    n = anime['media']
    id = n['id']
    name = f"({n['title']['english']}, {n['title']['romaji']}, {n['title']['native']})"
    scores = 0
    tags = '('
    for tag in n['tags']:
        if tag['rank']>= 70:
            tags = tags.join(tag['name'] + ",")
        else:
            tags = tags.join(tag['name'] + ")")
            break
    format = n['format']
    season = n['season']
    seasonYear = n['seasonYear']
    episodes = n['episodes']
    genres = ''
    for genre in n['genres']:
        genres = genres.join("(" + genre + ")")
    global_score  = n['averageScore']
    try:
        studio = n['studios']['edges'][0]['node']['name']
    except:
        studio = 'NuLL'
    query = """INSERT OR IGNORE INTO ANIMES (
    id, name, scores, tags, format, season, seasonYear, episodes, genres, global_score, studio
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    values = (id, name, scores, tags, format, season, seasonYear, episodes, genres, global_score, studio)
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
    print("success")
