from typing import Union
import sqlite3
from fastapi import FastAPI

app = FastAPI()


@app.get("/topanime")
async def read_root():
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor()
    f = """
    SELECT * FROM ANIMES
    WHERE watchcount = 3"""
    cur.execute(f)
    result = cur.fetchall()
    cur.close()
    conn.close()
    print(result)
    return {"result": result}


