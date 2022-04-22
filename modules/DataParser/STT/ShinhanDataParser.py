import re
import os

from data.TestData import TestData
from modules.DataParser.AIDataParser import AIDataParser

class ShinhanDataParser(AIDataParser):
    def __init__(self, targetPath) -> None:
        super().__init__(targetPath)


    def getTestDataList(self, targetPath: str = None, limit: int = 0):
        _targetPath = self.targetPath if not targetPath else targetPath
        _testDataList = []
        _numOftd = 0

        # 정답파일
        answerFile = open(f'{_targetPath}/expect_rewritten.txt', 'r')

        for line in answerFile.readlines():
            if limit > 0 and _numOftd >= limit:  # limit number of test dataset
                break

            # read exp from result file
            div = line.split('\t')
            index = str(div[0])
            id = _targetPath[_targetPath.rindex('/')+1:] + '_' + index
            expectedList = self.extractExpectedSentence(div[1].splitlines()[0])


            # td = TestData(id=id, expectedList=expectedList, sampleFilePath=f'{_targetPath}/{index}_16000.wav')
            td = TestData(id=id, expectedList=expectedList, sampleFilePath=f'{_targetPath}/{index}.wav')
            _testDataList.append(td)
            
            _numOftd += 1

        return _testDataList


    def extractExpectedSentence(self, expectedSentence):

        headwordList = re.findall("\([\w\s]+\)[/]*", expectedSentence)         # 표제어 추출 ('괄호' 및 '/' 구분자 가정)
        sentence_div = re.sub("[/]*\([\w\s]+\)", "^", expectedSentence)
        sentence_div = re.sub("[\^]+", "^", sentence_div)           # 표제어 위치 표시된 문장 (^)

        # 표제어 리스트로 정리
        hwList = []
        tmpAry = []
        totalLen = 1

        for a in headwordList:    
            if not str.endswith(a, '/'):
                tmpAry.append(a[1:len(a)-1])
                hwList.append(tmpAry)

                totalLen *= len(tmpAry)
                tmpAry = []
            else:
                tmpAry.append(a[1:len(a)-2])

        
        # 표제어 조합 생성
        divList = [[] for i in range(totalLen)]
        
        divLen = totalLen

        for nth_hwList in hwList:
            divLen = int(divLen/len(nth_hwList))
            word_cnt = 0

            for i in range(totalLen):

                divList[i].append(nth_hwList[word_cnt])
                if i-divLen*(int(i/divLen)) == (divLen-1):
                    word_cnt = (word_cnt+1)%len(nth_hwList)

        # 구분된 단어 하나씩 sentence_div의 ^에 채워넣어 리스트로 저장 및 반환
        combList = []
        for words in divList:
            combSentence = sentence_div[:]
            for word in words:
                blank = combSentence.find('^')
                combSentence = combSentence[:blank] + word + combSentence[blank+1:]

            # 후처리 및 저장
            combSentence = re.sub("[(n\/)(u\/)(\/)]*", '', combSentence)        # ['n/', 'u/', '/'] 제거
            combList.append(combSentence.strip())

        return combList