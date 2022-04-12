import csv
from data.TestData import TestData
from modules.DataParser.AIDataParser import AIDataParser

class FaceCountingParser(AIDataParser):
    def __init__(self, targetFile=None) -> None:
        super().__init__(targetFile)

    def getTestDataList(self, targetPath: str = None, limit: int = 0):
        _targetPath = self.targetPath if not targetPath else targetPath
        _testDataList = []
        _numOftd = 0

        # json 파일 정보 파싱
        try:
            answerFile = open(f'{_targetPath}/train.csv', 'r')
            csvData = csv.reader(answerFile)

            next(csvData)  # pass header

            # get data
            for name, num in csvData:
                if limit > 0 and _numOftd >= limit:  # limit number of test dataset
                    break

                id = name
                target_img = f'{_targetPath}/image_data/{name}'
                expectedValue = num

                # @@@@@@@@@@@@@ 좌표를 입력받으려면 (x, y, width, height)를 입력받도록 수정 필요
                td = TestData(id=id, expectedList=[expectedValue], sampleFilePath=target_img)
                _testDataList.append(td)

                _numOftd += 1

            answerFile.close()

        except:
            print("[Error] fail to parsing face_data.")
            # logging.error('[ERR] ClovaAIParser - ANswerFile not found. check the target path')

        return _testDataList
