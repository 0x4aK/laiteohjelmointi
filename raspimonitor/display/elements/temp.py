from sense_hat import SenseHat, InputEvent

from ..building_blocks.element import DisplayElement


class TempElement(DisplayElement):
    label = "temp"

    def __init__(self, sense: SenseHat = None, *args, **kwargs):
        if not sense:
            raise ValueError("No SenseHat instance provided")
        if not isinstance(sense, SenseHat):
            raise ValueError("Provided sense is not instance of SenseHat")

        super(TempElement, self).__init__(*args, **kwargs)

        self.sense = sense
        self._value = None

        self.update_buffer()

    @property
    def value(self):
        return f"{self._value:.1f}'C"

    @value.setter
    def value(self, value):
        self._value = value

    def update_buffer(self):
        self.buffer = [[self.background] for _ in range(self.height)]

        if not self.is_selected:
            self.insert_icon_to_buffer(self.label)
            return

        for char in self.value:
            self.insert_char_to_buffer(char)

    def update(self, timestamp, event: InputEvent = None) -> bool:
        self.should_redraw = False

        if self.last_update + 1 < timestamp:
            self.value = self.sense.get_temperature()
            self.last_update = timestamp
            self.update_buffer()
            self.should_redraw = True

        return super(TempElement, self).update(timestamp, event)
