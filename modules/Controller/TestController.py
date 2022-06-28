from itertools import zip_longest
import logging
from Struct.Result import TestResult
from Struct.TestData import TestData
from modules.Service.APICaller.BaseAPICaller import BaseAPICaller
from modules.Service.DataParser.BaseDataParser import BaseDataParser
from modules.Service.ResultAnalyzer.BaseResultAnalyzer import BaseResultAnalyzer
from modules.Service.Type import SERVICE_TYPE
from modules.Database.Controller import APIDatabaseController as db_ctrl
from modules.DesignPattern.Factory import DataParserFactory as df, ServiceFactory as sf, AnlalyzerFactory as af

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


    def testWith(self, testdata:df.DATA_NAME, service_provider:sf.PROVIDER, service_type:SERVICE_TYPE, option:dict=None):
        """DB에서 testset, 테스트 결과를 불러와 분석하고, 분석결과를 반환\n
        
        [option]\n
        * [update | update_data | updata_result ]:bool = update flag
        * data_limit:int = 데이터 수
        * api_version:str = api 버젼
        """

        resultList = []

        # testdata
        data_name = testdata.name

        # service_type
        purpose = service_type.value

        # option
        data_limit = option.get('data_limit')


        ### INIT. testdata objects
        try:
            # data_parser:BaseDataParser = df().getDataParser(testdata=testdata, service_type=service_type)
            # testsetList_from_file = data_parser.getTestDataList(limit=option.get("limit")) if option.get("limit") else data_parser.getTestDataList()

            # API 
            apiData_from_db:dict = db_ctrl().getAPIdata(provider=service_provider.name, purpose=purpose)
            api_id = apiData_from_db.get('id')
            api_caller:BaseAPICaller = sf().getAPICaller(service_provider=service_provider, service_type=service_type, service_info=apiData_from_db)

            # Testset
            testsetList_from_db = db_ctrl().getTestsetList(title=data_name, purpose=purpose, limit=data_limit)

            # Analyzer
            analyzer:BaseResultAnalyzer = af().getAnalyzer(service_type=service_type)

        except AttributeError as e:
            logging.error("[ERROR] Data or Service is not supported. - {}".format(e))
            return None


        ### UPDATE testdata
        # testset의 처음부터 순차로 파일로부터의 기대값/결과값이 DB에서읽은 기대값/결과값의 수와 동일한지 확인, 차이가 있는 경우 기존 DB의 expect/actual 삭제 후 신규 생성 (index 증가에 주의!)
        if option.get('update'):
            # TODO: option의 limit 개수만큼만 업데이트하도록 추가 구현
            # TODO: 추후 update는 별도 UI로 분리
            self._updateTestdata(testdata=testdata, service_type=service_type, limit=data_limit)
            self._updateResultdata(testdata=testdata, service_provider=service_provider, service_type=service_type, limit=data_limit)
            testsetList_from_db = db_ctrl().getTestsetList(title=data_name, purpose=purpose, limit=data_limit)
        elif option.get('update_data'):
            self._updateTestdata(testdata=testdata, service_type=service_type, limit=data_limit)
            testsetList_from_db = db_ctrl().getTestsetList(title=data_name, purpose=purpose, limit=data_limit)
        elif option.get('update_result'):
            self._updateResultdata(testdata=testdata, service_provider=service_provider, service_type=service_type, limit=data_limit)

        

        ### DB에서 테스트셋 및 결과 확인 (결과에 대해서는 정보가 없는 경우 추가)
        for testset in testsetList_from_db:
            testset:dict = testset
            testset_id = testset.get("index")
            testset_source = testset.get("source")


            ### get result
            result = db_ctrl().getResult(testset=testset_id, api=api_id)


            ### INSERT result
            if not result:
                db_ctrl().addResult(testset=testset_id, api=api_id)
                result = db_ctrl().getResult(testset=testset_id, api=api_id)

            actualList_from_DB = db_ctrl().getActualDataFromResultByPrimary(result=result[0])


            ### INSERT actual
            if not actualList_from_DB:
                response_data:list = api_caller.request(targetFile=testset_source)
                print("[STORE] trying to store actual data from {}".format(testset_source))
                logging.info("[STORE] trying to store actual data from {}".format(testset_source))

                if response_data:
                    for actual in response_data:
                        db_ctrl().addActualDataWithoutDuplicated(testset=testset_id, api=api_id, value=actual)
                else:
                    # empty response
                    logging.warn("[WARNING] empty response from api({}), testset({})".format(api_id, testset_id))



            ### Result
            tr = TestResult(id = testset_id,
                            source = testset_source,
                            service = service_provider.name + "_" + purpose,
                            expected = db_ctrl().getExpectDataFromTestsetByPrimary(testset=testset_id),
                            actual = db_ctrl().getActualDataFromResultByUnique(testset=testset_id, api=api_id))
            resultList.append(tr)


        return analyzer.analysisResultStack(resultList=resultList)


    def _updateTestdata(self, testdata:df.DATA_NAME, service_type:SERVICE_TYPE, limit:int=None):
        """datainfo와 testset 테이블은 키값이 겹치는 경우를 제외하고 추가 등록하며,
        expect는 파일로부터의 기대값 및 DB로부터의 기대값과 비교해 개수가 다른 경우만 업데이트 (기존 expect 데이터 삭제 및 신규 등록)
        """

        # testdata
        data_name = testdata.name
        data_origin = testdata.value['origin']
        data_type = testdata.value['type']
        # service_type
        purpose = service_type.value

        data_parser:BaseDataParser = df().getDataParser(testdata=testdata, service_type=service_type)
        testsetList_from_file = data_parser.getTestDataList(limit=limit)


        ### INSERT datainfo
        db_ctrl().addDatainfo(title=data_name, origin=data_origin, base_dir=data_parser.targetPath, purpose=purpose, data_type=data_type)

        ### UPDATE testset (add only, non-deletion)
        for testset_from_file in testsetList_from_file:
            testset_from_file:TestData = testset_from_file
            source = testset_from_file.sampleFilePath

            ### INSERT testset
            db_ctrl().addTestset(datainfo=data_name, purpose=purpose, source=source)

            ### DELETE expect (개수 다르면 삭제후 다시 저장)
            expectList_from_db = db_ctrl().getExpectData(datainfo=data_name, purpose=purpose, source=source)
            if expectList_from_db and len(testset_from_file.expectedList) != len(expectList_from_db):
                db_ctrl().deleteExpectDataAll(datainfo=data_name, purpose=purpose, source=source)

            ### UPDATE expect
            for expected in testset_from_file.expectedList:
                db_ctrl().addExpectDataWithoutDuplicated(datainfo=data_name, purpose=purpose, source=source, value=expected)


    def _updateResultdata(self, testdata:df.DATA_NAME, service_provider:sf.PROVIDER, service_type:SERVICE_TYPE, limit:int=None):
        """result 테이블은 키값이 겹치는 경우를 제외하고 추가 등록하며, 
        actual은 실제결과 및 DB호출결과와 비교해 개수가 다른 경우만 업데이트 (기존 actual 데이터 삭제 및 신규 등록)
        """


        ### INIT. testdata objects
        try:
            testsetList_from_db:list = db_ctrl().getTestsetList(title=testdata.name, purpose=service_type.value, limit=limit)
            
            # API 
            apiData_from_db:dict = db_ctrl().getAPIdata(provider=service_provider.name, purpose=service_type.value)
            api_id = apiData_from_db.get('id')
            api_caller:BaseAPICaller = sf().getAPICaller(service_provider=service_provider, service_type=service_type, service_info=apiData_from_db)

        except AttributeError as e:
            logging.error("[ERROR] Data or Service is not supported.")
            return None


        ### test api for all testset data
        for testset in testsetList_from_db:
            testset:dict = testset
            testset_id = testset.get('index')
            testset_source = testset.get('source')


            ### INSERT Result
            db_ctrl().addResult(testset=testset_id, api=api_id)

            ### DELETE expect (실제결과와 개수 다르면 삭제후 다시 저장)
            response_data:list = api_caller.request(targetFile=testset_source)
            actualList_from_db:list = db_ctrl().getActualDataFromResultByUnique(testset=testset_id, api=api_id)
            if len(response_data) != len(actualList_from_db):
                db_ctrl().deleteActualDataAll(testset=testset_id, api=api_id)


            ### INSERT actual data
            for actual in response_data:
                db_ctrl().addActualDataWithoutDuplicated(testset=testset_id, api=api_id, value=actual)
