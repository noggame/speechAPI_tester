import logging
from difflib import SequenceMatcher

def calculateAccuracy_cmplib(expectedList, actualResult):
    score = 0

    for expected in expectedList:
        eachScore = 0
        eachScore = SequenceMatcher(None, expected, actualResult).ratio()
        eachScore = round(eachScore*100, 2)

        print(f'[ACC] {eachScore} %')
        logging.info(f'[ACC] {eachScore} %')

        score = eachScore if eachScore > score else score

    return score

def calculateAccuracy_exp(expectedList, actualResult):

    score = 0

    # cmp chars with expected sentence
    for expected in expectedList:
        expectedDic = {}
        expectedLen = 0

        # counting chars
        for ch in expected:
            if ch == ' ':
                continue
            else:            
                expectedDic[ch] = int(1) if expectedDic.get(ch) is None else expectedDic[ch]+1
                expectedLen += 1

        # score
        for ch in actualResult:
            if ch == ' ':
                continue
            elif expectedDic.get(ch) is not None:
                if expectedDic[ch] == 1:
                    expectedDic.pop(ch)
                else:
                    expectedDic[ch] -= 1

        leftChar = 0
        totalLeftChar = 0
        for leftChar in expectedDic:
            totalLeftChar += expectedDic.get(leftChar)

        eachScore = round((1-totalLeftChar/expectedLen)*100, 2)
        print(f'[ACC] {eachScore} %')
        logging.info(f'[ACC] {eachScore} %')

        score = eachScore if eachScore > score else score

    return score


def calculateAccuracy_actual(expectedList, actualResult):
    actualDic = {}
    actualLen = 0
    score = 0

    # counting chars
    for ch in actualResult:
        if ch == ' ':
            continue
        else:            
            actualDic[ch] = int(1) if actualDic.get(ch) is None else actualDic[ch]+1
            actualLen += 1

    # cmp chars with expected sentence
    for expected in expectedList:
        cmpDic = actualDic.copy()

        # score
        for ch in expected:
            if ch == ' ':
                continue
            elif cmpDic.get(ch) is not None:
                if cmpDic[ch] == 1:
                    cmpDic.pop(ch)
                else:
                    cmpDic[ch] -= 1

        leftChar = 0
        totalLeftChar = 0
        for leftChar in cmpDic:
            totalLeftChar += cmpDic.get(leftChar)

        eachScore = round((1-totalLeftChar/actualLen)*100, 2)
        print(f'[ACC] {eachScore} %')
        logging.info(f'[ACC] {eachScore} %')

        score = eachScore if eachScore > score else score

    return score
# class CompareData:

#     def __init__(self) -> None:
#         pass

#     # def compareWithKakaoSTT(expectedList, actualResult):
#     def calculateAccuracy(expectedList, actualResult):
#         actualDic = {}
#         actualLen = 0
#         score = 0

#         # counting chars
#         for ch in actualResult:
#             if ch == ' ':
#                 continue
#             else:            
#                 actualDic[ch] = int(1) if actualDic.get(ch) is None else actualDic[ch]+1
#                 actualLen += 1

#         # cmp chars with expected sentence
#         for expected in expectedList:
#             cmpDic = actualDic.copy()

#             # score
#             for ch in expected:
#                 if ch == ' ':
#                     continue
#                 elif cmpDic.get(ch) is not None:
#                     if cmpDic[ch] == 1:
#                         cmpDic.pop(ch)
#                     else:
#                         cmpDic[ch] -= 1

#             leftChar = 0
#             totalLeftChar = 0
#             for leftChar in cmpDic:
#                 totalLeftChar += cmpDic.get(leftChar)

#             eachScore = round((1-totalLeftChar/actualLen)*100, 2)
#             print(f'>> {expected} (acc : {eachScore} %)')
#             logging.info(f'>> {expected} (acc : {eachScore} %)')

#             score = eachScore if eachScore > score else score

#         return score