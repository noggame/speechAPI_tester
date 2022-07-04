from itertools import zip_longest
import json
from Struct.Result import TestResult
from modules.Service.ResultAnalyzer.BaseResultAnalyzer import BaseResultAnalyzer
import logging
import config.cfgParser as cfg
from Struct.Vision.Image import RectangleBox
from Struct.Vision.FaceInfo import Face
from PIL import Image, ImageDraw


class FDResultAnalyzer(BaseResultAnalyzer):
    def __init__(self) -> None:
        super().__init__()
        self.resultStack = {
            'statistics' : {
                'numOfSamples' : 0,
                'accuracy_sum' : 0
            },
            'samples' : {}
        }
        ### samples
        # {
        #     'service': result.service,
        #     'expected': acc_expected,
        #     'actual': acc_actual,
        #     'metric': 'Jaccard Acc. with Rect. object',
        #     'accuracy': float(acc)
        # }


        # staticRepo = {
        #    "sample":35000,
        #    "KT_FaceDetect":{
        #       "expected":100,
        #       "actual":50,
        #       "matching":50
        #    },
        #    "Kakao_FaceDetect":{
        #       "expected":100,
        #       "actual":60,
        #       "matching":60
        #    }
        #   ...
        # }


    def analysisResultStack(self, resultList:list):
        """결과정보(resultList)를 분석해 (샘플수, 평균정확도) 결과 반환
        """
        for result in resultList:
            self._addResultToStack(result=result)

        samples = self.resultStack['statistics']['numOfSamples']
        accuracy_avg = round(float(self.resultStack['statistics']['accuracy_sum']/samples)*100, 2)

        return samples, accuracy_avg

    
    def _addResultToStack(self, result:TestResult):
        th_detection = float(cfg.get('vision', 'threshold_face_detection'))

        actualList = result.actual
        expectedList = result.expected
        jaccardScoreList = []

        for idx_act in range(len(actualList)): # for each actual
            eachActualJaccardScore = []

            for exp in expectedList:    # for each expected
                # 실제값 기준 각 기대값 박스와 매칭해보면서 자카드 유사도 계산 > 계산 결과 중 가장 유사도가 높은 배열 한 곳에 [idx, similarity] 값 저장
                act:dict = json.loads(actualList[idx_act])
                exp:dict = json.loads(exp)
                rect_act = RectangleBox(act.get('x'), act.get('y'), act.get('width'), act.get('height'))
                rect_exp = RectangleBox(exp.get('x'), exp.get('y'), exp.get('width'), exp.get('height'))
                jaccardScore = self._getJaccardSimirality(rect_act, rect_exp)

                eachActualJaccardScore.append(jaccardScore)

            jaccardScoreList.append(eachActualJaccardScore)

        bestResult:list = self._getBestJaccardScore(jaccardScoreList, cfg.get('vision', 'threshold_face_matching'))     # [[idx_actual, score]] * len(expectedList)

        accuracy = len([matching_rate for idx_act, matching_rate in bestResult if matching_rate > 0.5]) / len(expectedList)
        samples = self.resultStack['samples']
        samples[result.id] = {
            "service": result.service,
            "expected": expectedList,
            "actual": actualList,
            "metric": "Face Counting",
            "accuracy": float(accuracy)
        }

        statistics = self.resultStack['statistics']
        statistics['numOfSamples'] += 1
        statistics['accuracy_sum'] += float(accuracy)


        # _analysisRepo.addAnalysisData(testResult=result, bestResult=bestResult)
        logging.info("source = {}, MatchingResult = {}".format(result.source, bestResult))
        # print(result.source, bestResult)


        # TODO: FDResultAnalyzer : FaceDetection 분석 결과 저장
        ### make image
        # if record:
        #     fileName = str(result.source).split('/')
        #     fileName = fileName[len(fileName)-1]
        #     idx_Ext = str(fileName).rindex('.')
        #     saveFilePath = "{}/{}_{}{}".format(record, fileName[:idx_Ext], result.service, fileName[idx_Ext:])
        #     self._saveAnalizedImage(source=result.source, dest=saveFilePath, expectedList=expectedList, actualList=actualList, analysisResult=bestResult)
        #     logging.info("save image : {}".format(saveFilePath))


        ### 기대/인식 사람 얼굴 수 비교한 결과값 저장(record param.) 및 반환
        # return self.getStaticInfo(analysisData = _analysisRepo.getAnalysisRepo) 



    # def addAnalysisData(self, testResult:TestResult, bestResult:list):
    #     """ TestResult를 입력받아 분석하고, 분석 결과를 Analysis Reopistory에 저장 """
    #     # self._analysisResultDict = {}
        
        
    #     staticInfoList = []
            
    #     # collect static information
    #     numOfMatching = len([idx_act for [idx_act, score] in bestResult if idx_act != None])
    #     staticInfoList.append({
    #         "service": testResult.service,
    #         "expected": len(testResult.expected),
    #         "actual": len(testResult.actual),
    #         "matching": numOfMatching,
    #         "accuracy": numOfMatching/len(testResult.expected)
    #     })

    #     # store static data
    #     if testResult.id not in self._analysisResultDict:
    #         eachId = self._analysisResultDict[testResult.id] = {}   # set id
    #         eachId['source'] = testResult.source                    # set source
    #         eachId['statics'] = []                                  # init. static
        
    #     statics:list = self._analysisResultDict[testResult.id]['statics']
    #     statics.extend(staticInfoList)







