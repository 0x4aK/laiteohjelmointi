import subprocess

from sense_hat import InputEvent

from ..building_blocks.element import DisplayElement


class IpElement(DisplayElement):
    label = 'ip'

    def __init__(self, *args, **kwargs):
        super(IpElement, self).__init__(*args, **kwargs)

        self.value = subprocess.run(r"ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'",
                                    stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8').strip()

        self.last_selected = False

        self.update_buffer()

    def update_buffer(self):
        self.buffer = [[self.background] for _ in range(self.height)]

        if not self.is_selected:
            self.insert_icon_to_buffer(self.label)
            return

        for char in self.value:
            self.insert_char_to_buffer(char)

    def update(self, timestamp, event: InputEvent = None) -> bool:
        self.should_redraw = False

        return super(IpElement, self).update(timestamp, event)
