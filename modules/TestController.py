import logging
from typing import Set
from data.TestData import TestData
from data.TestResult import TestResult
from modules.AIDataParser.AIDataParser import AIDataParser
from modules.APICaller.APICaller import APICaller
from data.AnalysisRepository import STTAnalysisData, STTAnalysisRepository
import json


# Test DataSet 관리, API호출과 기대값 비교, 통계 등 테스트 수행
class TestController:
    def __init__(self) -> None:
        self._dataList = []
        self._apiList = []

    def add_STT_TestData(self, target:AIDataParser):
        self._dataList.append(target)

    def add_STT_API(self, target:APICaller):
        self._apiList.append(target)

    def startSTTRequest(self, limit:int=0, record:str=None):
        _trList = []
        file_record = open(record, 'w') if record else None

        # for each DATA
        for eachDP in self._dataList:
            dp:AIDataParser = eachDP

            for item in dp.getTestDataList(limit=limit)[11000:]:
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


    def startAnalysisSTTResult(self, categoryFilter:list=None, sttResultData:list=None, file:str=None, record:str=None):
        _categoryFilter = categoryFilter if categoryFilter else ['예약', '주차', '메뉴', '영업'] # default filter = ['NA', 'NC']
        _testResultList = []
        _analysisRepo = STTAnalysisRepository()
        # self._staticTool = StaticTool(categoryList=['예약', '주차', '메뉴', '영업'])
        _file_record = open(record, 'w')


        # get TestResult list.
        if sttResultData:       # list input (directly)
            _testResultList = sttResultData
        elif file:              # file input
            file_target = open(file, 'r') if file else None

            for tr in file_target.readlines():
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
        for eachTestResult in _testResultList:

            tr:TestResult = eachTestResult
            
            _analysisRepo.addAnalysisData(testResult=tr, categoryFilter=_categoryFilter) # accuracy_filter=_filter

        self._getStatics(_analysisRepo)
        # print(_analysisRepo)


    def _getStatics(self, analysisRepo:STTAnalysisRepository):
        # get Statics.

        ar = analysisRepo.analysisResultDict

        categoryCounter = {}
        categoryCounter['total'] = 0
        categoryCounter['NA'] = 0
        accuracyCounter = {}
        accuracyCounter['total'] = {}


        for arKey in ar.keys():    # id, source, statics
            id:dict = ar[arKey]
            staticsInfo:dict = id['statics']

            
            # get staticInfo for each service
            eachStaticInfo = {}
            categorySet = set()
            for stKey in staticsInfo.keys():
                service:STTAnalysisData = staticsInfo[stKey]
                eachStaticInfo[stKey] = service

                for ct in service.categories:
                    categorySet.add(ct)


            # statics for each category
            categoryCounter['total'] += 1
            if 'NA' in categorySet:
                categoryCounter['NA'] += 1
            else:
                for ct in categorySet:
                    # counting categories
                    if not categoryCounter.get(ct):
                        categoryCounter[ct] = 0
                    categoryCounter[ct] += 1

                    if not accuracyCounter.get(ct):
                        accuracyCounter[ct] = {}

                    for siKey in eachStaticInfo.keys():
                        service:STTAnalysisData = eachStaticInfo[siKey]

                        # 카테고리 & 서비스별 정확도 계산
                        accuracyForEachCategory:dict = accuracyCounter[ct]
                        if not accuracyForEachCategory.get(siKey):
                            accuracyForEachCategory[siKey] = 0
                        accuracyForEachCategory[siKey] += service.accuracy

                        # 서비스별 정확도 계산
                        accuracyCounterTotal:dict = accuracyCounter['total']
                        if not accuracyCounterTotal.get(siKey):
                            accuracyCounterTotal[siKey] = 0
                        accuracyCounterTotal[siKey] += service.accuracy

        print(accuracyCounter)
        print(categoryCounter)

        # average
        avgAccuracy = {}
        for acKey in accuracyCounter.keys():

            # init. category
            if not avgAccuracy.get(acKey):
                avgAccuracy[acKey] = {}
            
            serviceAccuracyDict:dict = accuracyCounter[acKey]
            for saKey in serviceAccuracyDict.keys():

                avgSvcAccuracy:dict = avgAccuracy[acKey]
                if not avgSvcAccuracy.get(saKey):
                    avgSvcAccuracy[saKey] = round(serviceAccuracyDict[saKey]/categoryCounter[acKey], 2) if acKey != 'total' else round(serviceAccuracyDict[saKey]/(categoryCounter[acKey]-categoryCounter['NA']), 2)
                
        print()
        for aaKey in avgAccuracy.keys():
            print(f'{aaKey} = {avgAccuracy[aaKey]}')


