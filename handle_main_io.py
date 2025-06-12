import sqlite3
import os
import json
def connect():
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor(conn)
    return cur, conn
def create_user_table():
    if os.path.exists("anime.db"):
        return
    cur, conn = connect()
    statement = """
    CREATE IF NOT EXISTS USERS(
    user1 PRIMARY KEY INT,
    user2 INT,
    comparision INT)"""
    cur.execute(statement)
    con.commit()
    cur.close()
    conn.close()
def handle_output(user1, user2, value):
    cur, conn = connect()
    statement = """
    INSERT INTO USERS(user, user2, comaprision) VALUES (?, ?, ?)"""
    values = (user1, user2, value)
    cur.execute(statement, values)
    conn.commit()
    cur.close()
    conn.close()
def handle_input():
    create_user_table()
    cur, conn = connect()
    get_existing_comparisions = """
    SELECT * FROM USERS"""
    cur.execute(get_existing_comparisions)
    existing = cur.fetchall()
    compared = []
    for users in existing:
        done = (users['user1'], users['user2'])
        compared.append(done)
    return compared 