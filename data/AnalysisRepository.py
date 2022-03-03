from data.TestResult import TestResult
from modules.Accuracy.AccuracyFilter import AccuracyFilter
import modules.Accuracy.STTAccuracyTool as sat
# from data.TestResultUnified import TestResultUnified

class STTAnalysisRepository:
    def __init__(self) -> None:
        self._analysisResultDict = {}

##### Format #####
# _analysisResultDict = {
#    "id": {
#       "source": ... ,
#       "statics":[
#             {
#                "service": ... ,
#                "expected": ... ,
#                "actual": ... ,
#                "accuracy":{
#                   "name": ... ,
#                   "value": 100
#                },
#                "categories":[ ... ]
#             }
#             ...
#       ]
#    }
# }
##### Example #####
# {
#    "41_0606_221_0_00822_03":{
#       "source":"/mnt/d/Workspace/python/speechAPI_tester/sample/clova_dataset/wavs_train/41_0606_221_0_00822_03.wav",
#       "statics":[
#          [
#             {
#                "service":"KT_STT",
#                "expected":"오늘 예약가능한가요?",
#                "actual":"운이 아니신가요",
#                "accuracy":{
#                   "name":"EXP_BASED",
#                   "value":22.22
#                },
#                "categories":[
#                   "예약"
#                ]
#             }
#             ...
#          ]
#       ]
#    }
# }


    def __str__(self) -> str:
        return str(self._analysisResultDict)

    @property
    def analysisResultDict(self):
        return self._analysisResultDict


    def addAnalysisData(self, testResult:TestResult, accuracyFilter:list, categoryFilter:list, isNA:bool=False):
        """ TestResult를 입력받아 분석하고, 분석 결과를 STT Analysis Reopistory에 저장
        """

        # get Accuracy & Category info.
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
