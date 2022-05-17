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


    def addDataset(self, title:str, origin:str, path:str, type:str, format:str):
        """테스트 데이터 정보 저장
        title 정보가 기-등록된 경우는 무시

        title: 테스트 데이터 파일 경로
        origin: 구분명(출처로 구분)
        type: 유형 (예_ image, sound, text, ...)
        fromat: 파일 포맷 (예_ jpeg, wav, mp3, txt, ...)
        """
        try:
            self._cur.execute(f"INSERT INTO dataset VALUES ('{title}', '{origin}', '{path}', '{type}', '{format}', now()) ON CONFLICT (title) DO NOTHING")
            self._connection.commit()

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured - {}".format(e))


    def addTestset(self, source:str, service_type:str, expected:str):
        """입력받은 기대값 정보를 testset 테이블에 저장
        저장에 성공하면 기대값_순번을 반환하고, 실패하면 -1 반환

        source: 테스트 데이터 파일 경로
        service_type: API 서비스 종류 (예_ KT_STT, Google_FaceAPI, ...)
        expected: 기대값
        """
        try:
            # get next_number
            self._cur.execute(f"SELECT MAX(number) FROM testset WHERE source='{source}' AND service_type='{service_type}'")
            matchingNumber = self._cur.fetchone()
            nextNumber = matchingNumber[0]+1 if matchingNumber[0] != None else 0

            # insert data
            self._cur.execute(f"INSERT INTO testset VALUES (nextval('testset_seq'), '{source}', '{service_type}', '{nextNumber}', '{expected}', now())")
            self._connection.commit()

            return nextNumber

        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured - {}".format(e))

        return -1


    def addResult(self, source:str, service_type:str, number:int, actual:str):
        """ 테스트결과 정보 저장
        입력받은 source, service_type, number 정보를 기반으로 testset에서 index값(고유번호) 검색 후 저장

        source: 테스트 데이터 파일 경로
        service_type: API 서비스 종류 (예_ KT_STT, Google_FaceAPI, ...)
        number: 기대값이 여러개일 경우의 index
        actual: 테스트 결과값
        """
        try:
            self._cur.execute(f"SELECT index FROM testset WHERE source='{source}' AND service_type='{service_type}' AND number={number}")
            matchingTestsetId = self._cur.fetchone()[0]
            self._cur.execute(f"INSERT INTO result VALUES ({matchingTestsetId}, '{actual}', now())")
            self._connection.commit()
            
        except psycopg2.Error as e:
            logging.error("[ERROR] Insertion error occured - {}".format(e))


