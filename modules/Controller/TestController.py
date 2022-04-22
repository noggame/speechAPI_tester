from modules.DataParser.AIDataParser import AIDataParser
from modules.APICaller.APICaller import APICaller
from modules.Analysis.VoiceAnalyzer import STTResultAnalyzer

# Test DataSet 관리, API호출과 기대값 비교, 통계 등 테스트 수행
class TestController:
    def __init__(self) -> None:
        self._dataList = []
        self._apiList = []

    def addTestData(self, target:AIDataParser):
        self._dataList.append(target)

    def addAPICaller(self, target:APICaller):
        self._apiList.append(target)

    def startRequest(self, limit:int=0, record:str=None):
        pass




    # TODO : method 파라미터 및 객체 검증 필요
    def startAnalysis(self, accuracyFilter:list=None, categoryFilter:list=None, resultList:list=None, targetFile:str=None, record:str=None):
        pass

    def getStaticInfo(self, accuracyFilter, categoryFilter, sttResultData, targetFile, record):
        pass

    def _getStatics(self, analysisRepo:STTResultAnalyzer, record:str=None):
        pass

    def _parseStaticRepo(self, staticRepository:dict):
        pass



   