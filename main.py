
from aihubData import AIDataHub
from kakaoSTT import kakaoAPI
from compareSTT import CompareData
import os
import logging

logging.basicConfig(filename=f'{os.getcwd()}/result_test.log', level=logging.INFO, format='%(asctime)s %(message)s')

##### get sample data list
aidata = AIDataHub(baseDir=str(os.getcwd()+"/sample_nodup"),
                    targetFile='0001.txt',
                    wavFile='0001.wav')

avgScore = 0
totalScore = 0
NumOfSample = 0


##### 분석
temp_cnt = 1                                      ################# tmp1
for txt, wav in aidata.getTargetList():
    logging.info(f'file = {txt} && wav = {wav}')
    print(txt + " - " + wav)

    # 기대결과
    expectedList = aidata.extractExpectedSentence(txt)
    print(f'[기대값] = {expectedList}', sep='\n')
    logging.info(f'[기대값] = {expectedList}')

    # 실제결과
    k_api = kakaoAPI()
    k_sttResult = k_api.requestSTT(wav)
    print(f"[KAKAO_STT] = {k_sttResult}")
    logging.info(f'[KAKAO_STT] = {k_sttResult}')

    # 결과비교
    #2) 기대결과 리스트 중 실제결과와 가장 일치율이 높은 점수 반환
    matchingScore = CompareData.compareWithKakaoSTT(expectedList, k_sttResult)
    print(f'[최고일치율] = {matchingScore}')
    logging.info(f'[최고일치율] = {matchingScore}')

    totalScore += matchingScore
    NumOfSample += 1

    temp_cnt -= 1               ################# tmp1
    if temp_cnt <= 0:           ################# tmp1
        break                   ################# tmp1


##### 그래프 



##### 평균
try:
    avgScore = round(totalScore/NumOfSample, 2)
    print(f'\n[평균일치율] = {avgScore}')
    logging.info(f'[평균일치율] = {avgScore}')
except FileNotFoundError:
    print('not found any file')
