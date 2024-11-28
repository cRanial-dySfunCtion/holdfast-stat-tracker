import sqlite3
import datetime
import os

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
database_name = "holdfast.db"
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def row_count_games():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    x = conn.execute("""SELECT COUNT(*) FROM games;""")
    count= x.fetchone()[0]
    return count

def row_count_honors():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    x = conn.execute("""SELECT COUNT(*) FROM honors;""")
    count= x.fetchone()[0]
    return count

def row_count_medals():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    x = conn.execute("""SELECT COUNT(*) FROM medals;""")
    count= x.fetchone()[0]
    return count

def add_game_entry(role, kills):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    date = datetime.date.today()
    ID = row_count_games() + 1
    c.execute("""insert into games (ID, date, role, kills)
    values (?, ?, ?, ?);
    """, (ID, date, role, kills))
    conn.commit()

def add_honor(honor_ID):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    date = datetime.date.today()
    c.execute("""insert into earned_honors (earned_honor_ID, date)
    values (?, ?);
    """, (honor_ID, date))
    conn.commit()


def add_medal(medal_ID):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    date = datetime.date.today()
    c.execute("""insert into earned_medals (earned_medal_ID, date)
    values (?, ?);
    """, (medal_ID, date))
    conn.commit()


def reset_database():
    os.remove(database_name)
    file_check()
    init_honors()
    init_medals()

def init_honors():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    mode = True  # True = description False = honor name
    with open("honors.txt", "r") as file:
        for line in file:
            if "\n" == line:
                description = ""
                honor_name = ""
                mode = True
            elif mode:
                description = line.strip()
                mode = False
            else:
                honor_name = line.strip()
                ID = row_count_honors() + 1
                c.execute("""insert into honors (honor_ID, name, description)
                values (?, ?, ?);
                """, (ID, honor_name, description))
                conn.commit()

def init_medals():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    mode = True  # True = description False = medal name
    with open("medals.txt", "r") as file:
        for line in file:
            if "\n" == line:
                description = ""
                medal_name = ""
                mode = True
            elif mode:
                description = line.strip()
                mode = False
            else:
                medal_name = line.strip()
                ID = row_count_medals() + 1
                c.execute("""insert into medals (medal_ID, name, description)
                values (?, ?, ?);
                """, (ID, medal_name, description))
                conn.commit()

def file_check():
    if not os.path.exists(database_name):
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE games(
                ID INTEGER, 
                date TEXT, 
                role TEXT, 
                kills INTEGER
                )""")

        c.execute("""CREATE TABLE medals(
                medal_ID INTEGER PRIMARY KEY, 
                name TEXT, 
                description TEXT
                )""")

        c.execute("""CREATE TABLE honors(
                honor_ID INTEGER PRIMARY KEY, 
                name TEXT, 
                description TEXT
                )""")

        c.execute("""CREATE TABLE earned_medals(
                earned_medal_ID INTEGER, 
                date TEXT
                )""")

        c.execute("""CREATE TABLE earned_honors(
                earned_honor_ID INTEGER, 
                date TEXT
                )""")


def get_earned_honors():
    conn = sqlite3.connect('holdfast.db')
    cursor = conn.cursor()
    cursor.execute("SELECT earned_honor_ID FROM earned_honors")
    results = cursor.fetchall()
    conn.close()
    earned_honors = []
    for honor in results:
        earned_honors.append(honor[0])
    return earned_honors

def get_all_honors():
    conn = sqlite3.connect('holdfast.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM honors")
    honors_data = cursor.fetchall()
    conn.close()
    return honors_data

def select_field_honor_data():
    conn = sqlite3.connect('holdfast.db')
    cursor = conn.cursor()
    cursor.execute("SELECT honor_ID, name FROM honors WHERE honor_ID NOT IN (SELECT earned_honor_ID FROM earned_honors)")
    honors_data = cursor.fetchall()
    conn.close()
    return honors_data


class honorSelectField(FlaskForm):
    submit = SubmitField("Enter")

    honor_ID = SelectField(u"Earned Honor")


def get_earned_medals():
    conn = sqlite3.connect('holdfast.db')
    cursor = conn.cursor()
    cursor.execute("SELECT earned_medal_ID FROM earned_medals")
    results = cursor.fetchall()
    conn.close()
    earned_medals = []
    for medal in results:
        earned_medals.append(medal[0])
    return earned_medals

def get_all_medals():
    conn = sqlite3.connect('holdfast.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medals")
    medals_data = cursor.fetchall()
    conn.close()
    return medals_data

def select_field_medal_data():
    conn = sqlite3.connect('holdfast.db')
    cursor = conn.cursor()
    cursor.execute("SELECT medal_ID, name FROM medals WHERE medal_ID NOT IN (SELECT earned_medal_ID FROM earned_medals)")
    medals_data = cursor.fetchall()
    conn.close()
    return medals_data


class medalSelectField(FlaskForm):
    submit = SubmitField("Enter")

    medal_ID = SelectField(u"Earned Medal")