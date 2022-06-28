import psycopg2
import logging
from modules.DesignPattern.Singleton import MetaSingleton
import config.cfgParser as cfg

class APIDatabaseController(metaclass=MetaSingleton):
    _connection = None
    _cur = None

    def __init__(self) -> None:
        self.connect()

    def connect(self):
        try:
            self._connection = psycopg2.connect(
                host="0.0.0.0",
                port="5432",
                dbname="apidata",
                user="admin",
                password=cfg.get("db", "password")
            )
            self._cur = self._connection.cursor()

        except psycopg2.Error as e:
            logging.error("[ERROR] DB Connecting error occured - {}".format(e))


    ################################################## datainfo

    def addDatainfo(self, title:str, origin:str, base_dir:str, purpose:str, data_type:str=None):
        """테스트 데이터 정보 저장

        title, purpose 정보로 기-등록된 경우는 무시

        title: 테스트 데이터 명칭
        origin: 구분명(출처로 구분)
        base_dir: 데이터 기본 경로
        purpose: 데이터 사용 목적 (STT, FaceDetection, ...)
        type :  데이터 유형 (image, sound, text, ...)
        """
        _type = f"'{data_type}'" if data_type else "NULL"

        try:
            self._cur.execute(f"INSERT INTO datainfo (title, origin, base_dir, purpose, type, registered) \
                                VALUES ('{title}', '{origin}', '{base_dir}', '{purpose}', {_type}, now()) \
                                ON CONFLICT (title, purpose) DO NOTHING")
            self._connection.commit()

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured - {}".format(e))





    ################################################## testset

    # def getTestset(self, datainfo, purpose, source):
    #     try:
    #         # self._cur.execute(f"SELECT T.index, T.expected \
    #         #                     FROM datainfo D, testset T \
    #         #                     WHERE D.title = '{datainfo}' \
    #         #                         AND D.purpose = '{purpose}' \
    #         #                         AND T.datainfo = D.index \
    #         #                         AND T.source = '{source}'")

    #         self._cur.execute(f"SELECT index, expected\
    #                             FROM testset\
    #                             WHERE datainfo IN (SELECT index FROM datainfo WHERE title='{datainfo}' AND purpose='{purpose}') \
    #                                 AND source='{source}'")

    #         return self._cur.fetchall()

    #     except psycopg2.Error as e:
    #         logging.error("[ERROR] getTestset error occured - {}".format(e))

    #     return None


    def getTestsetList(self, title:str, purpose:str, limit:int=None) -> list:
        """입력받은 data 이름(title)과 목적(purpose) 속성으로 정의된 testset 목록을 찾아 (index, source) 반환

        title: data 명칭
        purpose: data 사용 용도
        limit: 제한 개수
        """

        try:
            _limit = "" if not limit else f"LIMIT {limit}"

            self._cur.execute(f"SELECT index, source \
                                FROM testset \
                                WHERE datainfo IN (SELECT index FROM datainfo WHERE title='{title}' AND purpose='{purpose}') \
                                {_limit}")

            result = []
            for data in self._cur.fetchall():
                result.append({
                    "index": data[0],
                    "source": data[1]
                })

            return result

        except psycopg2.Error as e:
            logging.error("[ERROR] getTestsetGroup error occured - {}".format(e))

        return None


    def getTestsetListBySource(self, datainfo, purpose, source):
        """datainfo, purpose 데이터셋 중 source 값을 가지는 데이터셋을 찾아 반환

        return [(index, expected), ...]

        데이터셋을 찾지 못한 경우 None 반환

        datainfo: data 명칭
        purpose: data 사용 용도
        source: 테스트 데이터 파일 경로
        """
        try:
            # self._cur.execute(f"SELECT T.index, T.expected \
            #                     FROM datainfo D, testset T \
            #                     WHERE D.title = '{datainfo}' \
            #                         AND D.purpose = '{purpose}' \
            #                         AND T.datainfo = D.index \
            #                         AND T.source = '{source}'")
            self._cur.execute(f"SELECT index\
                                FROM testset\
                                WHERE datainfo IN (SELECT index FROM datainfo WHERE title='{datainfo}' AND purpose='{purpose}') \
                                    AND source='{source}'")

            return self._cur.fetchall()

        except psycopg2.Error as e:
            logging.error("[ERROR] getTestset error occured - {}".format(e))

        return None


    def addTestset(self, datainfo:str, purpose:str, source:str):
        """신규 testset 생성

        datainfo, source 정보로 기-등록된 경우는 무시

        datainfo: 관련 datainfo 데이터의 index
        purpose: 관련 datainfo 데이터의 사용목적
        source: 테스트 데이터 파일 경로
        expected: 기대값
        """
        try:
            # datainfo 테이블에서 datainfo 정보로 index 값을 찾아 datainfo 정보로 추가
            self._cur.execute(f"INSERT INTO testset (datainfo, source, registered) \
                                SELECT index, '{source}', now() \
                                FROM datainfo \
                                WHERE title='{datainfo}' AND purpose='{purpose}' \
                                ON CONFLICT (datainfo, source) DO NOTHING")

            self._connection.commit()

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured ::addTestset() - {}".format(e))



    def deleteTestset(self, datainfo, purpose, source):
        try:
            self._cur.execute(f"DELETE FROM testset \
                                WHERE datainfo IN (SELECT index FROM datainfo WHERE title='{datainfo}' AND purpose='{purpose}') \
                                    AND source = '{source}'")

            return self._cur.fetchall()

        except psycopg2.Error as e:
            logging.error("[ERROR] getTestset error occured - {}".format(e))

        return None



    ################################################## expect
    def getExpectData(self, datainfo:str, purpose:str, source:str):
        """
        """
        try:
            expectList = []

            self._cur.execute(f"SELECT value \
                                FROM expect \
                                WHERE testset IN (SELECT index \
                                                    FROM testset \
                                                    WHERE datainfo IN (SELECT index \
                                                                    FROM datainfo \
                                                                    WHERE title='{datainfo}' \
                                                                        AND purpose='{purpose}') \
                                                        AND source='{source}')")

            for expects in self._cur.fetchall():
                for expect in expects:
                    expectList.append(expect)

            return expectList


        except psycopg2.Error as e:
            logging.error("[ERROR] Searching error occured ::getNumOfExpectData() - {}".format(e))


    def getExpectDataFromTestsetByPrimary(self, testset:str):
        """
        """
        try:
            expectList = []

            self._cur.execute(f"SELECT value \
                                FROM expect \
                                WHERE testset='{testset}'")

            for expects in self._cur.fetchall():
                for expect in expects:
                    expectList.append(expect)

            return expectList

        except psycopg2.Error as e:
            logging.error("[ERROR] SELECTION error occured ::getExpectDataFromTestsetByPrimary() - {}".format(e))

        return None
        


    def addExpectData(self, datainfo:str, purpose:str, source:str, value:str):
        """
        """
        try:
            self._cur.execute(f"INSERT INTO expect (testset, value, registered) \
                                SELECT index, '{value}', now() \
                                FROM testset \
                                WHERE datainfo IN (SELECT index FROM datainfo WHERE title='{datainfo}' AND purpose='{purpose}') \
                                    AND source = '{source}'")

            self._connection.commit()
            print("[STORE] expect data - {}".format(value))
            logging.info("[STORE] expect data - {}".format(value))

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured ::addExpectData() - {}".format(e))


    def addExpectDataWithoutDuplicated(self, datainfo:str, purpose:str, source:str, value:str):
        """
        """
        try:
            self._cur.execute(f"SELECT index \
                                FROM expect \
                                WHERE testset IN (SELECT index \
                                                    FROM testset \
                                                    WHERE datainfo IN (SELECT index \
                                                                    FROM datainfo \
                                                                    WHERE title='{datainfo}' \
                                                                        AND purpose='{purpose}') \
                                                        AND source='{source}') \
                                    AND value='{value}'")

            if not self._cur.fetchall():
                self.addExpectData(datainfo=datainfo, purpose=purpose, source=source, value=value)

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured ::addExpectDataWithoutDuplicated() - {}".format(e))


    def deleteExpectDataAll(self, datainfo:str, purpose:str, source:str):

        try:
            self._cur.execute(f"DELETE FROM expect \
                                WHERE testset IN (SELECT index \
                                                    FROM testset \
                                                    WHERE datainfo IN (SELECT index \
                                                                    FROM datainfo \
                                                                    WHERE title='{datainfo}' \
                                                                        AND purpose='{purpose}') \
                                                        AND source='{source}')")

            self._connection.commit()
            print("[DELETE] all expect data - {}".format(source))
            logging.info("[DELETE] all expect data - {}".format(source))

        except psycopg2.Error as e:
            logging.error("[ERROR] Deletion error occured ::deleteExpectDataAll() - {}".format(e))




    ######################## Result
    def getResult(self, testset:str, api:str):
        """
        """
        try:
            self._cur.execute(f"SELECT index \
                                FROM result \
                                WHERE testset='{testset}' AND api='{api}'")

            return self._cur.fetchone()

        except psycopg2.Error as e:
            logging.error("[ERROR] Selection error occured ::getResult() - {}".format(e))

        return None


    def addResult(self, testset:str, api:str, output:str=None):
        """
        """

        _output = f"'{output}'" if output else "NULL"

        try:
            self._cur.execute(f"INSERT INTO result (testset, api, output, registered) \
                                VALUES ('{testset}', '{api}', {_output}, now()) \
                                ON CONFLICT (testset, api) DO NOTHING")

            self._connection.commit()

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured ::addResult() - {}".format(e))



    ######################## Actual
    def getActualData(self, datainfo:str, purpose:str, source:str):
        """입력받은 testset 정보를 대상으로 테스트한 결과과 있는지 result 테이블에서 검색 후 (testset_id, result_value)튜플 리스트 반환

        testset의 expected 개수에 따라 다수의 값을 반환할 수 있다.
        """
        try:
            actualList = []

            self._cur.execute(f"SELECT value \
                                FROM actual \
                                WHERE testset IN (SELECT index \
                                                    FROM testset \
                                                    WHERE datainfo IN (SELECT index \
                                                                    FROM datainfo \
                                                                    WHERE title='{datainfo}' \
                                                                        AND purpose='{purpose}') \
                                                        AND source='{source}')")

            for actual_tuple in self._cur.fetchall():
                for actual_value in actual_tuple:
                    actualList.append(actual_value)

            return actualList

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured - {}".format(e))

        return None


    def getActualDataFromResultByPrimary(self, result:str):
        """입력받은 result id 값을 가지는 result 데이터를 찾고 실제결과인 actual 데이터 반환

        testset : testset's index
        api : api's index
        """
        try:
            actualList = []

            self._cur.execute(f"SELECT value \
                                FROM actual \
                                WHERE result ='{result}'")

            for actual_tuple in self._cur.fetchall():
                for actual_value in actual_tuple:
                    actualList.append(actual_value)

            return actualList

        except psycopg2.Error as e:
            logging.error("[ERROR] Selection error occured ::getActualDataFromResultByPrimary - {}".format(e))


    def getActualDataFromResultByUnique(self, testset:str, api:str):
        """입력받은 testset, api 정보에서 result 데이터를 찾고 실제결과인 actual 데이터 반환

        testset : testset's index
        api : api's index
        """
        try:
            actualList = []

            self._cur.execute(f"SELECT value \
                                FROM actual \
                                WHERE result in (SELECT index FROM result WHERE testset='{testset}' AND api='{api}')")

            for actual_tuple in self._cur.fetchall():
                for actual_value in actual_tuple:
                    actualList.append(actual_value)

            return actualList

        except psycopg2.Error as e:
            logging.error("[ERROR] Selection error occured ::getActualDataFromResultByUnique - {}".format(e))

        return None

    def addActualData(self, testset:str, api:str, value:str):
        """
        """
        try:
            self._cur.execute(f"INSERT INTO actual (result, value, registered) \
                                SELECT index, '{value}', now() \
                                FROM result \
                                WHERE testset='{testset}' AND api='{api}'")

            self._connection.commit()
            print("[STORE] actual data - {}".format(value))
            logging.info("[STORE] actual data - {}".format(value))

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured ::addActualData() - {}".format(e))


    def addActualDataWithoutDuplicated(self, testset:str, api:str, value:str):
        """
        """
        try:
            self._cur.execute(f"SELECT index \
                                FROM actual \
                                WHERE result in (SELECT index FROM result WHERE testset='{testset}' AND api='{api}') \
                                    AND value='{value}'")

            if not self._cur.fetchall():
                self.addActualData(testset=testset, api=api, value=value)

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured ::addActualDataWithoutDuplicated() - {}".format(e))


    def deleteActualDataAll(self, testset:str, api:str):
        """
        """

        try:
            self._cur.execute(f"DELETE FROM actual \
                                WHERE result in (SELECT index FROM result WHERE testset='{testset}' AND api='{api}')")

            self._connection.commit()
            
        except psycopg2.Error as e:
            logging.error("[ERROR] Deletion error occured ::deleteActualDataAll() - {}".format(e))



    ######################## API
    def getAPIdata(self, provider:str, purpose:str, version:str=None) -> list:
        """(api_id, api_url, key_name, key_value) Dict 리스트 반환 (api에 등록된 key 개수에 따라 리스트 길이 결정)
        """
        try:
            _version = f"{version}" if version else self._getLastestAPIVersion(provider=provider, purpose=purpose)

            self._cur.execute(f"SELECT api.index, api.url, key.name, key.value \
                                FROM api \
                                INNER JOIN key ON api.index = key.api \
                                WHERE api.provider='{provider}' AND api.purpose='{purpose}' AND api.version='{_version}'")

            apiResult = {'keys':[]}
            keys:list = apiResult['keys']

            for apiData in self._cur.fetchall():
                apiResult['id'] = apiData[0]
                apiResult['url'] = apiData[1]
                keys.append((apiData[2], apiData[3]))

            return apiResult

        except psycopg2.Error as e:
            logging.error("[ERROR] Selection error occured ::getAPIdata() - {}".format(e))

        return None


    def _getLastestAPIVersion(self, provider:str, purpose:str):
        """
        """
        try:
            self._cur.execute(f"SELECT version \
                                FROM api \
                                WHERE provider='{provider}' AND purpose='{purpose}' \
                                ORDER BY version DESC \
                                LIMIT 1")

            return self._cur.fetchone()[0]

        except psycopg2.Error as e:
            logging.error("[ERROR] Error occured ::_getLastestAPIVersion() - {}".format(e))

        return None