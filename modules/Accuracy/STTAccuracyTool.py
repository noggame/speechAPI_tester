import re


def calculateSTTAccuracy(expectedList:list, actualList:list) -> list:
    accuracy = 0
    hm_expected = ''    # highest matching
    hm_actual = ''

    for exp in expectedList:
        for act in actualList:
            if act == '':   # except empty result
                continue

            # except special char. and whitespace
            exp_sub = re.sub('[!@#$%^&*\(\).? ]*', '', exp)
            act_sub = re.sub('[!@#$%^&*\(\).? ]*', '', act)
            each_accuracy = round(countMatchingCharsBasedOnExpected(exp_sub, act_sub)*100/len(exp_sub), 2)

            # update
            if each_accuracy >= accuracy:
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
            if act == '':   # except empty result
                continue

            # except special char. and whitespace
            exp_sub = re.sub('[!@#$%^&*\(\).? ]*', '', exp)
            act_sub = re.sub('[!@#$%^&*\(\).? ]*', '', act)

            # cur_wer = round(countLevenshtein(exp_sub, act_sub)*100/len(exp_sub), 2)
            cur_wer = (1-countLevenshtein(exp_sub, act_sub)/len(exp_sub))*100

            if cur_wer >= final_wer:
                final_wer = cur_wer
                hm_expected = exp
                hm_actual = act

    return [hm_expected, hm_actual, final_wer]


def calculateWERAccuracyWithNomalize(expectedList:list, actualList:list) -> list:
    final_wer = 0
    hm_expected = ''    # highest matching
    hm_actual = ''

    for exp in expectedList:
        for act in actualList:
            if act == '':   # except empty result
                continue

            # except special char. and whitespace
            exp_sub = re.sub('[!@#$%^&*\(\).? ]*', '', exp)
            act_sub = re.sub('[!@#$%^&*\(\).? ]*', '', act)

            ldl, correction = levenshteinDistanceList(exp_sub, act_sub)
            sum_ldl = sum(ldl)
            cur_wer = (1-sum_ldl/(sum_ldl+correction-ldl[0]))*100

            print(ldl, correction)

            if ldl[0] > 0 and cur_wer <= 0:     # nomalize
                cur_wer = (1-sum_ldl/(sum_ldl+correction))*100

            if cur_wer >= final_wer:
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


def levenshteinDistanceList(cmp1, cmp2):
    cmpAry = [[0 for i in range(len(cmp2)+1)] for j in range(len(cmp1)+1)]
    correction = 0

    # initialisation
    for i in range(len(cmp1)+1):
        for j in range(len(cmp2)+1):
            # [Insertion, Deletion, Substituion]
            if i == 0:
                cmpAry[0][j] = [0, j, 0]
            elif j == 0:
                cmpAry[i][0] = [i, 0, 0]

    # calculation
    for i in range(1, len(cmp1)+1):
        isMatched = False

        for j in range(1, len(cmp2)+1):
            # print(cmp1[i-1], cmp2[j-1])
            if cmp1[i-1] == cmp2[j-1]:
                cmpAry[i][j] = cmpAry[i-1][j-1]
                if not isMatched:
                    correction += 1
                    isMatched = True
                # print(cmpAry[i][j])
            else:
                insertion = sum(cmpAry[i][j-1]) + 1
                deletion = sum(cmpAry[i-1][j]) + 1
                substitution = sum(cmpAry[i-1][j-1]) + 1
                minValue = min(insertion, deletion, substitution)

                # print(insertion, deletion, substitution)

                if minValue == substitution:
                    cmpAry[i][j] = [cmpAry[i-1][j-1][0], cmpAry[i-1][j-1][1], cmpAry[i-1][j-1][2]+1]
                elif minValue == insertion:
                    cmpAry[i][j] = [cmpAry[i][j-1][0]+1, cmpAry[i][j-1][1], cmpAry[i][j-1][2]]
                elif minValue == deletion:
                    cmpAry[i][j] = [cmpAry[i-1][j][0], cmpAry[i-1][j][1]+1, cmpAry[i-1][j][2]]
                # print(cmpAry[i][j])
                    
    return cmpAry[len(cmp1)][len(cmp2)], correction



def categorizeSTT(expected:str, actual:str, categoryFilter:list, isNA:bool=False):
    categorySet = set()

    # except [number & digit]
    # if re.findall('[a-zA-Z0-9]+', expected + actual) or len(actual) == 0:
    if isNA or len(actual) == 0:
        return ['NA']   # Not Applicable

    # classify category
    for ct in categoryFilter:
        if re.search(ct, expected):
            categorySet.add(ct)
    
    # not matched any category
    if not len(categorySet):
        categorySet.add('NC')   # Not Classified

    return list(categorySet)


