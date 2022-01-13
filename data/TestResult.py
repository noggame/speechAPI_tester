
from typing import List


class TestResult:
    def __init__(self, id, service, source, expected, actual, accuracy, categories:List) -> None:
        self._id = id
        self._source = source
        self._service = service
        self._expected = expected
        self._actual = actual
        self._accuracy = accuracy
        self._categories = categories

    def __str__(self) -> str:
        result_str = f'[ID] : {self.id}\n'
        result_str += f'[Source] : {self.source}\n'
        result_str = f'[Service] : {self.service}\n'
        result_str += f'[Expected] : {self.expected}\n'
        result_str += f'[Actual] : {self.actual}\n'
        result_str += f'[Accuracy] : {self.accuracy}\n'
        result_str += f'[Categories] : {self.categories}'

        return result_str
        
    @property
    def id(self):
        return self._id

    @property
    def source(self):
        return self._source

    @property
    def service(self):
        return self._service

    @property
    def expected(self):
        return self._expected

    @property
    def actual(self):
        return self._actual

    @property
    def accuracy(self):
        return self._accuracy

    @property
    def categories(self):
        return self._categories

    @id.setter
    def id(self, id):
        self._id = id

    @service.setter
    def service(self, service):
        self._service = service

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

    @categories.setter
    def categories(self, categories:List):
        self._categories = categories