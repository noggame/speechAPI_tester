from data.TestResult import TestResult
import re


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


def calculateWERAccuracy(expectedList:list, actualList:list) -> list:
    final_wer = 0
    hm_expected = ''    # highest matching
    hm_actual = ''

    for exp in expectedList:
        for act in actualList:

            # except special char. and whitespace
            exp_sub = re.sub('[!@#$%^&*\(\).? ]*', '', exp)
            act_sub = re.sub('[!@#$%^&*\(\).? ]*', '', act)

            # cur_wer = round(countLevenshtein(exp_sub, act_sub)*100/len(exp_sub), 2)
            cur_wer = (1-countLevenshtein(exp_sub, act_sub)/len(exp_sub))*100

            if cur_wer > final_wer:
                final_wer = cur_wer
                hm_expected = exp
                hm_actual = act

    return [hm_expected, hm_actual, final_wer]


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


def countLevenshtein(cmp1, cmp2):
    cmpAry = [[0 for i in range(len(cmp2)+1)] for j in range(len(cmp1)+1)]

    # initialisation
    for i in range(len(cmp1)+1):
        for j in range(len(cmp2)+1):
            if i == 0:
                cmpAry[0][j] = j
            elif j == 0:
                cmpAry[i][0] = i

    # calculation
    for i in range(1, len(cmp1)+1):
        for j in range(1, len(cmp2)+1):
            if cmp1[i-1] == cmp2[j-1]:
                cmpAry[i][j] = cmpAry[i-1][j-1]
            else:
                substitution = cmpAry[i-1][j-1] + 1
                insertion = cmpAry[i][j-1] + 1
                deletion = cmpAry[i-1][j] + 1
                cmpAry[i][j] = min(substitution, insertion, deletion)

    return cmpAry[len(cmp1)][len(cmp2)]



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


