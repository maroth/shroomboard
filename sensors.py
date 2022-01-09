from time import sleep
from datetime import datetime
from random import randint

import database


def read_sensor_data(last_humidity, trend):
    # replace this with reading data from actual sensor
    delta = randint(-10, 10) + trend
    humidity = last_humidity + delta
    last_humidity = humidity
    humidity = max(humidity, 0)
    humidity = min(humidity, 100)
    now = datetime.now()
    temperature = 80
    trend = ((humidity - 85) * -1) / 7

    measurement = database.Measurement(now, humidity, temperature)
    return measurement, last_humidity, trend


def write_sensor_data_loop():
    last_humidity = 50
    trend = 1
    while True:
        measurement, last_humidity, trend = read_sensor_data(last_humidity, trend)
        database.write_data(measurement)
        sleep(5)
