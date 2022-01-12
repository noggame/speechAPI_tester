import logging
import json
from data.TestData import TestData

from modules.AIDataParser.AIDataParser import AIDataParser

class ClovaAIParser(AIDataParser):

    def __init__(self, targetPath) -> None:
        super().__init__(targetPath)

    def getTestDataList(self, targetPath: str = None, limit: int = 0):
        _targetPath = self.targetPath if not targetPath else targetPath
        _testDataList = []
        _numOftd = 0

        # json 파일 정보 파싱
        try:
            ansewerFile = open(f'{_targetPath}/train_ClovaCall.json', 'r').readline()

            for expectedInfo in json.loads(ansewerFile):
                if limit > 0 and _numOftd >= limit:  # limit number of test dataset
                    break

                # get data
                wav, expected, speakerId = expectedInfo['wav'], expectedInfo['text'], expectedInfo['speaker_id']

                # # except [number & digit]
                # if re.findall('[a-zA-Z0-9]+', expected):    
                #     continue

                td = TestData(id=wav[:-4], expectedList=[expected], sampleFilePath=f'{_targetPath}/wavs_train/{wav}')
                _testDataList.append(td)

                # inc.
                _numOftd +=1

        except FileNotFoundError:
            logging.error('[ERR] ClovaAIParser - ANswerFile not found. check the target path')

        return _testDataList
