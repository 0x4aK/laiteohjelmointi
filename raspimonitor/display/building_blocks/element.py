from .component import Component
from .alphabet import alphabet
from .icons import icons

from sense_hat import InputEvent, ACTION_PRESSED, ACTION_HELD


class DisplayElement(Component):
    _x = 0
    _y = 0
    _width = 8
    _height = 5

    def __init__(self, *args, **kwargs):
        super(DisplayElement, self).__init__(x=self._x, y=self._y, width=self._width,
                                             height=self._height, *args, **kwargs)

        self.is_selected = False
        self.last_selected = False

    def handle_left(self) -> None:
        self.x = self.x - 1 if self.x + self.width > 8 else -self.width + 8
        self.should_redraw = True

    def handle_right(self) -> None:
        self.x = self.x + 1 if self.x < 0 else 0
        self.should_redraw = True

    def insert_char_to_buffer(self, char: str) -> None:
        char_code = alphabet.get(char.lower(), alphabet.get('?'))
        for dy, line in enumerate(self.buffer):
            to_insert = [
                self.color if x else self.background for x in char_code[dy]]
            self.buffer[dy].extend(to_insert)
            self.buffer[dy].append(self.background)

    def insert_icon_to_buffer(self, icon: str) -> None:
        icon_code = icons.get(icon.lower())

        if not icon_code:
            raise NameError("Invalid icon name")

        for dy, line in enumerate(self.buffer):
            to_insert = [
                self.color if x else self.background for x in icon_code[dy]
            ]
            self.buffer[dy].extend(to_insert)
            self.buffer[dy].append(self.background)

    def update(self, timestamp, event: InputEvent = None) -> bool:
        if self.is_selected:
            if event and event.action in [ACTION_PRESSED, ACTION_HELD]:
                self.handle_input.get(event.direction, self.handle_default)()

            self.color.brightness = 1.0

        else:
            self.color.brightness = 0.4
            self.x = 0
            self.should_redraw = True

        if self.last_selected != self.is_selected:
            self.last_selected = self.is_selected
            self.update_buffer()
            self.should_redraw = True

        return self.should_redraw
