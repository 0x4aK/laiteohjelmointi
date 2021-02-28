from time import time

from sense_hat import InputEvent

from .color import Color


class Component:
    def __init__(self, x: int, y: int, width: int, height: int,
                 color: Color = Color(255, 255, 255),
                 background: Color = Color(0, 0, 0)) -> None:
        self.x = x
        self.y = y

        self.color = color
        self.background = background

        self.buffer = [[self.background] * width for _ in range(height)]
        self.last_update = time()
        self.should_redraw = False

        self.handle_input = {"left": self.handle_left,
                             "right": self.handle_right,
                             "up": self.handle_up,
                             "down": self.handle_down,
                             "middle": self.handle_middle}

    @property
    def width(self) -> int:
        return len(self.buffer[0])

    @property
    def height(self) -> int:
        return len(self.buffer)

    def update(self, timestamp, event: InputEvent = None) -> bool:
        """
        Handles events that are passed to the Component.
        Must be implemented in child components.
        return True if component should redraw.
        """
        raise NotImplemented("User must provide update function")

    def update_buffer(self) -> None:
        """
        Logic that defines how the component will look on screen.
        """

    def clear_buffer(self) -> None:
        """
        Makes a new clean buffer
        """
        self.buffer = [[self.background] * self.width for _ in range(self.height)]

    def handle_left(self) -> None:
        pass

    def handle_right(self) -> None:
        pass

    def handle_up(self) -> None:
        pass

    def handle_down(self) -> None:
        pass

    def handle_middle(self) -> None:
        pass

    def handle_default(self) -> None:
        pass
