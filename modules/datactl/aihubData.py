import os
import re
import logging

class AIDataHub:

    def __init__(self, baseDir=None, targetFile=None, voiceFileExt=None) -> None:
        self._baseDir = baseDir
        self._targetFile = targetFile
        self._voiceFileExt = voiceFileExt

    @property
    def baseDir(self):
        return self._baseDir
    
    @property
    def targetFile(self):
        return self._targetFile

    @property
    def voiceFileExt(self):
        return self._voiceFileExt
    
    @baseDir.setter
    def baseDir(self, path):
        self._baseDir = str(path)

    @targetFile.setter
    def targetFile(self, targetFile):
        self._targetFile = str(targetFile)

    @voiceFileExt.setter
    def voiceFileExt(self, voiceFileExt):
        self._voiceFileExt = str(voiceFileExt)

    def getTargetList(self):
        targetList = []
        
        for root, dirs, files in os.walk(self._baseDir):
            if self._targetFile in files:
                targetList.append([os.path.join(root, self._targetFile), os.path.join(root, self._voiceFileExt)])

        return targetList

    def extractExpectedSentence(self, path):
        if path is None:
            print("[warning] path is none")
            return None

        target = open(path, 'r').readline()
        logging.info(f'[ORG] = {target}')
        
        headwords = re.findall("\([\w\s]+\)[/]*", target)         # 표제어 추출 ('괄호' 및 '/' 구분자 가정)
        sentence_div = re.sub("[/]*\([\w\s]+\)", "^", target)
        sentence_div = re.sub("[\^]+", "^", sentence_div)           # 표제어 위치 표시된 문장 (^)

        ##### 표제어 리스트로 정리
        hwList = []
        tmpAry = []
        totalLen = 1

        for a in headwords:    
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

            # 후처리 및 저장
            combSentence = re.sub("[n/\.\?]*", '', combSentence)
            combList.append(combSentence)

        logging.info(f'[EXP] = {combList}')

        return combList

