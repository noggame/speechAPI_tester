

class RectangleBox:
    def __init__(self, x, y, width, height) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __repr__(self) -> str:
        return repr((self._x, self._y, self._width, self._height))

    def __str__(self) -> str:
        return f'{{"x":{self._x}, "y":{self._y}, "width":{self._width}, "height":{self._height}"}}'