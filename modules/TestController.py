import logging
import re
from typing import Set
from data.TestData import TestData
from data.TestResult import TestResult
from data.Vision.FaceInfo import Face
from modules.DataParser.AIDataParser import AIDataParser
from modules.APICaller.APICaller import APICaller
from data.AnalysisRepository import STTAnalysisRepository
from modules.Accuracy.AccuracyFilter import AccuracyFilter as AF
import json
import modules.Accuracy.STTAccuracyTool as sat
from PIL import Image, ImageDraw

# Test DataSet 관리, API호출과 기대값 비교, 통계 등 테스트 수행
class TestController:
    def __init__(self) -> None:
        self._dataList = []
        self._apiList = []

    def add_STT_TestData(self, target:AIDataParser):
        self._dataList.append(target)

    def add_STT_API(self, target:APICaller):
        self._apiList.append(target)

    def add_Vision_TestData(self, target:AIDataParser):
        self._dataList.append(target)

    def add_Vision_API(self, target:APICaller):
        self._apiList.append(target)

    def startVisionRequest(self, limit:int=0, record:str=None):
        # get target_data/path
        for eachDataParser in self._dataList:
            dataParser:AIDataParser = eachDataParser

            # get samples from target_data/path
            sum=0
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

                    self._saveVisionImage(target=testResult)
                    print("expected = {}, actual = {}".format(td.expectedList[0], len(actualResult)))
                    logging.info(str(testResult))

                    if td.expectedList[0] == len(actualResult):
                        sum+=1

            print(sum)

    def _saveVisionImage(self, target:TestResult):
        # init.
        img = Image.open(target.source)
        _width, _height = img.size
        draw = ImageDraw.Draw(img)

        # get rectangle data & draw
        for face in target.actual:
            face:Face = face
            abs_x = _width * face.x
            abs_y = _height * face.y
            abs_width = _width * face.width
            abs_height = _height * face.height
            draw.rectangle(xy=[(abs_x, abs_y), (int(abs_x+abs_width), int(abs_y+abs_height))], outline="#00FF00")

        # save
        idxOfExt = str(target.source).rindex('.')
        img.save(target.source[:idxOfExt] + "_rec" + target.source[idxOfExt:])
        img.close()


    def startSTTRequest(self, limit:int=0, record:str=None):
        _trList = []
        file_record = open(record, 'w') if record else None

        # for each DATA
        for eachDP in self._dataList:
            dp:AIDataParser = eachDP

            for item in dp.getTestDataList(limit=limit):     # TOTAL_SIZE
                td:TestData = item
                print(f'[SAMPLE] {td.sampleFilePath}')
                logging.info(f'[SAMPLE] {td.sampleFilePath}')
                logging.info(f'[EXP] {td.expectedList}')

                # for each API Call
                for eachAPI in self._apiList:
                    api:APICaller = eachAPI

                    actualResult = api.request(targetFile=td.sampleFilePath)  # api response
                    if not actualResult:
                        print(f'[Exception] {api.__class__.__name__} request failed.')
                        continue 
                    
                    tr = TestResult(id = td.id,
                                    source = td.sampleFilePath,
                                    service = api.__class__.__name__,
                                    expected = td.expectedList,
                                    actual = actualResult
                                    # accuracy = accuracy,
                                    # categories = self._staticTool.categorize([hm_expected, hm_actual])
                                    )

                    # recording
                    if file_record:
                        file_record.write(str(tr))
                        file_record.write("\n")
                    logging.info(str(tr))
                    print(tr)

                    _trList.append(tr)

        file_record.close()

        return _trList

    
    def getStaticInfo(self, accuracyFilter, categoryFilter, sttResultData, targetFile, record):
        targetFile = open(targetFile, 'r')
        dataList = targetFile.readlines()
        _analysisRepo = STTAnalysisRepository()

        for i in range(0, len(dataList), len(self._apiList)):
            apiResultList = []
            for j in range(i, i+len(self._apiList)):
                apiResultList.append(dataList[j])

            # filtering (digit, alpha, None)
            isNA = False
            for sttResult in apiResultList:
                jResult = json.loads(sttResult)
                
                ### 공백만 제외
                # if len([emptyData for emptyData in jResult['actual'] if len(emptyData)]) == 0:
                ### 공백+숫자+문자 제외
                if len([naData for naData in jResult['expected']+jResult['actual'] if re.findall('[a-zA-Z0-9]+', naData)]) > 0 \
                    or len([emptyData for emptyData in jResult['actual'] if len(emptyData)]) == 0:

                    isNA = True
                    logging.info("[Filtering] {} is removed.".format(jResult['id']))
                    break


            for sttResult in apiResultList:
                jResult = json.loads(sttResult)
                tr = TestResult(id=jResult['id'], service=jResult['service'], source=jResult['source'], expected=jResult['expected'], actual=jResult['actual'])
                _analysisRepo.addAnalysisData(testResult=tr, accuracyFilter=accuracyFilter, categoryFilter=categoryFilter, isNA=isNA)
        
        self._getStatics(analysisRepo=_analysisRepo, record=record)


    def startAnalysisSTTResult(self, accuracyFilter:list, categoryFilter:list=None, sttResultData:list=None, targetFile:str=None, record:str=None):

        _analysisRepo = STTAnalysisRepository()


        # get TestResult list.
        _testResultList = []
        if sttResultData:       # list input (directly)
            _testResultList = sttResultData
        elif targetFile:              # file input
            file_target = open(targetFile, 'r') if targetFile else None

            for tr in file_target.readlines():
                # print(tr)
                tr_json:dict = json.loads(tr)

                if type(tr_json) != dict:
                    logging.exception(f'[Exception] {__class__.__name__}:{__name__} - result data is not json format')
                    return

                _testResultList.append(TestResult(id=tr_json.get('id'),
                                            service=tr_json.get('service'),
                                            source=tr_json.get('source'),
                                            expected=tr_json.get('expected'),
                                            actual=tr_json.get('actual')))
        else:
            logging.exception(f'[Exception] {__class__.__name__}:{__name__} - result data is empty')
            return


        # get AnalysisResult list.
        _categoryFilter = categoryFilter if categoryFilter else []
        for eachTestResult in _testResultList:
            _analysisRepo.addAnalysisData(testResult=eachTestResult,
                                        accuracyFilter=accuracyFilter,
                                        categoryFilter=_categoryFilter)

        # Record Analysis data
        # if record:
        #     file_record = open(record, 'w')
        #     file_record.write(str(_analysisRepo))
        #     file_record.close()


        return self._getStatics(analysisRepo=_analysisRepo, record=record)


    def _getStatics(self, analysisRepo:STTAnalysisRepository, record:str=None):

        _ar:dict = json.loads(str(analysisRepo).replace("\'", "\""))

        staticRepo = {'total': 0}
        # staticRepo = {
        #    "total":35000,
        #    "EXP_BASED":{
        #       "KT_STT":{
        #          "NC":{
        #             "sample":15274,
        #             "acc_sum":1188084.430000014
        #          },
        #          "NA":{
        #             "sample":4855,
        #             "acc_sum":291369.5600000018
        #          }, ...
        #       },
        #       "Kakao_STT":{...}
        #    },
        #    "WER":{
        #       "KT_STT":{...},
        #       "Kakao_STT":{...}
        #    }
        # }

        # Statics
        for sample in _ar.values():
            staticRepo['total'] += 1
            
            for eachStatic in sample['statics']:
                service = eachStatic['service']
                categories = eachStatic['categories']
                acc_name = eachStatic['accuracy']['name']
                acc_rate = eachStatic['accuracy']['value']

                # create AccuracyType (ex_ [EXP_BASED, WER, ...])
                if acc_name not in staticRepo:
                    staticRepo[acc_name] = {}
                
                # create Service (ex_ KT, KAKAO)
                if service not in staticRepo[acc_name]:
                    staticRepo[acc_name][service] = {}
                
                service_in_repo:dict = staticRepo[acc_name][service]
                for ct in categories:
                    
                    # create Category (ex_ ['NA', 'NC', '예약', ...])
                    if ct not in service_in_repo:
                        service_in_repo[ct] = {}
                        service_in_repo[ct]['sample'] = 0
                        service_in_repo[ct]['acc_sum'] = 0

                    service_in_repo[ct]['sample'] += 1
                    service_in_repo[ct]['acc_sum'] += acc_rate

            
        ### Record
        # if record:
        #     file_record = open(record, 'w')
        #     file_record.write(str(_analysisRepo))
        #     file_record.close()

        # print Statics
        return self._parseStaticRepo(staticRepository = staticRepo)


    def _parseStaticRepo(self, staticRepository:dict):
        result = ''

        for sKey, sValue in staticRepository.items():
            if sKey == 'total':
                result += '========================\n'
                result += 'total sample = {}\n'.format(sValue)
                result += '========================\n'
            else:
                result += '{} 정확도 측정 결과\n'.format(sKey)
                for serviceType, categoryInfo in sValue.items():               # Compare Method
                    result += '{0:<15}  '.format(serviceType)

                    s_sum = 0
                    s_sample = 0

                    for categoryType, staticInfo in categoryInfo.items():     # Service
                        result += '{} : {} % ({})'.format(categoryType, str(round(staticInfo['acc_sum']/staticInfo['sample'], 2)).ljust(5), staticInfo['sample'])
                        result += '{0:<4}'.format(' ')

                        # Not Applicable 제외한 전체 평균
                        if categoryType != 'NA':
                            s_sum += staticInfo['acc_sum']
                            s_sample += staticInfo['sample']

                    result += '전체평균 : {} %'.format(str(round(s_sum/s_sample, 2)).ljust(5))
                    result += '\n'

                result += '------------------------\n'

        print(result)

        return result
        # print(staticRepository)



   