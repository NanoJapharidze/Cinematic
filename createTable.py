import sqlite3
conn = sqlite3.connect("data.sqlite")
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50),
        email VARCHAR(50),
        password VARCHAR(20) )""")


cursor.execute("""CREATE TABLE IF NOT EXISTS comment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(100),
        title VARCHAR(100),
        text VARCHAR(1000))""")