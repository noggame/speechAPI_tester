import os
import re

def splitSentence(sentence):
    print("[원본] " + sentence)
    
    headwords = re.findall("\([\w\s]+\)[/]*", sentence)         # 표제어 추출
    sentence_div = re.sub("[/]*\([\w\s]+\)", "^", sentence)
    sentence_div = re.sub("[\^]+", "^", sentence_div)           # 표제어 위치 표시된 문장

    ### 표제어 리스트로 정리
    hwList = []
    totalLen = 1
    tmpAry = []
    for a in headwords:
        # list에 추가
        if not str.endswith(a, '/'):
            tmpAry.append(a[1:len(a)-1])
            hwList.append(tmpAry)

            totalLen *= len(tmpAry)
            tmpAry = []
        else:
            tmpAry.append(a[1:len(a)-2])

    # print(hwList)    # check
    
    ### 표제어 조합 생성
    combList = [[] for i in range(totalLen)]
    
    divLen = totalLen

    for nth_hwList in hwList:
        divLen = int(divLen/len(nth_hwList))
        word_cnt = 0

        for i in range(totalLen):

            combList[i].append(nth_hwList[word_cnt])
            if i-divLen*(int(i/divLen)) == (divLen-1):
                word_cnt = (word_cnt+1)%len(nth_hwList)

    # print(combList)     # check


    ################# 구분된 단어 하나씩 sentence_div의 ^에 채워넣어 리스트로 저장 및 반환

    return combList


result = splitSentence("안녕하세요 (만나서)/(처음 뵈었지만) 반갑습니다. 오늘은 (날씨가)/(기분이)/(공기가) (매우)/(정말) 좋습니다")

# print(result)