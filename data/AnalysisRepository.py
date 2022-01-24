from data.TestResult import TestResult
import modules.Analysis.AnalysisToolForSTT as sttAnalysisTool
import re
import json
# from data.TestResultUnified import TestResultUnified

class STTAnalysisRepository:
    def __init__(self) -> None:
        self._analysisResultDict = {}

        #####   format   #######
        # analysisRepo = {
        #   '{id}' : ... {
        #       'source' : ...
        #       'statics' : {STTAnalysisData()} = {
        #           '{service}': STTAnalysisData() = {
        #              'expected' = 'expected sentence'
        #              'actual' = 'actual sentence'
        #              'accuracy' = xx.xx
        #              'categories' = [cat1, cat2]
        #           }
        #       }
        #   }
        # }
        #####

    def __str__(self) -> str:
        result_json = '{'                                       # open json
        
        idList = []
        for aKey in self._analysisResultDict.keys():
            result_id_json = ''

            id:dict = self._analysisResultDict[aKey]
            result_id_json += f'"{aKey}": ' + "{"              # open id
            result_id_json += f'"source": "{id.get("source")}"'                    
            result_id_json += ', "statics" : {'                # open statics

            staticsList = []
            statics:dict = id['statics']
            for sKey in statics.keys():
                result_static_json = ''

                static:STTAnalysisData = statics[sKey]
                result_static_json += f'"{sKey}": '
                result_static_json += f'{static}'
                staticsList.append(result_static_json)
            result_id_json += ', '.join(staticsList)            # combine staticList

            result_id_json += '}'                              # close statics
            result_id_json += '}'                              # close id
            idList.append(result_id_json)

        result_json += ', '.join(idList)                        # combine idList
        result_json += '}'                                      # clise json
        
        return result_json


    def addAnalysisData(self, testResult:TestResult, accuracyFilter:list=None, categoryFilter:list=None):
        """ TestResult를 입력받아 분석하고, 분석 결과를 STT Analysis Reopistory에 저장
        """
        id = testResult.id

        # Accuracy
        hm_expected, hm_actual, accuracy = sttAnalysisTool.calculateSTTAccuracy(expectedList = testResult.expected,
                                                                                actualList = testResult.actual)
        # Categories
        categories = sttAnalysisTool.categorizeSTT(expected= hm_expected,
                                                    actual= hm_actual,
                                                    categoryFilter = categoryFilter)

        # init.
        if not self._analysisResultDict.get(id):
            self._analysisResultDict[id] = {}
            sttAnalysisData:dict = self._analysisResultDict[id]
            sttAnalysisData['source'] = testResult.source
            sttAnalysisData['statics'] = {}
        
        sttAnalysisData:dict = self._analysisResultDict[id]
        statics:dict = sttAnalysisData['statics']
        statics[testResult.service] = STTAnalysisData(expected = hm_expected,
                                                            actual = hm_actual,
                                                            accuracy = accuracy,
                                                            categories = categories)
        

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


    @property
    def analysisResultDict(self):
        return self._analysisResultDict
        

class STTAnalysisData:

    def __init__(self, expected, actual, accuracy, categories) -> None:
        # self._source = None
        self._expected = expected
        self._actual = actual
        self._accuracy = accuracy
        self._categories = categories
        # self._expected = {}
        # self._actual = {}
        # self._accuracy = {}
        # self._categories = set()

    def __str__(self) -> str:
        result_json = "{"

        result_json += f'"expected" : "{self._expected}"'
        result_json += f', "actual" : "{self._actual}"'
        result_json += f', "accuracy" : {self._accuracy}'
        result_json += f', "categories" : {self._categories}'

        result_json += "}"
        return result_json

    # @property
    # def source(self):
    #     return self._source
    @property
    def expected(self):
        return self._expected
    @property
    def actual(self):
        return self._actual
    @property
    def categories(self):
        return self._categories
    @property
    def accuracy(self):
        return self._accuracy

    # @source.setter
    # def source(self, source):
    #     self._source = source
    @expected.setter
    def expected(self, expected):
        self._expected = expected
    @actual.setter
    def actual(self, actual):
        self._actual = actual
    @accuracy.setter
    def accuracy(self, accuracy):
        self._accuracy = accuracy
    @categories.setter
    def categories(self, categories):
        self._categories = categories
    # def addCategories(self, categories):
    #     for ct in categories:
    #         self._categories.add(ct)
