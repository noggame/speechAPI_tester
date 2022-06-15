
from abc import abstractclassmethod, abstractmethod

from Struct.Result import TestResult


class BaseResultAnalyzer():
    def __init__(self) -> None:
        self.resultStack = {}

    @property
    def getResultStack(self):
        return self.resultStack

    @abstractmethod
    def analysisResultStack(self, resultList:list, filter:list=None):
        pass

    @abstractmethod
    def _addResultToStack(self, result:TestResult):
        pass


