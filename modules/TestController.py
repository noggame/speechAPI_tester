import logging
from data.TestData import TestData
from data.TestResult import TestResult
from modules.AIDataParser.AIDataParser import AIDataParser
from modules.APICaller.APICaller import APICaller
from data.AnalysisRepository import STTAnalysisRepository
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
        fr = open(f'{record}', 'w') if record else None

        # for each DATA
        for eachDP in self._dataList:
            dp:AIDataParser = eachDP

            for item in dp.getTestDataList(limit=limit):
                td:TestData = item
                print(f'[SAMPLE] {td.sampleFilePath}')
                logging.info(f'[SAMPLE] {td.sampleFilePath}')
                logging.info(f'[EXP] {td.expectedList}')

                # for each API Call
                for eachAPI in self._apiList:
                    api:APICaller = eachAPI

                    # tts_result = api.request(targetFile=td.sampleFilePath)  # api response
                    actualResult = api.request(targetFile=td.sampleFilePath)  # api response

                    # select highest matcehd accuracy
                    
                    tr = TestResult(id = td.id,
                                    source = td.sampleFilePath,
                                    service = api.__class__.__name__,
                                    expected = td.expectedList,
                                    actual = actualResult
                                    # accuracy = accuracy,
                                    # categories = self._staticTool.categorize([hm_expected, hm_actual])
                                    )

                    # recording
                    if fr:
                        fr.write(str(tr))
                    logging.info(str(tr))
                    # print(tr)

                    _trList.append(tr)

        return _trList


    def startAnalysisSTTResult(self, filter:list=None, sttResultData:list=None, file:str=None, record:str=None):
        _filter = filter if filter else ['예약', '주차', '메뉴', '영업'] # default filter = ['NA', 'NC']
        _testResultList = []
        _analysisRepo = STTAnalysisRepository()
        # self._staticTool = StaticTool(categoryList=['예약', '주차', '메뉴', '영업'])


        # get TestResult list.
        if sttResultData:       # list input (directly)
            _testResultList = sttResultData
        elif file:              # file input
            fr = open(f'{file}', 'r') if file else None

            for tr in fr.readlines():
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
            
            _analysisRepo.addAnalysisData(testResult=tr, category_filter=_filter) # accuracy_filter=_filter

        
        print(_analysisRepo)


        ##### +) AnalysisTool에 각 tr_json 정보 넘겨주고, 해당 정보들이 추가될 때 마다 내부적으로 정확도 계산 후 저장
        # hm_expected, hm_actual, accuracy = compareSTT.calculateAccuracy_exp(tr_json.get('expected'), tr_json.get('actual'))
        # ar = 
        # _analysisReuslt.addTestResult(tr)

        # 각 샘플 분석결과 저장
        # _analysisResult = AnalysisResult()
        # _analysisResult.addTestResult(tr)


        # hm_expected, hm_actual, accuracy = compareSTT.calculateAccuracy_exp(td.expectedList, tts_result)
        # logging.info(f'[{api.__class__.__name__}] {hm_expected} / {hm_actual} / {accuracy}%')
        # logging.info(self._staticTool.getStatics())

