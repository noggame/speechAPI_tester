import re



class Category:
    def __init__(self) -> None:
        self._type = None
        self._count = 0

    @property
    def type(self):
        return self._type

    @property
    def count(self):
        return self._count

    @type.setter
    def type(self, type):
        self._type = type

    def increment(self):
        self._count += 1


ll = {}

for cName in ['c1', 'c2', 'c1', 'c3']:

    if not ll.get(cName):
        ll[cName] = 1
    else:
        ll[cName] += 1


print(ll)