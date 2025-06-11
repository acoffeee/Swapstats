import sqlite3


def update_anime(id: int, score: int, cur):
    get_anime = f'SELECT * FROM ANIMES WHERE id={id}'
    cur.execute(get_anime)
    anime = cur.fetchone()
    update_count = f"""
    UPDATE ANIMES
    SET watchcount = {int(anime[13] + 1)}
    WHERE id = {id}
    """
    update_deviation = f"""
    UPDATE ANIMES
    SET averagedeviation ={((anime[14] * anime[13]) + score) / (anime[13] + 1)}
    WHERE id = {id}
    """
    cur.execute(update_count)
    cur.execute(update_deviation)
def process_list(user_list: list):
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor()
    for anime in user_list:
        print("anime")
        update_anime(anime['id'], anime['score'], cur)
    conn.commit()
    cur.close()
    conn.close()