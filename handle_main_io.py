import sqlite3
import os
import json
def connect():
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor()
    return cur, conn
def create_user_table():
    cur, conn = connect()
    statement = """
    CREATE TABLE IF NOT EXISTS USERS(
    user1 TEXT,
    user2 TEXT,
    comparision INT,
    shared INT);"""
    cur.execute(statement)
    conn.commit()
    test_data ="""
    INSERT OR IGNORE INTO USERS (user1, user2, comparision, shared) VALUES (?, ?, ?, ?);"""
    test = "coffeee"
    data = "data"
    values = (test, data, 69, 420)
    cur.execute(test_data, values)
    conn.commit()
    cur.close()
    conn.close()

def handle_output(user1, user2, value, shared):
    cur, conn = connect()
    statement = """
    INSERT INTO USERS(user1, user2, comparision, shared) VALUES (?, ?, ?, ?)"""
    values = (user1, user2, value, shared)
    cur.execute(statement, values)
    conn.commit()
    cur.close()
    conn.close()

def handle_some_input():
    filtered_results =[]
    try:
        cur, conn = connect()
        get_users = """
        SELECT user1 FROM USERS"""
        cur.execute(get_users)
        results = cur.fetchall()
        print(results)
        for user in results:
            if user[0] in filtered_results or user[0] == 'test':
                continue
            else:
                filtered_results.append(user[0])
        cur.close()
        conn.close()
    except Exception as e:
        create_user_table()
        print(e)
        handle_some_input()
    print(filtered_results)
    return filtered_results