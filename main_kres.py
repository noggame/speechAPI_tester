# official
import os
import logging
import time
from datetime import datetime
from pydub import AudioSegment
# user defined
import modules.TTS.kakaoSTT as kakao_api
import modules.TTS.ktSTT as kt_api
from modules.datactl.aihubData import AIDataHub
from modules.compareSTT import CompareData


##### get sample list
aidata = AIDataHub(baseDir=str(os.getcwd()+"/sample/sample_nodup"),
                    targetFile='0001.txt',
                    voiceFileExt='0001.wav')
logging.basicConfig(filename=f'{os.getcwd()}/logs/result_test_{datetime.now().strftime("%Y%d%m%H%M%S")}.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

totalScore = {
    'kt':0,
    'kakao':0
}
avgScore = {
    'kt':0,
    'kakao':0
}
matchingScore = {}
NumOfSample = 0


##### 분석
# temp_cnt = 1                                      ################# tmp1
for txt, ext_wav in aidata.getTargetList():
    logging.info(f'file = {txt} && wav = {ext_wav}')
    print(txt + " - " + ext_wav)

    # convert wav to mp3
    ext_mp3 = ext_wav[:-4]+'.mp3'
    if not os.path.isfile(ext_mp3): # mp3 파일이 없는경우 wav 파일을 변환하여 사용
        try:
            print(ext_wav)
            voice = AudioSegment.from_file(file=ext_wav)
            voice.export(ext_mp3, format="mp3")

            while True:
                time.sleep(1)
                print('sleep')
                if os.path.isfile(ext_mp3):
                    break

        except FileNotFoundError:
            logging.exception('Fail to convert wav to mp3 file')

    

    # 기대결과
    expectedList = aidata.extractExpectedSentence(txt)
    print(f'[EXP] = {expectedList}', sep='\n')


    # STT 요청 및 결과비교
    ##### @@@ [implement] String Comparison/Similarity algorithm
    sttResult_kt = kt_api.requestKtSTT(ext_mp3)             # KT STT 결과
    matchingScore['kt'] = CompareData.calculateAccuracy(expectedList, sttResult_kt)
    sttResult_kakao = kakao_api.requestKakaoSTT(ext_wav)    # KAKAO STT 결과
    matchingScore['kakao'] = CompareData.calculateAccuracy(expectedList, sttResult_kakao)


    # 결과비교
    totalScore['kt'] += matchingScore['kt']
    totalScore['kakao'] += matchingScore['kakao']

    NumOfSample += 1

    # temp_cnt -= 1               ################# tmp1
    # if temp_cnt <= 0:           ################# tmp1
    #     break                   ################# tmp1


##### 그래프 



##### 평균
avgScore['kt'] = round(totalScore['kt']/NumOfSample, 2)
print(f'\n[avg_kt] = {avgScore["kt"]}')
logging.info(f'[avg_kt] = {avgScore["kt"]}')

avgScore['kakao'] = round(totalScore['kakao']/NumOfSample, 2)
print(f'\n[avg_kko] = {avgScore["kakao"]}')
logging.info(f'[avg_kko] = {avgScore["kakao"]}')

