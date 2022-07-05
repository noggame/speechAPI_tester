import logging
import json
from Struct.TestData import TestData
from modules.Service.DataParser.BaseDataParser import BaseDataParser


class ClovaAIParser(BaseDataParser):

    def __init__(self, targetPath:str=None) -> None:
        super().__init__(targetPath)

    def getTestDataList(self, targetPath: str = None, limit: int = 0):
        _targetPath = self.targetPath if not targetPath else targetPath
        _testDataList = []
        _numOftd = 0

        # json 파일 정보 파싱
        try:
            answerFile = open(f'{_targetPath}/train_ClovaCall.json', 'r').readline()

            for expectedInfo in json.loads(answerFile):
                if limit > 0 and _numOftd >= limit:  # limit number of test dataset
                    break

                # get data
                wav, expected, speakerId = expectedInfo['wav'], expectedInfo['text'], expectedInfo['speaker_id']
                td = TestData(id=wav[:-4], expectedList=[f"\"{expected}\""], sampleFilePath=f'{_targetPath}/wavs_train/{wav}')
                _testDataList.append(td)

                # inc.
                _numOftd +=1

        except FileNotFoundError:
            logging.error('[ERROR] ClovaAIParser - target file not found. check the path {}'.format(_targetPath))
        except:
            logging.error('[ERROR] ClovaAIParser - unexpected error occured.')

        return _testDataList
