class Color:
    def __init__(self, r: int = 0, g: int = 0, b: int = 0, brightness: int = 1):
        self._r = r
        self._g = g
        self._b = b
        self._brightness = brightness

    def __getitem__(self, item) -> int:
        return [self.r, self.g, self.b][item]

    def __len__(self) -> int:
        return 3

    @staticmethod
    def _clamp(value) -> int:
        return 0 if value < 0 else 255 if value > 255 else value

    @property
    def r(self) -> int:
        return int(self._r * self.brightness)

    @r.setter
    def r(self, value: int) -> None:
        self._r = self._clamp(value)

    @property
    def g(self) -> int:
        return int(self._g * self.brightness)

    @g.setter
    def g(self, value: int) -> None:
        self._g = self._clamp(value)

    @property
    def b(self) -> int:
        return int(self._b * self.brightness)

    @b.setter
    def b(self, value: int) -> None:
        self._b = self._clamp(value)

    @property
    def brightness(self) -> int:
        return self._brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        if not 0.0 <= value <= 1.0:
            raise ValueError("brightness must be between values of 0.0 and 1.0")
        self._brightness = value
