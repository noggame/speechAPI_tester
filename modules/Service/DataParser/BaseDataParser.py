


from abc import ABC, abstractmethod

class BaseDataParser(ABC):
    def __init__(self, targetPath:str=None) -> None:
        self._targetPath = targetPath

    @property
    def targetPath(self):
        return self._targetPath

    @targetPath.setter
    def targetPath(self, targetPath):
        self._targetPath = targetPath

    @abstractmethod
    def getTestDataList(self, targetPath:str=None, limit:int=0):
        """
        limit : 테스트데이터 개수 제한, default 값은 0으로 전체 데이터 사용
        """
        _targetPath = self.targetPath if not targetPath else targetPath
        _testDataList = []

        # implements...
        

        return _testDataList

