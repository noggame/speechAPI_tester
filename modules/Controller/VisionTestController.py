# from audioop import minmax
# from inspect import iscoroutine
from datetime import datetime
from itertools import zip_longest
import json
import os
# from re import L, X
from data.Vision.FaceInfo import Face
from data.Vision.Image import RectangleBox
from Struct.Result.BaseResultRepository import FaceResultRepository
from modules.APICaller.Vision.KT_FaceDetect import KT_FaceAPI
from modules.APICaller.Vision.Kakao_FaceDetect import Kakao_FaceAPI
from modules.DataParser.DataParser import DataParser
from modules.APICaller.APICaller import APICaller
from data.TestData import TestData
from data.Result import TestResult
from modules.Controller.TestController import TestController
import logging
from PIL import Image, ImageDraw
import config.cfgParser as cfg
from modules.DataParser.Vision.FaceDetectParser import FaceCountingParser

class FaceTestController(TestController):
    def __init__(self) -> None:
        super().__init__()


    def startTestAndAnalysis(self, data_name, api_name, number=0):
        """
        API Test and Analysis method
        """
        ### create ID with time
        now = datetime.now()
        current_time = now.strftime("%Y%m%d_%H%M%S_")
        time_stamp = str(current_time)+str(now.microsecond)

        ### Environment
        filePath = {}
        filePath['log'] = "{}/log_{}.log".format(cfg.get("system","log_dir"), time_stamp)
        filePath['result'] = "{}/result_faceDetection_{}.log".format(cfg.get("system","result_dir"), time_stamp)
        # filePath['analysis'] = f'{os.getcwd()}/logs/analysis_faceDetection_{time_stamp}.log'  # TODO: 결과 로그파일 저장
        filePath['resultImgaeDir'] = cfg.get("system","output_dir")
        # f'{os.getcwd()}/sample/vision/face_counting_challenge/temp_resultImage'
        logging.basicConfig(filename=filePath['log'], level=logging.DEBUG, format='%(asctime)s %(message)s') # set Log
        target_data = self.__setTestData(data_name)     # set Data (target)
        target_api = self.__setAPICaller(api_name)      # set API
        if target_data == None or target_api == None:
            return None


        ### STT API 호출 및 결과 저장
        sttResultList = self.startRequest(limit=number, record=filePath['result'])    # number개의 샘플 테스트


        ### 테스트 결과 파일 불러와 결과 반환
        analysisResultList = self.startAnalysis(targetFile = filePath['result'], record = filePath['resultImgaeDir'])


        return analysisResultList


    def startRequest(self, limit:int=0, record:str=None):
        _testResultList = []
        file_record = open(record, 'w') if record else None

        # get target_data/path
        for eachDataParser in self._dataList:
            dataParser:DataParser = eachDataParser

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

                    print("{} >> expected = {}, actual = {}".format(api.__class__.__name__, len(td.expectedList), len(actualResult)))
        
        file_record.close()

        return _testResultList


    def startAnalysis(self, accuracyFilter:list=None, categoryFilter:list=None, resultList:list=None, targetFile:str=None, record:str=None):
        _resultList = []
        _analysisRepo = FaceResultRepository()
        th_detection = float(cfg.get('vision', 'threshold_face_detection'))


        ### get resultList
        if resultList:
            _resultList = resultList
        elif targetFile:    # get resultList from file
            resultFile = open(targetFile, 'r')

            for result in resultFile.readlines():
                result = json.loads(result)
                _resultList.append(TestResult(result['id'], result['service'], result['source'], result['expected'], result['actual']))

            resultFile.close()
        else:
            logging.exception(f'[Exception] {__class__.__name__}:{__name__} - result data is empty')
            print("not found result data")


        ### Anaysis result
        for result in _resultList:  # for each picture
            result:TestResult = result
            actualList = result.actual
            expectedList = result.expected
            jaccardScoreList = []

            for idx_act in range(len(actualList)): # for each actual
                eachActualJaccardScore = []

                for exp in expectedList:    # for each expected
                    # 실제값 기준 각 기대값 박스와 매칭해보면서 자카드 유사도 계산 > 계산 결과 중 가장 유사도가 높은 배열 한 곳에 [idx, similarity] 값 저장
                    act:dict = actualList[idx_act]
                    exp:dict = exp
                    rect_act = RectangleBox(act.get('x'), act.get('y'), act.get('width'), act.get('height'))
                    rect_exp = RectangleBox(exp.get('x'), exp.get('y'), exp.get('width'), exp.get('height'))
                    jaccardScore = self._getJaccardSimirality(rect_act, rect_exp)

                    eachActualJaccardScore.append(jaccardScore)

                jaccardScoreList.append(eachActualJaccardScore)

            bestResult = self._getBestJaccardScore(jaccardScoreList, cfg.get('vision', 'threshold_face_matching'))     # [[idx_actual, score]] * len(expectedList)
            _analysisRepo.addAnalysisData(testResult=result, bestResult=bestResult)
            logging.info("source = {}, MatchingResult = {}".format(result.source, bestResult))
            # print(result.source, bestResult)

            ### make image
            if record:
                fileName = str(result.source).split('/')
                fileName = fileName[len(fileName)-1]
                idx_Ext = str(fileName).rindex('.')
                saveFilePath = "{}/{}_{}{}".format(record, fileName[:idx_Ext], result.service, fileName[idx_Ext:])
                self._saveAnalizedImage(source=result.source, dest=saveFilePath, expectedList=expectedList, actualList=actualList, analysisResult=bestResult)
                logging.info("save image : {}".format(saveFilePath))


        ### 기대/인식 사람 얼굴 수 비교한 결과값 저장(record param.) 및 반환
        return self.getStaticInfo(analysisData = _analysisRepo.getAnalysisRepo) # TODO: Vision - FaceDetection 분석 결과 저장


    def getStaticInfo(self, accuracyFilter:list=None, categoryFilter:list=None, analysisData:dict=None, targetFile:str=None, record:str=None):
        staticRepo = {"sample": 0}
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


        ### analysis data
        for id in analysisData:
            staticRepo['sample'] += 1

            for static in analysisData[id]['statics']:
                service = static['service']

                if service not in staticRepo:
                    staticRepo[service] = {'expected':0, 'actual':0, 'matching':0}
                
                staticRepo[service]['expected'] += static['expected']
                staticRepo[service]['actual'] += static['actual']
                staticRepo[service]['matching'] += static['matching']


        ### Result formating
        result = "---------------------------\n"
        result += "Result of Face Detection"
        for static in staticRepo:
            if static == 'sample':
                result += f" (sample : {staticRepo[static]})\n"
                result += "---------------------------\n"
                continue

            exp = staticRepo[static]['expected']
            act = staticRepo[static]['actual']
            mat = staticRepo[static]['matching']
            acc = round(mat/exp*100, 2)
            result += "{} : ACC = {} % (exp:{}, act:{}, mat:{})\n".format(static, str(acc).ljust(5), exp, act, mat)

        return result























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

                if curScore > bestScore:    # TODO : Threshold 값 보다 높은 경우에 매칭

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
                            # TODO : bestJaccardScore[expIdxMatchingWith[idx_act]] 의 값을 새로 쓰면서, expIdxMatchingWith[idx_act] 번째 기대값 항목에 대한 매칭을 새롭게 계산

        return bestJaccardScore


    def __setTestData(self, data_name):
        target_data = None

        if data_name == 'FaceCounting':
            target_data = FaceCountingParser(targetFile=f"{os.getcwd()}/sample/vision/face_counting_challenge")   # FaceCounting
            # target_data = ClovaAIParser(f'{os.getcwd()}/sample/voice/stt/ClovaCall')   # ClovaAI

        if target_data:
            self.addTestData(target_data)
        
        return target_data


    def __setAPICaller(self, api_name):
        target_api = None

        if api_name == 'KT':
            target_api = KT_FaceAPI(url=cfg.get('kt', 'url_face'), options={"threshold":0.5})

        elif api_name == 'Kakao':
            target_api = Kakao_FaceAPI(url=cfg.get('kakao', 'url_face'), key=cfg.get('kakao', 'key_sdh'))

        if target_api:
            self.addAPICaller(target_api)

        return target_api