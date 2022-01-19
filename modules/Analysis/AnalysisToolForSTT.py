from data.TestResult import TestResult
import re
import logging


# 정확도 정보 어떤걸 리턴할지 모두 정의해서 사용 (현재는 expected 기준만 반영됨)
def calculateSTTAccuracy(expectedList:list, actualList:list) -> dict:
    accuracy = 0
    hm_expected = ''    # highest matching
    hm_actual = ''

    if not actualList:
        return ['', '', 0]

    # cmp chars with expected sentence
    for expected in expectedList:
        expectedDic = {}
        expectedLen = 0

        expected_nonSpecChar = re.sub('[!@#$%^&*\(\).?]*', '', expected)
        # counting chars
        for ch in expected_nonSpecChar:
            if ch==' ':
                continue
            else:            
                expectedDic[ch] = int(1) if expectedDic.get(ch) is None else expectedDic[ch]+1
                expectedLen += 1

        # scoring
        for actualSTT in actualList:
            expectedDicCopy = expectedDic.copy()

            for ch in actualSTT:
                if ch == ' ':
                    continue
                elif expectedDicCopy.get(ch) is not None:
                    if expectedDicCopy[ch] == 1:
                        expectedDicCopy.pop(ch)
                    else:
                        expectedDicCopy[ch] -= 1

            leftChar = 0
            totalLeftChar = 0
            for leftChar in expectedDicCopy:
                totalLeftChar += expectedDicCopy.get(leftChar)

            eachAccuracy = round((1-totalLeftChar/expectedLen)*100, 2)

            # update result
            if eachAccuracy > accuracy:
                accuracy = eachAccuracy
                hm_expected = expected
                hm_actual = actualSTT
            # score = eachScore if eachScore > score else score


    return [hm_expected, hm_actual, accuracy]
    # testReusltRepo 

    # if not self.testResultRepo:
    #     logging.exception(f'[Exception] {__class__.__name__}:{__name__} - Test result data is empty.')
    #     return

    # for tr in self.testResultRepo:
    #     print(tr)
    # return {}
    # pass






def calculateInstDeltAccuracy(expected:list, actual:list) -> float:
    # 정확도 계산후 값 반환
    pass

def classifySentence(expected:list, actual:list):
    pass



def categorizeSTT(expected:str, actual:str, categoryFilter:list=None):
    categorySet = set()

    # except [number & digit]
    if re.findall('[a-zA-Z0-9]+', expected+actual) or len(actual) == 0:
        return ['NA']   # Not Applicable

    # classify category
    for ct in categoryFilter:
        if re.search(ct, expected):
            categorySet.add(ct)
    
    # not matched any category
    if not len(categorySet):
        categorySet.add('NC')   # Not Classified

    return list(categorySet)