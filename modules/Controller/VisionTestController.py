from audioop import minmax
import json
from re import L, X
from data.Vision.FaceInfo import Face
from data.Vision.Image import RectangleBox
from modules.DataParser.AIDataParser import AIDataParser
from modules.APICaller.APICaller import APICaller
from data.TestData import TestData
from data.TestResult import TestResult
from modules.Controller.TestController import TestController
import logging
from PIL import Image, ImageDraw
import config.cfgParser as cfg

class FaceTestController(TestController):
    def __init__(self) -> None:
        super().__init__()

    def startRequest(self, limit:int=0, record:str=None):
        _testResultList = []
        file_record = open(record, 'w') if record else None

        # get target_data/path
        for eachDataParser in self._dataList:
            dataParser:AIDataParser = eachDataParser

            # get samples from target_data/path
            cnt=1
            # for sample in dataParser.getTestDataList(limit=limit):
            for sample in dataParser.getTestDataList(limit=limit):
                td:TestData = sample
                print("[{}] {}".format(cnt, td.sampleFilePath))
                cnt+=1

                # request API
                for eachAPI in self._apiList:
                    api:APICaller = eachAPI

                    actualResult:list = api.request(targetFile=td.sampleFilePath)   # = faceList
                    testResult:TestResult = TestResult(id=td.id,
                                                        service=api.__class__.__name__,
                                                        source=td.sampleFilePath,
                                                        expected=td.expectedList,
                                                        actual=actualResult)
                    _testResultList.append(testResult)

                    # recording
                    if file_record:
                        file_record.write(str(testResult))
                        file_record.write("\n")
                    logging.info(str(testResult))

                    print("expected = {}, actual = {}".format(len(td.expectedList), len(actualResult)))
        
        file_record.close()

        return _testResultList


    def startAnalysis(self, accuracyFilter:list=None, categoryFilter:list=None, resultList:list=None, targetFile:str=None, record:str=None):
        _expectedList = []
        _resultList = []
        _analysisResultList = []
        th_detection = float(cfg.get('vision', 'threshold_face_dectection'))

        ### get resultList
        if resultList:
            _resutlList = resultList
        elif targetFile:    # get resultList from file
            resultFile = open(targetFile, 'r')

            for result in resultFile.readlines():
                result = json.loads(result)
                _resultList.append(TestResult(result['id'], result['service'], result['source'], result['expected'], result['actual']))

            resultFile.close()
        else:
            # logging.exception(f'[Exception] {__class__.__name__}:{__name__} - result data is empty')
            print("not found result data")


        ### Anaysis result
        for result in _resultList:  # type(result) = TestResult
            result:TestResult = result
            actualList = result.actual
            expectedList = result.expected
            jaccardScoreList = []

            for idx_act in range(len(actualList)): # for each actual
                eachActualJaccardScore = []

                for exp in expectedList:
                    # TODO: 실제값 기준 각 기대값 박스와 매칭해보면서 자카드 유사도 계산 > 계산 결과 중 가장 유사도가 높은 배열 한 곳에 [idx, similarity] 값 저장
                    act:dict = actualList[idx_act]
                    exp:dict = exp
                    rect_act = RectangleBox(act.get('x'), act.get('y'), act.get('width'), act.get('height'))
                    rect_exp = RectangleBox(exp.get('x'), exp.get('y'), exp.get('width'), exp.get('height'))
                    jaccardScore = self._getJaccardSimirality(rect_act, rect_exp)

                    eachActualJaccardScore.append(jaccardScore)

                jaccardScoreList.append(eachActualJaccardScore)

            bestResult = self._getBestJaccardScore(jaccardScoreList, cfg.get('vision', 'threshold_face_dectection'))     # [[idx_actual, score]] * len(expectedList)
            _analysisResultList.append(bestResult)


            ### make image
            if record:
                self._saveAnalizedImage(result.source, record, expectedList, actualList, bestResult)

        return _analysisResultList


    def _saveAnalizedImage(self, source:str, record_path:str, expectedList, actualList, analysisResult):
        ### init.
        img = Image.open(source)
        draw = ImageDraw.Draw(img)

        ### draw rectangle
        for face_expected, [idx_act, score] in zip(expectedList, analysisResult):
            # expected
            face_expected = Face(x=face_expected['x'], y=face_expected['y'], width=face_expected['width'], height=face_expected['height'], gender=face_expected['gender'])
            draw.rectangle(xy=[(float(face_expected.x), float(face_expected.y)), (float(face_expected.x)+float(face_expected.width), float(face_expected.y)+float(face_expected.height))], outline="#00FF00FF")

            # actual
            face_actual = Face(x=actualList[idx_act]['x'], y=actualList[idx_act]['y'], width=actualList[idx_act]['width'], height=actualList[idx_act]['height'], gender=actualList[idx_act]['gender'])
            draw.rectangle(xy=[(float(face_actual.x), float(face_actual.y)), (float(face_actual.x)+float(face_actual.width), float(face_actual.y)+float(face_actual.height))], outline="#FF0000FF")
            draw.text(xy=(float(face_actual.x+5), float(face_actual.y+5)), text=str(round(score, 2)), align='left', fill="#FF0000FF")

            # # intersection
            # rect_intersection = self._getIntersection(coordinate_A = RectangleBox(x=face_expected.x, y=face_expected.y, width=face_expected.width, height=face_expected.height),
            #                                         coordinate_B= RectangleBox(x=face_actual.x, y=face_actual.y, width=face_actual.width, height=face_actual.height))
            # for line in self._getRectangleBoundaries(rect_intersection):
            #     draw.line(xy=line, fill="#00FFFFFF", width=2)
            # draw.text(xy=(rect_intersection.x, rect_intersection.y), text=str(round(score, 2)))


        ### save
        fileName = source.split('/')
        fileName = fileName[len(fileName)-1]
        idx_Ext = str(fileName).rindex('.')

        img.save("{}/{}_rec{}".format(record_path, fileName[:idx_Ext], fileName[idx_Ext:]))
        img.close()


    def _getRectangleBoundaries(self, rectangle:RectangleBox):
        x = rectangle.x
        y = rectangle.y
        w = rectangle.width
        h = rectangle.height

        top = ((x, y), (x+w, y))
        left = ((x, y), (x, y+h))
        bottom = ((x+w, y+h), (x, y+h))
        right = ((x+w, y+h), (x+w, y))
        
        return [top, bottom, left, right]



    def _getJaccardSimirality(self, coordinate_A:RectangleBox, coordinate_B:RectangleBox) -> float:
        """입력받은 두 RectangleBox의 Jaccard 유사도값을 계산해 반환
        @if completly overlap, return 1
        @if not found, return 0
        """

        jaccard = 0

        intersection:RectangleBox = self._getIntersection(coordinate_A, coordinate_B)

        if intersection:
            area_A = coordinate_A.width * coordinate_A.height
            area_B = coordinate_B.width * coordinate_B.height
            area_I = intersection.width * intersection.height
            jaccard = area_I / (area_A + area_B - area_I)

        return jaccard


    def _getIntersection(self, coordinate_A:RectangleBox, coordinate_B:RectangleBox) -> RectangleBox:
        """입력받은 두 RectangleBox의 교집합(Intersection) 정보를 담고 있는 RectangleBox 개체 반환\n
        @if not found, return None
        """

        _intersection:RectangleBox = None

        ### get coordinate(X, Y), length(Width/Height) information
        # s=short, l=long (distance from zero point of axis x/y)
        X_s, X_l, Y_s, Y_l = None, None, None, None
        W_s, H_s, W_l, H_l = None, None, None, None
        if coordinate_A.x >= coordinate_B.x:
            X_s = coordinate_B.x
            X_l = coordinate_A.x
            W_s = coordinate_B.width
            W_l = coordinate_A.width
        else:
            X_s = coordinate_A.x
            X_l = coordinate_B.x
            W_s = coordinate_A.width
            W_l = coordinate_B.width

        if coordinate_A.y >= coordinate_B.y:
            Y_s = coordinate_B.y
            Y_l = coordinate_A.y
            H_s = coordinate_B.height
            H_l = coordinate_A.height
        else:
            Y_s = coordinate_A.y
            Y_l = coordinate_B.y
            H_s = coordinate_A.height
            H_l = coordinate_B.height

        
        ### check overlap
        X_diff = X_l - X_s
        Y_diff = Y_l - Y_s
        if X_diff < W_s and Y_diff < H_s:   # check overlap
            X_i = X_l
            Y_i = Y_l
            # TODO: 완전히 겹치는 경우 가로/세로 길이 계산도 cover 가능해야함
            W_i = (W_l + W_s - abs(X_diff) - abs(X_diff + W_l - W_s))/2
            H_i = (H_l + H_s - abs(Y_diff) - abs(Y_diff + H_l - H_s))/2
            # W_i = X_s + W_s - X_l
            # H_i = Y_s + H_s - Y_l
            _intersection = RectangleBox(x=X_i, y=Y_i, width=W_i, height=H_i)

        return _intersection


    def _getBestJaccardScore(self, jaccardScoreList:list, threshold:float) -> list:
        """N(actual) * N(expected) 배열을 입력받아, 각 열(actual)의 값들 중 Jaccard 유사도가 가장 높은 값을 선택해 [idx_actual, score] 데이터 형태로 모은 리스트를 반환\n
        @ 실제값과 기대값의 유사도가 0에 해당하는 데이터는 [None, 0]의 값으로 반환
        """
        if not jaccardScoreList:
            return None

        # print(*jaccardScoreList, sep="\n")

        bestJaccardScore = []
        chosen = [False] * len(jaccardScoreList)

        for idx_exp in range(len(jaccardScoreList[0])):      # length of num(expected)
            bestJaccardScore.append([None, 0])

            for idx_act in range(len(jaccardScoreList)):
                eachScore = jaccardScoreList[idx_act][idx_exp]

                # update [idx, score]
                if not chosen[idx_act] and eachScore > bestJaccardScore[idx_exp][1]:
                    prev_chosen_idx = bestJaccardScore[idx_exp][0]

                    if prev_chosen_idx != None:
                        chosen[prev_chosen_idx] = False

                    chosen[idx_act] = True
                    bestJaccardScore[idx_exp][0] = idx_act
                    bestJaccardScore[idx_exp][1] = eachScore

        # print(f" >>> {bestJaccardScore}")

        return bestJaccardScore