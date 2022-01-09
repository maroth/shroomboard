import sqlite3
import pandas as pd
import datetime


class Measurement:
    def __init__(self, timestamp, humidity, temperature):
        self.timestamp = timestamp
        self.humidity = humidity
        self.temperature = temperature

    timestamp: datetime.datetime
    humidity: float
    temperature: float


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


def read_newest_record():
    with get_connection() as connection:
        df = pd.read_sql_query("SELECT * FROM measurement ORDER BY timestamp DESC LIMIT 1", connection)
    return df


def write_data(measurement):
    with get_connection() as connection:
        cur = connection.cursor()
        timestamp_formatted = measurement.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        statement = f"INSERT INTO measurement (timestamp, humidity, temperature) " \
                    f"VALUES ('{timestamp_formatted}', {measurement.humidity}, {measurement.temperature})"
        cur.execute(statement)
        cur.close()
