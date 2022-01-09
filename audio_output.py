import pyttsx3
from time import sleep

import database
import ranges


def output_audio_loop():
    while True:
        engine = pyttsx3.init()
        df = database.read_newest_record()
        humidity = round(df.humidity.squeeze())
        status, message = ranges.get_humidity_status(humidity)
        engine.say(message)
        engine.runAndWait()
        sleep(60)
        engine.endLoop()
