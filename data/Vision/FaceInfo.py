from data.Vision.Image import RectangleBox

class Face(RectangleBox):
    def __init__(self, x, y, width, height, gender) -> None:
        super().__init__(x, y, width, height)
        self._gender = gender

    def __repr__(self) -> str:
        return repr((self._x, self._y, self._width, self._height, self._gender))

    def __str__(self) -> str:
        return f'{{"x":{self._x}, "y":{self._y}, "width":{self._width}, "height":{self._height}, "gender":"{self._gender}"}}'

    @property
    def gender(self):
        return self._gender