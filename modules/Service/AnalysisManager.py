from enum import Enum
from modules.Service.Analyzer.BaseResultAnalyzer import BaseResultAnalyzer
# from modules.Service.Analyzer.ResultAnalyzer.Vision.FDResultAnalyzer import FDResultAnalyzer
from modules.Service.Analyzer.ResultAnalyzer.Voice.STTResultAnalyzer import STTResultAnalyzer
from modules.Service.Type import SUPPORT


class AnalyzerInfo():
    def __init__(self, analyzer:BaseResultAnalyzer, support:SUPPORT) -> None:
        self.analyzer = analyzer
        self.support = support


class AnalyzerManager():
    def __init__(self) -> None:
        self.analyzerList = []
        self._addAnalyzer(analyzerObject = AnalyzerInfo(analyzer=STTResultAnalyzer(), support=SUPPORT.STT))


    def findAnalyzer(self, support:SUPPORT):
        for analyzer in self.analyzerList:
            analyzer:AnalyzerInfo = analyzer
            if analyzer.support == support:
                return analyzer
        return None

    def _addAnalyzer(self, analyzerObject:AnalyzerInfo):
        # Except Duplication
        for analyzer in self.analyzerList:
            analyzer:AnalyzerInfo = analyzer
            if analyzer.support == analyzerObject.support:
                return
        self.analyzerList.append(analyzerObject)

