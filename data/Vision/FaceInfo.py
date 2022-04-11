

class Face:
    def __init__(self, x, y, gender) -> None:
        self._x = x
        self._y = y
        self._gender = gender

    def __repr__(self) -> str:
        return repr((self._x, self._y, self._gender))

    def __str__(self) -> str:
        return "x={}, y={}, gender={}".format(self._x, self._y, self._gender)

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    @property
    def gender(self):
        return self._gender