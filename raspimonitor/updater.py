from collections import deque
from time import sleep, time
from threading import Thread
import shelve
import os

import schedule
from sense_hat import SenseHat


class UpdateThread(Thread):
    """
    Responsible for reading values from SenseHat and updating database file.
    """

    datafile = "/tmp/raspimonitor-data"
    updates_in_hour = 12  # update every 5 minutes

    def __init__(self, *args, **kwargs):
        super(UpdateThread, self).__init__(*args, **kwargs)

        self.sense = SenseHat()

        self.data_points = {
            'temp': {
                'unit': "°C",
                'getter': self.sense.get_temperature
            },
            'pressure': {
                'unit': "mbar",
                'getter': self.sense.get_pressure
            },
            'humidity': {
                'unit': "%",
                'getter': self.sense.get_humidity
            },
        }

        self.reset_db()
        self.update()

        self.quiting = False

    def run(self) -> None:
        schedule.every(int(60 / self.updates_in_hour)
                       ).minutes.at(':00').do(self.update)

        while not self.quiting:
            schedule.run_pending()
            sleep(1)

    def quit(self) -> None:
        self.quiting = True

    def reset_db(self) -> None:
        """
        Makes sure that the database file is the right format.
        """

        with shelve.open(self.datafile) as db:
            for data_point, data_dictionary in self.data_points.items():
                db[data_point] = {
                    "unit": data_dictionary.get("unit"),
                    "data": deque(maxlen=30)
                }

    def update(self) -> None:
        """
        Loops through data_points and uses it's getter function
        to append (Timestamp, Value) to database file
        """
        timestamp = int(time())

        with shelve.open(self.datafile, writeback=True) as db:
            for data_point, data_dictionary in self.data_points.items():
                db[data_point]["data"].append(
                    (timestamp,
                     round(data_dictionary["getter"](), 1))
                )
