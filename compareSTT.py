import re

class CompareData:

    def __init__(self) -> None:
        pass

    def compareWithKakaoSTT(expectedList, actualResult):
        actualDic = {}
        actualLen = 0
        score = 0

        # counting chars
        for ch in actualResult:
            if ch is ' ':
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
            print(f"EXP Result = {expected} ({eachScore} %)")
            score = eachScore if eachScore > score else score

        return score