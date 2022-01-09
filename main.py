from threading import Thread

import audio_output
import dashboard
import sensors

if __name__ == '__main__':
    sensor_thread = Thread(target=sensors.write_sensor_data_loop)
    sensor_thread.start()

    audio_thread = Thread(target=audio_output.output_audio_loop)
    audio_thread.start()

    dashboard.host_dashboard()
