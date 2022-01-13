import logging
import re
from data.TestData import TestData
from data.TestResult import TestResult
from modules.AIDataParser.AIDataParser import AIDataParser
from modules.APICaller.APICaller import APICaller
from data.ResultRepository import ResultRepository
from modules.StaticTool import StaticTool
import modules.similarity.STT.compareSTT as compareSTT


# Test DataSet 관리 및 API호출과 기대값 비교 등 테스트 전반의 기능 제어

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
                logging.info(f'testing for {td.sampleFilePath}')
                logging.info(f'[EXP] {td.expectedList}')

                # for each API Call
                for eachAPI in self._apiList:
                    api:APICaller = eachAPI

                    tts_result = api.request(targetFile=td.sampleFilePath)  # api response

                    # select highest matcehd accuracy
                    hm_expected, hm_actual, accuracy = compareSTT.calculateAccuracy_exp(td.expectedList, tts_result)
                    # _categories = []
                    # _categories.append(self._staticTool.categorize([hm_expected, hm_actual]))
                    
                    tr = TestResult(id = td.id,
                                    source = td.sampleFilePath,
                                    service = api.__class__.__name__,
                                    expected = hm_expected,
                                    actual = hm_actual,
                                    accuracy = accuracy,
                                    categories = self._staticTool.categorize([hm_expected, hm_actual]))

                    self._resultRepo.addTestResult(testResult=tr)
                    

                    logging.info(f'\n[TestResult]\n{tr}')

                    # self._staticInfo.addTestResult

                    # self._staticInfo.addTestResult(tr, categoryList=['예약', '주차', '메뉴', '영업'])
                    
        print(self._resultRepo)
        # logging.info(self._staticTool.getStatics())

    def getStatics(self):
        # @@@@@@@@@@@@@@ 저장된 self._staticInfo 를 
        pass

    # def getStaticInfo(self):
        # self._staticInfo.