### Image Processing
    def _saveAnalizedImage(self, source:str, dest:str, expectedList, actualList, analysisResult):
        ### init.
        img = Image.open(source)
        draw = ImageDraw.Draw(img)

        ### draw rectangle
        for face_expected_info, face_actual_info in zip_longest(expectedList, actualList):
            # expected
            if face_expected_info:
                face_expected = Face(x=face_expected_info['x'], y=face_expected_info['y'], width=face_expected_info['width'], height=face_expected_info['height'], gender=face_expected_info['gender'])
                draw.rectangle(xy=[(float(face_expected.x), float(face_expected.y)), (float(face_expected.x)+float(face_expected.width), float(face_expected.y)+float(face_expected.height))], outline="#00FF00FF")
            
            # actual
            if face_actual_info:
                face_actual = Face(x=face_actual_info['x'], y=face_actual_info['y'], width=face_actual_info['width'], height=face_actual_info['height'], gender=face_actual_info['gender'])
                draw.rectangle(xy=[(float(face_actual.x), float(face_actual.y)), (float(face_actual.x)+float(face_actual.width), float(face_actual.y)+float(face_actual.height))], outline="#0000FFFF")

            # # intersection
            # rect_intersection = self._getIntersection(coordinate_A = RectangleBox(x=face_expected.x, y=face_expected.y, width=face_expected.width, height=face_expected.height),
            #                                         coordinate_B= RectangleBox(x=face_actual.x, y=face_actual.y, width=face_actual.width, height=face_actual.height))
            # for line in self._getRectangleBoundaries(rect_intersection):
            #     draw.line(xy=line, fill="#00FFFFFF", width=2)
            # draw.text(xy=(rect_intersection.x, rect_intersection.y), text=str(round(score, 2)))

        # matching
        for face_matching_info in analysisResult:
            # face_matching_info and 
            if face_matching_info[0] != None:
                idx_act, score = face_matching_info
                face_matching = Face(x=actualList[idx_act]['x'], y=actualList[idx_act]['y'], width=actualList[idx_act]['width'], height=actualList[idx_act]['height'], gender=actualList[idx_act]['gender'])
                draw.rectangle(xy=[(float(face_matching.x), float(face_matching.y)), (float(face_matching.x)+float(face_matching.width), float(face_matching.y)+float(face_matching.height))], outline="#FF0000FF")
                draw.text(xy=(float(face_matching.x+5), float(face_matching.y+5)), text=str(round(score, 2)), align='left', fill="#FF0000FF")


        ### save
        img.save(dest)
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
            # 완전히 겹치는 경우 가로/세로 길이 계산도 cover
            W_i = (W_l + W_s - abs(X_diff) - abs(X_diff + W_l - W_s))/2
            H_i = (H_l + H_s - abs(Y_diff) - abs(Y_diff + H_l - H_s))/2
            _intersection = RectangleBox(x=X_i, y=Y_i, width=W_i, height=H_i)

        return _intersection


    def _getBestJaccardScore(self, jaccardScoreList:list, threshold:float) -> list:
        """N(actual) * N(expected) 배열을 입력받아, 각 열(actual)의 값들 중 Jaccard 유사도가 가장 높은 값을 선택해 [idx_actual, score] 데이터 형태로 모은 리스트를 반환\n
        @ 실제값과 기대값의 유사도가 0에 해당하는 데이터는 [None, 0]의 값으로 반환
        """

        ### Example
        #################################################################################
        # JaccardScoreList ------------------------------------------------------------
        #                 |    exp_01   |  exp_02   |  exp_03   ##   expIdxMatchingWith (EIMW)   
        # ----------------|-------------|-----------|-----------## -------------------- 
        #       act_01    |     0.1     |   0.2     |   0.7     ##   2 (idx of exp_03)
        #       act_02    |     0.8     |   0       |   0.3     ##   0 (idx of exp_01)
        #       ...                                             ##                      
        #################################################################################
        # bestJaccardScore|   [1, 0.8]  | [None, 0] | [0, 0.7]]
        #################################################################################

        if not jaccardScoreList:
            return []

        bestJaccardScore = []   # jaccardScoreList에서 실제 Rect.와 일치률이 높은 기대값의 Rect.와 매칭시킨 배열
        expIdxMatchingWith = [None] * len(jaccardScoreList)

        for idx_exp in range(len(jaccardScoreList[0])):     # for each expected (col.)
            bestJaccardScore.append([None, 0])              # [selected_actual_number, best_score]

            for idx_act in range(len(jaccardScoreList)):    # for each actual (row.)
                bestActIdx, bestScore = bestJaccardScore[idx_exp]
                curScore = jaccardScoreList[idx_act][idx_exp]

                if curScore > bestScore:    # TODO : FDResultAnalyzer : Threshold 값 보다 높은 경우에 매칭

                    if expIdxMatchingWith[idx_act] == None:
                        if bestActIdx == None:
                            # new value (해당 exp_rect 에 대해서 아직 매칭된 결과가 없는 경우)
                            bestJaccardScore[idx_exp] = [idx_act, curScore]
                            expIdxMatchingWith[idx_act] = idx_exp
                        else:
                            # update (해당 exp_rect 에 대해서 매칭된 결과가 있었으나, 다른 act_rect 와의 일치율이 더 높은 경우)
                            expIdxMatchingWith[bestActIdx] = None
                            expIdxMatchingWith[idx_act] = idx_exp
                            bestJaccardScore[idx_exp] = [idx_act, curScore]
                    else:
                        if curScore > jaccardScoreList[idx_act][expIdxMatchingWith[idx_act]]:
                            # update (해당 exp_rect 에 대해서 매칭된 결과가 있었으나, 다른 exp_rect 와의 매칭으로 이미 정의되었던 act_rect와의 매칭한 결과값이 더 높은 경우)
                            bestJaccardScore[expIdxMatchingWith[idx_act]] = [None, 0]
                            expIdxMatchingWith[idx_act] = idx_exp
                            bestJaccardScore[idx_exp] = [idx_act, curScore]
                            # TODO : FDResultAnalyzer : bestJaccardScore[expIdxMatchingWith[idx_act]] 의 값을 새로 쓰면서, expIdxMatchingWith[idx_act] 번째 기대값 항목에 대한 매칭을 새롭게 계산

        return bestJaccardScore
