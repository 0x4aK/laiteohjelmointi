#!/usr/bin/python3

import os
import sys
from signal import signal, SIGTERM

from raspimonitor.display import DisplayThread
from raspimonitor.updater import UpdateThread
from raspimonitor.webserver import Webserver


class RaspiMonitor:
    def __init__(self):
        self.threads = [DisplayThread(), UpdateThread(), Webserver()]

        signal(SIGTERM, self.term_handler)

    def term_handler(self, signal_number, _):
        print(f"[!] Got SIGTERM {signal_number}")
        [t.quit() for t in self.threads]

    def start(self):
        print("[>] Starting threads")
        [t.start() for t in self.threads]
        [t.join() for t in self.threads]

    def quit(self):
        print("[>] Waiting for the threads to finish up and quiting")
        [t.quit() for t in self.threads]
        [t.join() for t in self.threads]


def main():
    if not os.geteuid() == 0:
        exit('RaspiMonitor must be run as root!')

    if len(sys.argv) > 1:
        if sys.argv[1] == "enable":
            os.system(f"systemctl enable {os.path.dirname(os.path.abspath(__file__))}/raspimonitor.service")
            print("RaspiMonitor enabled and will start on boot")

        elif sys.argv[1] == "disable":
            os.system("systemctl disable raspimonitor.service")
            print("RaspiMonitor disabled")

        else:
            text = "Raspimonitor available commands: \n\n"
            text += "enable - installs RaspiMonitor as a system service and starts at boot\n"
            text += "disable - removes RaspiMonitor from system services\n"

            print(text)

        sys.exit()

    monitor = RaspiMonitor()
    try:
        monitor.start()
    except KeyboardInterrupt:
        monitor.quit()


if __name__ == '__main__':
    main()
