from .component import Component
from .color import Color


class Screen:
    def __init__(self, width: int = 8, height: int = 8,
                 background: Color = Color(0, 0, 0)) -> None:
        self.width = width
        self.height = height
        self.screen = [[background] * self.height for _ in range(self.height)]

    def flatten(self) -> list:
        """ Makes the 2d screen list to 1d list"""
        return [item for sublist in self.screen for item in sublist]

    def component_to_screen(self, component: Component) -> None:
        """ Performs checks and adds components to screen. """
        if not isinstance(component, Component):
            raise ValueError("component must be subclass of Component")

        # no need to modify screen if component not on screen
        if any([component.x > self.width,
                component.y > self.height,
                component.x + component.width - 1 < 0,
                component.y + component.height - 1 < 0]):
            return

        # loop through components buffer and add pixel to screen if pixel in screen
        for dy, pixel_row in enumerate(component.buffer):
            for dx, pixel in enumerate(pixel_row):
                on_screen_y = dy + component.y
                on_screen_x = dx + component.x

                if 0 <= on_screen_y < self.height and 0 <= on_screen_x < self.width:
                    self.screen[on_screen_y][on_screen_x] = pixel

    def __iadd__(self, other):
        self.component_to_screen(other)
        return self
