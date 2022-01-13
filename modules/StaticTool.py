import re
import logging
from typing import List
from data.TestResult import TestResult
from data.ResultRepository import ResultRepository


class StaticTool:

    def __init__(self, categoryList:List=[]) -> None:
        self._resultDict = {}
        self._categoryList = categoryList
        self._total = 0
        self._sumOfAccuracy = 0


    def addTestResult(self, testResult:TestResult, categoryList:List=None):
        pass

        # return result_str
        ##### 서비스별 통계
        # (1) 전체 샘플 수 = 길이
        # (2) 정홛도 합계
        # (3) 평균 정확도 = (2)/(1)
        # (4) 카테고리별 정확도 ??


    # @@@@@ 전체 통계
    # @@@@@ 카테고리별 통계

    def getStatics(self):
        staticsResult = '\n[Result]\n'

        for key in self._resultDict.keys():
            staticsResult += f'[{key}] --------------------\n'
            staticsResult += f'{self._resultDict[key]}\n'

        return staticsResult

    def categorize(self, targetList):
        categorySet = set()

        for target in targetList:
            # except [number & digit]
            if re.findall('[a-zA-Z0-9]+', target):
                return ['NA']   # Not Applicable

            # classify category
            for ct in self._categoryList:
                if re.search(ct, target):
                    categorySet.add(ct)
            
            # not matched any category
            if not len(categorySet):
                categorySet.add('NC')   # Not Classified


            # @@@@@@@@ what about empty

        return list(categorySet)
