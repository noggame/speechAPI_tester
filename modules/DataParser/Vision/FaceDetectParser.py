import csv
from data.TestData import TestData
from data.Vision.FaceInfo import Face
from modules.DataParser.AIDataParser import AIDataParser

class FaceCountingParser(AIDataParser):
    def __init__(self, targetFile=None) -> None:
        super().__init__(targetFile)

    def getTestDataList(self, targetPath: str = None, limit: int = 0):
        _targetPath = self.targetPath if not targetPath else targetPath
        _testDataList = []
        _numOftd = 1


        ### face box
        boxFile = open(f'{_targetPath}/bbox_train.csv', 'r')
        csvData = csv.reader(boxFile)
        next(csvData)  # pass header

        # get data
        prev_name = None
        faceList = []
        for name, width, height, xmin, ymin, xmax, ymax in csvData:

            if name != prev_name and prev_name:
                if limit > 0 and _numOftd >= limit: # limit number of test dataset
                    break
                else:
                    _numOftd += 1

                faceList.sort(key=lambda m: m.x)
                td = TestData(id=prev_name, expectedList=faceList, sampleFilePath=f'{_targetPath}/image_data/{prev_name}')
                _testDataList.append(td)
                # init.
                faceList = []
            
            prev_name = name
            faceList.append(Face(x=xmin, y=ymin, width=int(xmax)-int(xmin), height=int(ymax)-int(ymin), gender=None))

        # end of line
        faceList.sort(key=lambda m: m.x)
        td = TestData(id=prev_name, expectedList=faceList, sampleFilePath=f'{_targetPath}/image_data/{prev_name}')
        _testDataList.append(td)

        boxFile.close()

        # except:
        #     print("[Error] fail to parsing face_data.")
            # logging.error('[ERR] ClovaAIParser - ANswerFile not found. check the target path')

        return _testDataList
