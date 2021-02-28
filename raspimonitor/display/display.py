from threading import Thread, Event
from time import sleep, time

from sense_hat import SenseHat

from .building_blocks.screen import Screen
from .building_blocks.color import Color
from .elements import IpElement, TempElement, HumidityElement, PressureElement
from .selector import Selector


class DisplayThread(Thread):
    def __init__(self, *args, **kwargs) -> None:
        super(DisplayThread, self).__init__(*args, **kwargs)

        self.sense = SenseHat()

        # SenseHat stick nonsense... stick.direction_any doesn't give InputEvent
        self.sense.stick.direction_up = self.handle_input
        self.sense.stick.direction_down = self.handle_input
        self.sense.stick.direction_left = self.handle_input
        self.sense.stick.direction_right = self.handle_input
        self.sense.stick.direction_middle = self.handle_input

        self.screen = Screen()

        self.elements = [
            IpElement(color=Color(0, 0, 255)),
            TempElement(sense=self.sense, color=Color(255, 0, 0)),
            HumidityElement(sense=self.sense, color=Color(0, 150, 200)),
            PressureElement(sense=self.sense, color=Color(200, 150, 0))
        ]
        self.selector = Selector(elements=self.elements,
                                 color=Color(0, 255, 0))

        self.sleeping = Event()
        self.sleeping.set()

        self.last_input = time()
        self.last_event = None
        self.timeout = 30
        self.quiting = False

    def run(self) -> None:
        self.screen += self.selector
        self.screen += self.selector.selected

        while not self.quiting:
            timestamp = time()

            if self.selector.update(timestamp, self.last_event):
                self.screen += self.selector

            # Update the selected element and redraw if needed
            if self.selector.selected.update(timestamp, self.last_event):
                self.screen += self.selector.selected

            self.last_event = None  # Consume last event so we wont have the same in next iteration
            self.sense.set_pixels(self.screen.flatten())  # Flatten the screen and set pixels

            """
            Sleep for 0.1 sec so we wont consume 100% CPU.
            0.05 sec = ~26% CPU utilization really snappy.
            0.1  sec = ~15% CPU utilization.
            0.2  sec = ~8%  CPU utilization but not responsive.
            When thread goes to sleep (go_to_sleep()), CPU utilization goes to near 0%.
            """
            sleep(0.1)

            if self.last_input + self.timeout < timestamp:
                self.go_to_sleep()

        self.sense.clear()

    def quit(self) -> None:
        """ Readies the thread to exit the main loop and quit """
        self.quiting = True
        self.sleeping.set()

    def go_to_sleep(self) -> None:
        """
        Clears the SenseHat pixel matrix and puts the thread to sleep.
        Crucial to preserve CPU when not in use.
        """
        print("[!] Display going to sleep")
        self.sense.clear()
        self.sleeping.clear()
        self.sleeping.wait()

    def handle_input(self, event) -> None:
        """
        Callback function for SenseHat stick.
        Records the time of the event, the input and
        continues running the main loop if the thread is sleeping.
        """
        self.last_input = time()
        # if waking up, don't set event
        self.last_event = event if self.sleeping.is_set() else None
        self.sleeping.set()
