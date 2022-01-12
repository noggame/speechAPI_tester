
class TestResultUnified:

    def __init__(self) -> None:
        self._source = None
        self._expected = None
        self._categories = set()
        self._actual = {}
        self._accuracy = {}

    @property
    def source(self):
        return self._source
    @property
    def expected(self):
        return self._expected
    @property
    def categories(self):
        return self._categories
    @property
    def actual(self):
        return self._actual
    @property
    def accuracy(self):
        return self._accuracy

    @source.setter
    def source(self, source):
        self._source = source
    @expected.setter
    def expected(self, expected):
        self._expected = expected
    @actual.setter
    def actual(self, actual):
        self._actual = actual
    @accuracy.setter
    def accuracy(self, accuracy):
        self._accuracy = accuracy
    def addCategories(self, categories):
        for ct in categories:
            self._categories.add(ct)

    
    