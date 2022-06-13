from itertools import zip_longest
import logging
from data.Result import TestResult
from data.TestData import TestData
from modules.DataParser.AIDataParser import AIDataParser
from modules.APICaller.APICaller import APICaller
from data.ResultRepository import ResultRepository

# Test DataSet 관리, API호출과 기대값 비교, 통계 등 테스트 수행
class TestController:
    def __init__(self) -> None:
        self._dataList = []
        self._apiList = []

    def addTestData(self, target:AIDataParser):
        self._dataList.append(target)

    def addAPICaller(self, target:APICaller):
        self._apiList.append(target)

    def startTestAndAnalysis(self, data_name, api_name, number=0):
        """
        API Test and Analysis method
        """
        pass

    # TODO : method 파라미터 및 객체 검증 필요
    def startRequest(self, limit:int=0, record:str=None):
        pass

    def startAnalysis(self, accuracyFilter:list=None, categoryFilter:list=None, resultList:list=None, targetFile:str=None, record:str=None):
        pass

    def getStaticInfo(self, accuracyFilter:list=None, categoryFilter:list=None, analysisData:dict=None, targetFile:str=None, record:str=None):
        pass

    # def _getStatics(self, analysisRepo:ResultRepository, record:str=None):
    #     pass

    # def _parseStaticRepo(self, staticRepository:dict):
    #     pass


import data.TestVars as TV
import modules.DataParser.DataParserController as dpc
from modules.Database.Controller import APIDatabaseController as db_ctrl

class TestControllerWithDB:
    def testWith(self, data:TV.DATA, api:TV.API, purpose:TV.PURPOSE, option:dict=None):
        '''설정된 테스트 대상으로 검증 진행

        data: 테스트 대상 sample
        api: 테스트 대상 api
        purpose: api type (STT, FACE_DETECTION, ...)
        option: limit, threshold, ...
        '''
        resultList = []
        aidp:AIDataParser = TV.DATA_PARSER.get(data.name, None)(targetPath=data.value)
        apiCaller:APICaller = TV.API_CALLER.get(api.name, None)(url=api.value.get('url'), key=api.value.get('key'))


        # TODO:TestController: test mode에 따라서 데이터를 어떻게 가져올 것인지 추가 구현


        ### GET testset
        # datainfo 테이블에서 이미 등록된 데이터가 있는지 검색
        testsetGroup_from_file = aidp.getTestDataList(limit=option.get("limit")) if option.get("limit") else aidp.getTestDataList()
        testsetGroup_from_db = db_ctrl().getTestsetGroup(title=data.name, purpose=purpose.value, limit=option.get("limit"))


        ### ADD datainfo
        # DB에 (testset의 묶음 정보인) datainfo 정보가 없는 경우 신규 등록
        print(testsetGroup_from_db)
        if not testsetGroup_from_db:
            db_ctrl().addDatainfo(title=data.name, origin=TV.DATA.ORIGIN(data.name), base_dir=data.value, purpose=purpose.value)
            print(2)


        ### UPDATE testset
        # Testset 개수가 다른 경우, DB에 누락된 데이터 찾아서 추가
        if len(testsetGroup_from_db) < len(testsetGroup_from_file):
            for td_file in testsetGroup_from_file:
                td_file:TestData = td_file
                testsetList_db = db_ctrl().getTestsetList(datainfo=data.name, purpose=purpose.value, source=td_file.sampleFilePath)    # searching testset
                needUpdate = False

                # 파일의 데이터와 DB의 데이터가 다른 경우, 동기화를 위해 DB의 기존 testset 데이터 삭제 (result는 cascade로 삭제됨)
                if len(td_file.expectedList) != len(testsetList_db):
                    db_ctrl().deleteTestsetList(datainfo=data.name, purpose=purpose.value, source=td_file.sampleFilePath)
                    needUpdate = True
                elif len(testsetList_db) > 0:
                    # 파일과 DB의 기대값이 다른 경우 기존 DB의 값 삭제
                    for td_file, expected in zip_longest(testsetList_db, td_file.expectedList):
                        if td_file[1] != expected:
                            db_ctrl().deleteTestsetList(datainfo=data.name, purpose=purpose.value, source=td_file.sampleFilePath)
                            needUpdate = True
                            break

                # update testset
                if len(testsetList_db) == 0 or needUpdate:
                    number = 0
                    for expected in td_file.expectedList:
                        db_ctrl().addTestset(datainfo=data.name, purpose=purpose.value, source=td_file.sampleFilePath, number=number, expected=expected)
                        number += 1


        ### GET/UPDATE result
        for td_file in testsetGroup_from_file:
            td_file:TestData = td_file
            result_db = db_ctrl().getResultList(datainfo=data.name, purpose=purpose.value, source=td_file.sampleFilePath, api=api.name)
            
            # API request
            if not result_db:
                result_db = apiCaller.request(targetFile=td_file.sampleFilePath)
                logging.info("request API to {} [{}] >> {}".format(api.name, td_file.sampleFilePath, result_db))
                print("request API to {} [{}] >> {}".format(api.name, td_file.sampleFilePath, result_db))

                # update db (when response-data exist)
                for ra in result_db:
                    db_ctrl().addResult(datainfo=data.name, purpose=purpose.value, source=td_file.sampleFilePath, api=api.name, result=ra)

            # result
            tr = TestResult(id = td_file.id,
                            source = td_file.sampleFilePath,
                            service = api.name,
                            expected = td_file.expectedList,
                            actual = result_db)

            resultList.append(tr)


        ### TODO: resultList를 기반으로 기대값/결과값 분석 결과(통계값) 반환



        return resultList


                
