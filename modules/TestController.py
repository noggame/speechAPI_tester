import logging
import re
from data.TestData import TestData
from data.TestResult import TestResult
from modules.AIDataParser.AIDataParser import AIDataParser
from modules.APICaller.APICaller import APICaller
from data.ResultRepository import ResultRepository
from modules.StaticTool import StaticTool
import modules.similarity.STT.compareSTT as compareSTT


# Test DataSet 관리, API호출과 기대값 비교, 통계 등 테스트 수행
class TestController:
    def __init__(self) -> None:
        self._dataList = []
        self._apiList = []
        self._staticTool = StaticTool(categoryList=['예약', '주차', '메뉴', '영업'])
        self._resultRepo = ResultRepository()

    def addTestData(self, target:AIDataParser):
        self._dataList.append(target)

    def addAPICaller(self, target:APICaller):
        self._apiList.append(target)

    def start(self, limit:int=0):
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

                    tts_result = api.request(targetFile=td.sampleFilePath)  # api response
                    
                    # select highest matcehd accuracy
                    hm_expected, hm_actual, accuracy = compareSTT.calculateAccuracy_exp(td.expectedList, tts_result)
                    logging.info(f'[{api.__class__.__name__}] {hm_expected} / {hm_actual} / {accuracy}%')
                    
                    tr = TestResult(id = td.id,
                                    source = td.sampleFilePath,
                                    service = api.__class__.__name__,
                                    expected = hm_expected,
                                    actual = hm_actual,
                                    accuracy = accuracy,
                                    categories = self._staticTool.categorize([hm_expected, hm_actual]))

                    self._resultRepo.addTestResult(testResult=tr)

        # Finished

        print(self._resultRepo)

        # logging.info(self._staticTool.getStatics())

