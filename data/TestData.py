
class TestData:
    def __init__(self, id, expectedList, sampleFilePath) -> None:
        self._id = id
        self._expectedList = expectedList
        self._sampleFilePath = sampleFilePath

    def __str__(self) -> str:
        # id
        result = f'ID : {self._id}\n'
        
        # expectedList
        result += 'Expected : ['
        for i in range(len(self._expectedList)):
            result += f', "{self._expectedList[i]}"' if i > 0 else f'"{self._expectedList[i]}"'
        result += ']\n'

        # sampleFilePath
        result += f'SampleFilePath : {self._sampleFilePath}'

        return result


    @property
    def id(self):
        return self._id

    @property
    def expectedList(self):
        return self._expectedList

    @property
    def sampleFilePath(self):
        return self._sampleFilePath

    @id.setter
    def id(self, id):
        self._id = id

    @expectedList.setter
    def expectedList(self, expectedList):
        self._expectedList = expectedList
        
    @sampleFilePath.setter
    def sampleFilePath(self, sampleFilePath):
        self._sampleFilePath = sampleFilePath