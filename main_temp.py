import re
import modules.Analysis.AnalysisToolForSTT as ast

def countMatchingCharsBasedOnExpected(expected:str, actual:str):

    # make a strDict
    expectedDict = {}
    for ch in expected:
        if ch not in expectedDict:
            expectedDict[ch] = 0
        expectedDict[ch] += 1

    # count diff
    matched = 0
    for ch in actual:
        if ch not in expectedDict:
            continue

        matched += 1
        if expectedDict[ch] == 1:
            expectedDict.pop(ch)
        else:
            expectedDict[ch] -= 1

    return matched

def calculateSTTAccuracy(expectedList:list, actualList:list) -> list:
    accuracy = 0
    hm_expected = ''    # highest matching
    hm_actual = ''

    for exp in expectedList:
        for act in actualList:
            exp_sub = re.sub('[!@#$%^&*\(\).? ]*', '', exp)
            act_sub = re.sub('[!@#$%^&*\(\).? ]*', '', act)
            each_accuracy = round(countMatchingCharsBasedOnExpected(exp_sub, act_sub)*100/len(exp_sub), 2)

            # update
            if each_accuracy > accuracy:
                accuracy = each_accuracy
                hm_expected = exp
                hm_actual = act

    return [hm_expected, hm_actual, accuracy]


s = ['가와! 나#와 다', '안녕하세요']
cmp = ['가나다', '가와 나와 다']

print(calculateSTTAccuracy(s, cmp))