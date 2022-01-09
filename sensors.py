from time import sleep
from datetime import datetime
from random import randint

import database


def read_sensor_data(last_humidity, trend):
    delta = randint(-10, 10) + trend
    humidity = last_humidity + delta
    last_humidity = humidity
    humidity = max(humidity, 0)
    humidity = min(humidity, 100)
    now = datetime.now()
    temperature = 80
    trend = ((humidity - 25) * -1) / 10
    return now, humidity, temperature, last_humidity, trend


def write_data(timestamp, humidity, temperature):
    with database.get_connection() as connection:
        cur = connection.cursor()
        timestamp_formatted = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        statement = f"INSERT INTO measurement (timestamp, humidity, temperature) " \
                    f"VALUES ('{timestamp_formatted}', {humidity}, {temperature})"
        cur.execute(statement)
        cur.close()


def write_sensor_data_loop():
    last_humidity = 50
    trend = 1
    while True:
        timestamp, humidity, temperature, last_humidity, trend = read_sensor_data(last_humidity, trend)
        write_data(timestamp, humidity, temperature)
        sleep(5)
