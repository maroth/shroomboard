from threading import Thread

import dashboard
import database
import sensors

if __name__ == '__main__':
    database.create_table()
    thread = Thread(target=sensors.write_sensor_data_loop)
    thread.start()
    dashboard.host_dashboard()
