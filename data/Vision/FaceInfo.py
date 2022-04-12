

class Face:
    def __init__(self, x, y, width, height, gender) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._gender = gender

    def __repr__(self) -> str:
        return repr((self._x, self._y, self._width, self._height, self._gender))

    def __str__(self) -> str:
        return f'{{"x":{self._x}, "y":{self._y}, "width":{self._width}, "height":{self._height}, "gender":"{self._gender}"}}'
    
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

    @property
    def gender(self):
        return self._gender