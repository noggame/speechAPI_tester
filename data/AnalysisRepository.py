from data.TestResult import TestResult
from modules.AccuracyFilter import AccuracyFilter
import modules.Analysis.AnalysisToolForSTT as sttAnalysisTool
import re
import json
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


    def addAnalysisData(self, testResult:TestResult, accuracyFilter:list, categoryFilter:list=None):
        """ TestResult를 입력받아 분석하고, 분석 결과를 STT Analysis Reopistory에 저장
        """

        # get Accuracy & Category info.
        staticInfoList = []
        for accFunc in accuracyFilter:
            hm_expected, hm_actual, accuracy = accFunc(expectedList = testResult.expected, actualList = testResult.actual)
            categories = sttAnalysisTool.categorizeSTT(expected= hm_expected,
                                                    actual= hm_actual,
                                                    categoryFilter = categoryFilter)
            
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
            eachId['source'] = testResult.source    # set source
            eachId['statics'] = []      # init. static
        
        statics:list = self._analysisResultDict[testResult.id]['statics']
        statics.extend(staticInfoList)


    def _categorize(self, targetList, filter:list=None):
        categorySet = set()

        for target in targetList:
            # except [number & digit]
            if re.findall('[a-zA-Z0-9]+', target):
                return ['NA']   # Not Applicable

            # classify category
            for ct in filter:
                if re.search(ct, target):
                    categorySet.add(ct)
            
            # not matched any category
            if not len(categorySet):
                categorySet.add('NC')   # Not Classified

        return list(categorySet)



        

# class STTAnalysisData:

#     def __init__(self, expected, actual, accuracy, categories) -> None:
#         # self._source = None
#         self._expected = expected
#         self._actual = actual
#         self._accuracy = accuracy
#         self._categories = categories
#         # self._expected = {}
#         # self._actual = {}
#         # self._accuracy = {}
#         # self._categories = set()

#     def __str__(self) -> str:
#         result_json = "{"

#         result_json += f'"expected" : "{self._expected}"'
#         result_json += f', "actual" : "{self._actual}"'
#         result_json += f', "accuracy" : {self._accuracy}'
#         result_json += f', "categories" : {self._categories}'

#         result_json += "}"
#         return result_json

#     # @property
#     # def source(self):
#     #     return self._source
#     @property
#     def expected(self):
#         return self._expected
#     @property
#     def actual(self):
#         return self._actual
#     @property
#     def categories(self):
#         return self._categories
#     @property
#     def accuracy(self):
#         return self._accuracy

#     # @source.setter
#     # def source(self, source):
#     #     self._source = source
#     @expected.setter
#     def expected(self, expected):
#         self._expected = expected
#     @actual.setter
#     def actual(self, actual):
#         self._actual = actual
#     @accuracy.setter
#     def accuracy(self, accuracy):
#         self._accuracy = accuracy
#     @categories.setter
#     def categories(self, categories):
#         self._categories = categories
#     # def addCategories(self, categories):
#     #     for ct in categories:
#     #         self._categories.add(ct)
