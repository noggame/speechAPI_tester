import psycopg2
import logging
from modules.DesignPattern.Singleton import MetaSingleton

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
                password="qaexam12#$"
            )
            self._cur = self._connection.cursor()

        except psycopg2.Error as e:
            logging.error("[ERROR] DB Connecting error occured - {}".format(e))


    def addDatainfo(self, title:str, origin:str, base_dir:str, purpose:str):
        """테스트 데이터 정보 저장

        title 정보가 기-등록된 경우는 무시

        title: 테스트 데이터 명칭
        origin: 구분명(출처로 구분)
        base_dir: 데이터 기본 경로
        purpose: 데이터 사용 목적 (STT, FaceDetection, ...)
        """

        try:
            self._cur.execute(f"INSERT INTO datainfo (title, origin, base_dir, purpose, registered) \
                                VALUES ('{title}', '{origin}', '{base_dir}', '{purpose}', now()) \
                                ON CONFLICT (title, purpose) DO NOTHING")
            self._connection.commit()

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured - {}".format(e))


    def getTestset(self, datainfo, purpose, source, number):
        try:
            self._cur.execute(f"SELECT T.index, T.expected \
                                FROM datainfo D, testset T \
                                WHERE D.title = '{datainfo}' \
                                    AND D.purpose = '{purpose}' \
                                    AND T.datainfo = D.index \
                                    AND T.source = '{source}' \
                                    AND T.number = {number}")

            return self._cur.fetchall()

        except psycopg2.Error as e:
            logging.error("[ERROR] getTestset error occured - {}".format(e))

        return None


    def getTestsetList(self, datainfo, purpose, source):
        """datainfo, purpose 데이터셋 중 source, number 값을 가지는 데이터셋을 찾아 반환

        return [(index, expected), ...]

        데이터셋을 찾지 못한 경우 None 반환

        datainfo: data 명칭
        purpose: data 사용 용도
        source: 테스트 데이터 파일 경로
        number: 기대값이 여러개일 경우의 index
        """
        try:
            self._cur.execute(f"SELECT T.index, T.expected \
                                FROM datainfo D, testset T \
                                WHERE D.title = '{datainfo}' \
                                    AND D.purpose = '{purpose}' \
                                    AND T.datainfo = D.index \
                                    AND T.source = '{source}'")

            return self._cur.fetchall()

        except psycopg2.Error as e:
            logging.error("[ERROR] getTestset error occured - {}".format(e))

        return None


    def getTestsetGroup(self, title:str, purpose:str, limit:int=None):
        """data 이름과 목적을 입력받아 datainfo 테이블에서 검색 후, 존재하는 경우 해당하는 전체 testset 반환

        title: data 명칭
        purpose: data 사용 용도
        limit: 제한 개수
        """
        try:
            _limit = "" if not limit else f"LIMIT {limit}"

            self._cur.execute(f"SELECT index, source, number, expected FROM testset \
                                WHERE datainfo IN (SELECT index FROM datainfo WHERE title='{title}' AND purpose='{purpose}') \
                                {_limit}")

            # result = self._cur.fetchall()
            # print(*result, sep="\n")
        
            # return result
            result = []

            for data in self._cur.fetchall():
                result.append({
                    "index": data[0],
                    "source": data[1],
                    "number": data[2],
                    "expected": data[3]
                })

            return result

        except psycopg2.Error as e:
            logging.error("[ERROR] getTestsetGroup error occured - {}".format(e))

        return None


    def addTestset(self, datainfo:str, purpose:str, source:str, number:int, expected:str):
        """신규 testset 생성

        datainfo: 관련 datainfo 데이터의 index
        purpose: 관련 datainfo 데이터의 사용목적
        source: 테스트 데이터 파일 경로
        number: 동일 데이터의 기대값이 복수개인 경우 사용되는 구분자(counting number)
        expected: 기대값
        """
        try:
            # datainfo 테이블에서 datainfo 정보로 index 값을 찾아 datainfo 정보로 추가
            self._cur.execute(f"INSERT INTO testset (datainfo, source, number, expected, registered) \
                                SELECT index, '{source}', {number}, '{expected}', now() \
                                FROM datainfo \
                                WHERE title='{datainfo}' AND purpose='{purpose}'")

            self._connection.commit()

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured - {}".format(e))



    def deleteTestset(self, datainfo, purpose, source, number):
        try:
            self._cur.execute(f"DELETE FROM testset \
                                WHERE datainfo IN (SELECT index FROM datainfo WHERE title='{datainfo}' AND purpose='{purpose}') \
                                    AND source = '{source}' \
                                    AND number = {number}")

            return self._cur.fetchall()

        except psycopg2.Error as e:
            logging.error("[ERROR] getTestset error occured - {}".format(e))

        return None


    def deleteTestsetList(self, datainfo:str, purpose:str, source:str):
        """title, purpose 데이터셋 중 source, number 값을 가지는 데이터셋을 찾아 반환

        데이터셋을 찾지 못한 경우 None 반환

        title: data 명칭
        purpose: data 사용 용도
        source: 테스트 데이터 파일 경로
        number: 기대값이 여러개일 경우의 index
        """
        try:
            self._cur.execute(f"DELETE FROM testset \
                                WHERE datainfo IN (SELECT index FROM datainfo WHERE title='{datainfo}' AND purpose='{purpose}') \
                                    AND source = '{source}'")

            self._connection.commit()
            logging.info("[DB] DELETE : testset data - title={}, purpose={}, source={}".format(datainfo, purpose, source))

        except psycopg2.Error as e:
            logging.error("[ERROR] getTestset error occured")


    def getResultList(self, datainfo:str, purpose:str, source:str, api:str):
        """입력받은 testset 정보를 대상으로 테스트한 결과과 있는지 result 테이블에서 검색 후 (testset_id, result_value)튜플 리스트 반환

        testset의 expected 개수에 따라 다수의 값을 반환할 수 있다.
        """
        try:
            result = []

            self._cur.execute(f"SELECT R.value FROM datainfo D, testset T, result R \
                                WHERE D.title='{datainfo}' \
                                    AND D.purpose='{purpose}' \
                                    AND T.datainfo = D.index \
                                    AND T.source='{source}' \
                                    AND R.testset = T.index \
                                    AND R.api = '{api}'")

            for actualList in self._cur.fetchall():
                for actual in actualList:
                    result.append(actual)

            return result

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured - {}".format(e))

        return None       


    def addResult(self, datainfo:str, purpose:str, source:str, api:str, result:str, output:str=None):
        """ 테스트결과 정보 저장

        source: 테스트 데이터 파일 경로
        service_type: API 서비스 종류 (예_ KT_STT, Google_FaceAPI, ...)
        number: 기대값이 여러개일 경우의 index
        actual: 테스트 결과값
        """
        try:
            self._cur.execute(f"INSERT INTO result (testset, api, value, output, registered) \
                                SELECT index, '{api}', '{result}', '{output}', now() \
                                FROM testset \
                                WHERE datainfo IN (SELECT index FROM datainfo WHERE title='{datainfo}' AND purpose='{purpose}') \
                                    AND source='{source}'")

            self._connection.commit()
            
        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured - {}".format(e))

