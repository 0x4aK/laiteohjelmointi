from collections import deque

from sense_hat import InputEvent, ACTION_PRESSED, ACTION_HELD

from .building_blocks.component import Component
from .building_blocks.element import DisplayElement


class Selector(Component):
    _x = 0
    _y = 5
    _width = 8
    _height = 3

    def __init__(self, elements: list, *args, **kwargs):
        super(Selector, self).__init__(x=self._x, y=self._y, width=self._width,
                                       height=self._height, *args, **kwargs)

        self.elements = deque(elements)

        self.left_arrow_x = self.x + 1
        self.right_arrow_x = self.x + self.width - 2

        self.update_buffer()

    @property
    def selected(self) -> DisplayElement:
        """ Returns the selected component """
        return self.elements[0]

    def handle_left(self) -> None:
        if self.selected.is_selected:
            return

        self.elements.rotate(-1)
        self.left_arrow_x = self.x

    def handle_right(self) -> None:
        if self.selected.is_selected:
            return

        self.elements.rotate(1)
        self.right_arrow_x = self.x + self.width - 1

    def handle_up(self) -> None:
        self.selected.is_selected = True
        self.color.brightness = 0.3

    def handle_down(self) -> None:
        self.selected.is_selected = False
        self.color.brightness = 1

    def handle_middle(self) -> None:
        if self.selected.is_selected:
            self.handle_down()
        else:
            self.handle_up()

    def update(self, timestamp, event: InputEvent = None) -> bool:
        self.should_redraw = False

        if event and event.action in [ACTION_PRESSED, ACTION_HELD]:
            self.handle_input.get(event.direction, self.handle_default)()
            self.last_update = timestamp

            self.should_redraw = True

        elif self.last_update + 0.2 < timestamp:
            self.left_arrow_x = self.x + 1
            self.right_arrow_x = self.x + self.width - 2

            self.last_update = timestamp
            self.should_redraw = True

        if self.should_redraw:
            self.update_buffer()

        return self.should_redraw

    def update_buffer(self) -> None:
        self.clear_buffer()

        for dy, line in enumerate(self.buffer, -1):
            line[self.left_arrow_x + abs(dy)] = self.color
            line[self.right_arrow_x - abs(dy)] = self.color
