import sqlite3
import pandas as pd


def get_connection():
    return sqlite3.connect('shroomboard.db')


def create_table():
    cur = get_connection().cursor()
    cur.execute('''DROP TABLE IF EXISTS measurement''')
    cur.execute('''CREATE TABLE measurement
                   (timestamp datetime, humidity float, temperature float)''')


def read_data():
    with get_connection() as connection:
        df = pd.read_sql_query("SELECT * FROM measurement", connection)
    return df






