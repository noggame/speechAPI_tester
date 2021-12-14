import os
import re
import json

class AIDataHub:

    def __init__(self, baseDir=None, targetFile=None, wavFile=None) -> None:
        self._baseDir = baseDir
        self._targetFile = targetFile
        self._wavFile = wavFile

    @property
    def baseDir(self):
        return self._baseDir
    
    @property
    def targetFile(self):
        return self._targetFile

    @property
    def wavFile(self):
        return self._wavFile
    
    @baseDir.setter
    def baseDir(self, path):
        self._baseDir = str(path)

    @targetFile.setter
    def targetFile(self, targetFile):
        self._targetFile = str(targetFile)

    @wavFile.setter
    def wavFile(self, wavFile):
        self._wavFile = str(wavFile)

    def getTargetList(self):
        targetList = []
        
        for root, dirs, files in os.walk(self._baseDir):
            if self._targetFile in files:
                targetList.append([os.path.join(root, self._targetFile), os.path.join(root, self._wavFile)])


        return targetList

    def getExpectedResultList(self, sentence):
        ################# 파일경로 입력받아서 기대값 추출
        # print("[원본] " + sentence)
        
        headwords = re.findall("\([\w\s]+\)[/]*", sentence)         # 표제어 추출 ('괄호' 및 '/' 구분자 가정)
        sentence_div = re.sub("[/]*\([\w\s]+\)", "^", sentence)
        sentence_div = re.sub("[\^]+", "^", sentence_div)           # 표제어 위치 표시된 문장 (^)

        ##### 표제어 리스트로 정리
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

        
        ##### 표제어 조합 생성
        divList = [[] for i in range(totalLen)]
        
        divLen = totalLen

        for nth_hwList in hwList:
            divLen = int(divLen/len(nth_hwList))
            word_cnt = 0

            for i in range(totalLen):

                divList[i].append(nth_hwList[word_cnt])
                if i-divLen*(int(i/divLen)) == (divLen-1):
                    word_cnt = (word_cnt+1)%len(nth_hwList)

        ##### 구분된 단어 하나씩 sentence_div의 ^에 채워넣어 리스트로 저장 및 반환
        combList = []
        for words in divList:
            combSentence = sentence_div[:]
            for word in words:
                blank = combSentence.find('^')
                combSentence = combSentence[:blank] + word + combSentence[blank+1:]

            combList.append(combSentence)

        return combList

    def extractExpectedSentence(self, path):
        target = open(path, 'r')
        
        print(target.readline()[3:])

