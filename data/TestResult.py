
from typing import List


class TestResult:
    def __init__(self, id, service, source, expected:list, actual:list) -> None:
        self._id = id
        self._source = source
        self._service = service
        self._expected = expected
        self._actual = actual

        # self._accuracy = accuracy
        # self._categories = categories

    def __str__(self) -> str:
        result_json = '{'                                   # open json
        result_json += f'"id": "{self.id}"'
        result_json += f', "source": "{self.source}"'
        result_json += f', "service": "{self.service}"'   # publisher
        
        result_json += f', "expected": ['
        expectedList = []
        for exp in self._expected:
            expectedList.append(f'"{exp}"')
        expectedList = ', '.join(expectedList)
        result_json += f'{expectedList}]'

        result_json += f', "actual": ['
        actualList = []
        for act in self._actual:
            actualList.append(f'"{act}"')
        actualList = ', '.join(actualList)
        result_json += f'{actualList}]'


        # result_str += f'[Expected] : {self.expected}'
        # result_str += f'[Actual] : {self.actual}\n'
        # result_str += f'[Accuracy] : {self.accuracy}\n'
        # result_str += f'[Categories] : {self.categories}'

        result_json += '}'                                  # close json
        return result_json
        
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
    def expected(self) -> list:
        return self._expected

    @property
    def actual(self) -> list:
        return self._actual

    # @property
    # def accuracy(self):
    #     return self._accuracy

    # @property
    # def categories(self):
    #     return self._categories

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
    def expected(self, expected:list):
        self._expected = expected

    @actual.setter
    def actual(self, actual:list):
        self._actual = actual

    # @accuracy.setter
    # def accuracy(self, accuracy):
    #     self._accuracy = accuracy

    # @categories.setter
    # def categories(self, categories:List):
    #     self._categories = categories