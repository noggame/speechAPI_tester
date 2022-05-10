import os
import re
import logging

from data.TestData import TestData
from modules.DataParser.AIDataParser import AIDataParser

class AIHubParser(AIDataParser):
    def __init__(self, targetPath) -> None:
        super().__init__(targetPath)


    def getTestDataList(self, targetPath: str = None, limit: int = 0):
        _targetPath = self.targetPath if not targetPath else targetPath
        _testDataList = []
        _numOftd = 0

        try:
            for root, dirs, files in os.walk(f"{_targetPath}/라벨링데이터"):
                if limit > 0 and _numOftd >= limit:  # limit number of test dataset
                    break

                answerFile = None
                soundFile = None

                for file in files:
                    if file.endswith(".txt"):
                        answerFile = f"{root}/{file}"
                        soundFile = answerFile.replace("라벨링데이터", "원천데이터")
                        soundFile = f"{soundFile[:-4]}.wav"

                        # id
                        idx_id_form_root = answerFile.rindex("KrespSpeech")
                        id = answerFile[idx_id_form_root+len("KrespSpeech"):0-len(file)]
                        id = ''.join(id.split('/'))

                        # expectedList
                        expList = self.extractExpectedSentence(expectedInfoFile = answerFile)

                        # test data
                        td = TestData(id=id, expectedList=expList, sampleFilePath=soundFile)
                        print(td)
                        _testDataList.append(td)

                        # inc.
                        _numOftd += 1

        except FileNotFoundError:
            logging.error('[ERR] AIHubParser - ExpectedTargetDirectory not found. check the target path')

        return _testDataList


    ### deprecated
    # def getTestDataList(self, targetPath: str = None, limit: int = 0):
    #     _targetPath = self.targetPath if not targetPath else targetPath
    #     _testDataList = []
    #     _numOftd = 0

    #     try:
    #         for root, dirs, files in os.walk(_targetPath):
    #             if limit > 0 and _numOftd >= limit:  # limit number of test dataset
    #                 break

    #             expInfoPath = f'{root}/0001.txt'
    #             soundFilePath = f'{root}/0001.wav'

    #             if not pathlib.Path(expInfoPath).exists():  # except directory
    #                 continue

    #             # id
    #             id = root.split('/')
    #             id = id[len(id)-1]

    #             # expectedList
    #             expList = self.extractExpectedSentence(expectedInfoFile = expInfoPath)

    #             # test data
    #             td = TestData(id = id, expectedList=expList, sampleFilePath=soundFilePath)
    #             _testDataList.append(td)

    #             # inc.
    #             _numOftd += 1

    #     except FileNotFoundError:
    #         logging.error('[ERR] AIHubParser - ExpectedTargetDirectory not found. check the target path')

    #     return _testDataList


    def extractExpectedSentence(self, expectedInfoFile):
        expectedSentence = ''

        try:
            expectedSentence = open(expectedInfoFile, 'r').readline()
        except FileNotFoundError:
            logging.error('[ERR] AIHubParser - ExpectedInfoFile not found. check the expected information file path')

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
            combList.append(f"\"{combSentence.strip()}\"")

        return combList
