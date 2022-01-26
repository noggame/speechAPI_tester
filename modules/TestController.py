import logging
from typing import Set
from data.TestData import TestData
from data.TestResult import TestResult
from modules.AIDataParser.AIDataParser import AIDataParser
from modules.APICaller.APICaller import APICaller
from data.AnalysisRepository import STTAnalysisRepository
from modules.AccuracyFilter import AccuracyFilter as AF
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

            # 완료
            # for item in dp.getTestDataList(limit=limit)[21500:22900]:     # 07
            # for item in dp.getTestDataList(limit=limit)[22900:24000]:     # 08
            # for item in dp.getTestDataList(limit=limit)[24000:25100]:     # 09
            # for item in dp.getTestDataList(limit=limit)[25100:26600]:     # 10

            # 진행중

            for item in dp.getTestDataList(limit=limit)[26500:]:
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


    def startAnalysisSTTResult(self, accuracyFilter:list, categoryFilter:list=None, sttResultData:list=None, file:str=None, record:str=None):

        _analysisRepo = STTAnalysisRepository()


        # get TestResult list.
        _testResultList = []
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
        _categoryFilter = categoryFilter if categoryFilter else []
        for eachTestResult in _testResultList:
            _analysisRepo.addAnalysisData(testResult=eachTestResult,
                                        accuracyFilter=accuracyFilter,
                                        categoryFilter=_categoryFilter)
        # Record Analysis data
        if record:
            file_record = open(record, 'w')
            file_record.write(str(_analysisRepo))


        self._getStatics(_analysisRepo)


    def _getStatics(self, analysisRepo:STTAnalysisRepository):

        staticRepo = {'total':0}
        _ar:dict = json.loads(str(analysisRepo).replace("'", "\""))

        # count StaticInfo
        for sample in _ar.values():
            staticRepo[acc_name]['total'] += 1
            
            for eachStatic in sample['statics']:
                service = eachStatic['service']
                categories = eachStatic['categories']
                acc_name = eachStatic['accuracy']['name']
                acc_rate = eachStatic['accuracy']['value']

                # create AccuracyType (ex_ [EXP_BASED, WER, ...])
                if acc_name not in staticRepo:
                    staticRepo[acc_name] = {}
                
                # new Service (ex_ KT, KAKAO)
                if service not in staticRepo[acc_name]:
                    staticRepo[acc_name][service] = {}
                
                service_in_repo:dict = staticRepo[acc_name][service]
                for ct in categories:
                    # new Category (ex_ ['NA', 'NC', '예약', ...])
                    if ct not in service_in_repo:
                        service_in_repo[ct] = {}
                        service_in_repo[ct]['sample'] = 0
                        service_in_repo[ct]['acc_sum'] = 0

                    service_in_repo[ct]['sample'] += 1
                    service_in_repo[ct]['acc_sum'] += acc_rate

        # print Statics
        self._parseStaticRepo(staticRepository = staticRepo)


    def _parseStaticRepo(self, staticRepository:dict):
        for accuracyType, static in staticRepository.items():
            


        print(staticRepository)



   