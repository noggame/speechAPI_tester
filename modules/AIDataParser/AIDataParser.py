
class AIDataParser:
    def __init__(self, targetPath) -> None:
        self._targetPath = targetPath

    @property
    def targetPath(self):
        return self._targetPath

    @targetPath.setter
    def targetPath(self, targetPath):
        self._targetPath = targetPath

    def getTestDataList(self, targetPath:str=None, limit:int=0):
        _targetPath = self.targetPath if not targetPath else targetPath
        _testDataList = []

        # implements...

        return _testDataList

