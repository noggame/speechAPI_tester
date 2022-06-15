import AIDataParser
import os

from data.TestData import TestData

class KC(AIDataParser):
    def __init__(self) -> None:
        super().__init__()

    def getTestDataList(self, targetPath:str=None, limit:int=0):
        _targetPath = self.targetPath if not targetPath else targetPath
        _testDataList = []

        for root, dirs, files in os.walk(_targetPath):
            for file in files:

                if file.endswith(('.png')):
                    dirPathSplit = root.split('/')
                    id_pre = dirPathSplit[len(dirPathSplit)-1]
                    
                    td = TestData(id=f'{id_pre}_{file}', expectedList='temp', sampleFilePath=root)

        
# # get data
#         wav, expected, speakerId = expectedInfo['wav'], expectedInfo['text'], expectedInfo['speaker_id']
#         td = TestData(id=wav[:-4], expectedList=[expected], sampleFilePath=f'{_targetPath}/wavs_train/{wav}')
#         _testDataList.append(td)

        return _testDataList

