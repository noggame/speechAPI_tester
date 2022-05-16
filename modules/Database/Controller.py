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
            logging.ERROR("[ERROR] DB Connecting error occured - {}".format(e))
            print("[ERROR] DB Connecting error occured - {}".format(e))


    def addDataset(self, source:str, origin:str, data_type:str, data_format:str):
        """테스트 데이터 정보 저장

        source: 테스트 데이터 파일 경로
        origin: 구분명(출처로 구분)
        data_type: 유형 (예_ image, sound, text, ...)
        data_fromat: 파일 포맷 (예_ jpeg, wav, mp3, txt, ...)
        """
        pass

    def addTestset(self, source:str, service_type:str, number:int, expected:str):
        """입력받은 기대값 정보를 testset 테이블에 저장

        source: 테스트 데이터 파일 경로
        service_type: API 서비스 종류 (예_ KT_STT, Google_FaceAPI, ...)
        number: 기대값이 여러개일 경우의 index
        expected: 기대값
        """
        pass

    def addResult(self, source, service_type, number, actual):
        """ 테스트결과 정보 저장
        입력받은 source, service_type, number 정보를 기반으로 testset에서 index값(고유번호) 검색 후 저장

        source: 테스트 데이터 파일 경로
        service_type: API 서비스 종류 (예_ KT_STT, Google_FaceAPI, ...)
        number: 기대값이 여러개일 경우의 index
        actual: 테스트 결과값
        """
        pass

    # def createEmptyTableForTest(self, tableName):
    #     try:
    #         self._cur.execute(f"CREATE TABLE IF NOT EXISTS {tableName} (name TEXT NOT NULL)")
    #         self._connection.commit()

    #     except psycopg2.Error as e:
    #         logging.ERROR("[ERROR] Create table error - {}".format(e))
    #         print("[ERROR] Create table error - {}".format(e))