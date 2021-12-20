from aihubData import AIDataHub
from kakaoSTT import kakaoAPI
from compareSTT import CompareData
import os
import logging
from pydub import AudioSegment
import ktstt.stt_async_client as ktapi

logging.basicConfig(filename=f'{os.getcwd()}/result_test.log', level=logging.INFO, format='%(asctime)s %(message)s')

##### get sample data list
aidata = AIDataHub(baseDir=str(os.getcwd()+"/sample_nodup"),
                    targetFile='0001.txt',
                    voiceFileExt='0001.mp3')

avgScore = 0
totalScore = 0
NumOfSample = 0


##### 분석
temp_cnt = 1                                      ################# tmp1
for txt, ext in aidata.getTargetList():
    logging.info(f'file = {txt} && wav = {ext}')
    print(txt + " - " + ext)

    if not os.path.isfile(ext): # mp3 파일이 없는경우 wav 파일을 변환하여 사용
        try:
            sound = AudioSegment.from_wav(ext[:-4]+'.wav')
            sound.export(ext, format="mp3")
        except FileNotFoundError:
            logging.exception('Fail to convert wav to mp3 file')

    # 기대결과
    expectedList = aidata.extractExpectedSentence(txt)
    print(f'[기대값] = {expectedList}', sep='\n')
    logging.info(f'[기대값] = {expectedList}')


    # 실제결과 - kt
    sttResult_kt = ktapi.requestKtSTT(ext)
    print(sttResult_kt)
    # # 실제결과 - kakao
    # kakao_api = kakaoAPI()
    # sttResult_kakao = kakao_api.requestSTT(ext)
    # print(f"[KAKAO_STT] = {sttResult_kakao}")
    # logging.info(f'[KAKAO_STT] = {sttResult_kakao}')

    # 결과비교
    #2) 기대결과 리스트 중 실제결과와 가장 일치율이 높은 점수 반환
    matchingScore={}
    matchingScore['kt'] = CompareData.compareWithKakaoSTT(expectedList, sttResult_kt)
    # matchingScore['kakao'] = CompareData.compareWithKakaoSTT(expectedList, sttResult_kakao)
    # print(f'[최고일치율] = {matchingScore}')
    # logging.info(f'[최고일치율] = {matchingScore}')

    # totalScore += matchingScore
    # NumOfSample += 1

    temp_cnt -= 1               ################# tmp1
    if temp_cnt <= 0:           ################# tmp1
        break                   ################# tmp1


##### 그래프 



##### 평균
# try:
#     avgScore = round(totalScore/NumOfSample, 2)
#     print(f'\n[평균일치율] = {avgScore}')
#     logging.info(f'[평균일치율] = {avgScore}')
# except FileNotFoundError:
#     print('not found any file')
