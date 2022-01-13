import logging
import re
from difflib import SequenceMatcher

def removeSpecialCharacters(sentence:str) -> str:
    return re.sub("[n/\.\?]*", '', sentence)



def calculateAccuracy_exp(expectedList, actualList):
    score = 0
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

            eachScore = round((1-totalLeftChar/expectedLen)*100, 2)

            # update result
            if eachScore > score:
                score = eachScore
                hm_expected = expected
                hm_actual = actualSTT
            # score = eachScore if eachScore > score else score


    return [hm_expected, hm_actual, score]

def calculateAccuracy_cmplib(expectedList, actualResult):
    score = 0

    for expected in expectedList:
        eachScore = 0
        eachScore = SequenceMatcher(None, expected, actualResult).ratio()
        eachScore = round(eachScore*100, 2)

        # print(f'[ACC] {eachScore} %')
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
        # print(f'[ACC] {eachScore} %')
        logging.info(f'[ACC] {eachScore} %')

        score = eachScore if eachScore > score else score

    return score
