from itertools import zip_longest
import logging
from Struct.Result import TestResult
from Struct.TestData import TestData
from modules.Service.AnalysisManager import AnalyzerInfo
from modules.Service.Analyzer.BaseResultAnalyzer import BaseResultAnalyzer
from modules.Service.Type import SUPPORT
from modules.Database.Controller import APIDatabaseController as db_ctrl

from modules.Service.API.BaseAPICaller import BaseAPICaller
from modules.Service.APIManager import APIInfo, ServiceProvider

from modules.Service.DataManager import DataInfo
from modules.Service.Data.BaseDataParser import BaseDataParser

import psycopg2

class TestController:
    def __init__(self) -> None:
        self.__connectDB()

    def __connectDB(self):
        ### DB init.
        # apidb = APIDatabaseController()
        try:
            apidb = db_ctrl()
            apidb.connect()
        except psycopg2.Error as e:
            logging.info(f"[Error] DB Connecting Error. - {e}")

        return apidb


    def testWith(self, data:DataInfo, service_provider:ServiceProvider, analyzerInfo:AnalyzerInfo, support:SUPPORT, option:dict):
        '''설정된 테스트 대상으로 검증 진행

        data: 테스트 대상 sample
        service_provider: api service provider
        support: api type (STT, FACE_DETECTION, ...)
        option: limit, threshold, ...
        '''
        resultList = []
        purpose = support.value

        try:
            data_parser:BaseDataParser = data.findParser(support=support).parser
            api:APIInfo = service_provider.findAPICaller(support=support)
            analyzer:BaseResultAnalyzer = analyzerInfo.analyzer
        except AttributeError as e:
            logging.error("[ERROR] {} is not supporte {} - {}".format(service_provider.name, support.name, e))
            return None
        

        # TODO:TestController: test mode에 따라서 데이터를 어떻게 가져올 것인지 추가 구현


        ### GET testset
        # datainfo 테이블에서 이미 등록된 데이터가 있는지 검색
        testsetGroup_from_file = data_parser.getTestDataList(limit=option.get("limit")) if option.get("limit") else data_parser.getTestDataList()
        testsetGroup_from_db = db_ctrl().getTestsetGroup(title=data.name, purpose=purpose, limit=option.get("limit"))


        ### ADD datainfo
        # DB에 (testset의 묶음 정보인) datainfo 정보가 없는 경우 신규 등록
        if not testsetGroup_from_db:
            # db_ctrl().addDatainfo(title=data_parser.name, origin=TV.DATA.ORIGIN(data_parser.name), base_dir=data_parser.value, purpose=purpose)
            db_ctrl().addDatainfo(title=data.name, origin="", base_dir=data.path, purpose=purpose)
            print("add testset to DB")


        ### UPDATE testset
        # Testset 개수가 다른 경우, DB에 누락된 데이터 찾아서 추가
        if len(testsetGroup_from_db) < len(testsetGroup_from_file):
            for td_file in testsetGroup_from_file:
                td_file:TestData = td_file
                testsetList_db = db_ctrl().getTestsetList(datainfo=data.name, purpose=purpose, source=td_file.sampleFilePath)    # searching testset
                needUpdate = False

                # 파일의 데이터와 DB의 데이터가 다른 경우, 동기화를 위해 DB의 기존 testset 데이터 삭제 (result는 cascade로 삭제됨)
                if len(td_file.expectedList) != len(testsetList_db):
                    db_ctrl().deleteTestsetList(datainfo=data.name, purpose=purpose, source=td_file.sampleFilePath)
                    needUpdate = True
                elif len(testsetList_db) > 0:
                    # 파일과 DB의 기대값이 다른 경우 기존 DB의 값 삭제
                    for td_file, expected in zip_longest(testsetList_db, td_file.expectedList):
                        if td_file[1] != expected:
                            db_ctrl().deleteTestsetList(datainfo=data.name, purpose=purpose, source=td_file.sampleFilePath)
                            needUpdate = True
                            break

                # update testset
                if len(testsetList_db) == 0 or needUpdate:
                    number = 0
                    for expected in td_file.expectedList:
                        db_ctrl().addTestset(datainfo=data.name, purpose=purpose, source=td_file.sampleFilePath, number=number, expected=expected)
                        number += 1


        ### GET/UPDATE result
        for td_file in testsetGroup_from_file:
            td_file:TestData = td_file
            result_db = db_ctrl().getResultList(datainfo=data.name, purpose=purpose, source=td_file.sampleFilePath, api=api.name)
            
            # API request
            if not result_db:
                api_caller:BaseAPICaller = api.caller
                result_db = api_caller.request(targetFile=td_file.sampleFilePath)
                logging.info("request API to {} [{}] >> {}".format(api.name, td_file.sampleFilePath, result_db))
                print("request API to {} [{}] >> {}".format(api.name, td_file.sampleFilePath, result_db))

                # update db (when response-data exist)
                for ra in result_db:
                    db_ctrl().addResult(datainfo=data.name, purpose=purpose, source=td_file.sampleFilePath, api=api.name, result=ra)

            # result
            tr = TestResult(id = td_file.id,
                            source = td_file.sampleFilePath,
                            service = api.name,
                            expected = td_file.expectedList,
                            actual = result_db)

            resultList.append(tr)

        
        return analyzer.analysisResultStack(resultList=resultList)

        # return resultList
        # return self.getStatistics(resultList=resultList, support=support)


    # def getStatistics(self, resultList:list, support=SUPPORT):
    #     Analy

    #     ### TODO: resultList를 기반으로 support에 따라서 Analyzer 중 선별해 통계 결과 반환

        

    #     sttRA = STTResultAnalyzer()
    #     statisticsResult = sttRA.analysisResultStack(resultList=resultList)

    #     return statisticsResult

                
