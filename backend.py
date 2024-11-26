import sqlite3
import datetime
import os
database_name = "holdfast.db"


def row_count():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    x = conn.execute("""SELECT COUNT(*) FROM games;""")
    count= x.fetchone()[0]
    return count


def add_game_entry(role, kills):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    date = datetime.date.today()
    ID = row_count() + 1
    c.execute("""insert into games (ID, date, role, kills)
    values (?, ?, ?, ?);
    """, (ID, date, role, kills))
    conn.commit()

    
def file_check():
    if not os.path.exists(database_name):
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE games(
                ID INT, 
                date text, 
                role text, 
                kills int
                )""")

        c.execute("""CREATE TABLE medals(
                ID INT AUTO_INCREMENT PRIMARY KEY, 
                name text, 
                description text
                )""")

        c.execute("""CREATE TABLE earned_medals(
                medal_ID INT, 
                date text
                )""")

        c.execute("""CREATE TABLE honors(
                ID INT AUTO_INCREMENT PRIMARY KEY, 
                name text, 
                description text
                )""")

        c.execute("""CREATE TABLE earned_honors(
                honor_ID INT, 
                date text
                )""")

