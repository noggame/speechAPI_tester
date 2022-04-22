from data.TestResult import TestResult
from modules.Analysis.ResultAnalyzer import ResultAnalyzer


class FaceResultAnalyzer(ResultAnalyzer):
    def __init__(self) -> None:
    #     self._analysisResultDict = {}
        super().__init__()

    # def addAnalysisData():
    # def addAnalysisData(self, testResult:TestResult, accuracyFilter:list, categoryFilter:list, isNA:bool=False):
    def addAnalysisData(self, testResult:TestResult):
        """ TestResult를 입력받아 분석하고, 분석 결과를 STT Analysis Reopistory에 저장 """
        
        pass

        # get Accuracy & Category info.d
        staticInfoList = []
        for accFunc in accuracyFilter:
            hm_expected, hm_actual, accuracy = accFunc(expectedList = testResult.expected, actualList = testResult.actual)
            categories = sat.categorizeSTT(expected = hm_expected, actual  = hm_actual, categoryFilter  = categoryFilter, isNA=isNA)
            
            # get Filter Name (Key)
            filterName = None
            for k, v in AccuracyFilter.__dict__.items():
                if accFunc == v:
                    filterName = k
                    break

            
            # collect static information
            staticInfoList.append({
                'service': testResult.service,
                'expected': hm_expected,
                'actual': hm_actual,
                'accuracy': {
                    'name': filterName,
                    'value': accuracy
                },
                'categories': categories
            })
            

        # store static data
        if testResult.id not in self._analysisResultDict:
            eachId = self._analysisResultDict[testResult.id] = {}   # set id
            eachId['source'] = testResult.source                    # set source
            eachId['statics'] = []                                  # init. static
        
        statics:list = self._analysisResultDict[testResult.id]['statics']
        statics.extend(staticInfoList)