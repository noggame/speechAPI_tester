from modules.datactl.clovaData import ClovaDataController
import os
import logging
from datetime import datetime
from pydub import AudioSegment
import time

import re
import modules.TTS.kakaoSTT as kakao_api
import modules.TTS.ktSTT as kt_api
from modules.similarity.STT.compareSTT import CompareData

# clovaCTL = ClovaDataController(voiceDir=f'{baseDir}/wavs_train', answer="train_ClovaCall.json")
clovaCTL = ClovaDataController(baseDir=f'{os.getcwd()}/sample/clova_dataset', answer="train_ClovaCall.json")
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

tmp_cnt = 10
for dataset in clovaCTL.getExpectedList():

    wav, text, speaker_id = dataset['wav'], dataset['text'], dataset['speaker_id']

    # classify
    if not any(x in text for x in ["주차"]):
        continue

    logging.info(f'{wav} / {text} / {speaker_id}')
    print(f'{wav} / {text} / {speaker_id}')
    ext_wav = f'{clovaCTL.baseDir}/wavs_train/{wav}'

    # convert wav to mp3
    ext_mp3 = ext_wav[:-4]+'.mp3'
    if not os.path.isfile(ext_mp3): # mp3 파일이 없는경우 wav 파일을 변환하여 사용
        try:
            print(ext_wav)
            voice = AudioSegment.from_file(file=ext_wav)
            voice.export(ext_mp3, format="mp3")

            while True:
                time.sleep(1)
                if os.path.isfile(ext_mp3):
                    break

        except FileNotFoundError:
            logging.exception('[Error] Fail to convert wav to mp3')

    # 기대결과
    expectedList = [re.sub("[n/\.\?]*", '', text)]
    print(f'[EXP] = {expectedList}', sep='\n')
    logging.info(f'[EXP] = {expectedList}')


    # STT 요청 및 결과비교
    ##### @@@ [implement] String Comparison/Similarity algorithm
    print("[KT]")
    sttResult_kt = kt_api.requestKtSTT(ext_mp3)             # KT STT 결과
    matchingScore['kt'] = CompareData.calculateAccuracy(expectedList, sttResult_kt)
    print("[KAKAO]")
    sttResult_kakao = kakao_api.requestKakaoSTT(ext_wav)    # KAKAO STT 결과
    matchingScore['kakao'] = CompareData.calculateAccuracy(expectedList, sttResult_kakao)


    # 결과비교
    totalScore['kt'] += matchingScore['kt']
    totalScore['kakao'] += matchingScore['kakao']

    NumOfSample += 1

    tmp_cnt-=1
    if tmp_cnt <= 0:
        break


##### 평균
avgScore['kt'] = round(totalScore['kt']/NumOfSample, 2)
print(f'\n[avg_kt] = {avgScore["kt"]}')
logging.info(f'[avg_kt] = {avgScore["kt"]}')

avgScore['kakao'] = round(totalScore['kakao']/NumOfSample, 2)
print(f'\n[avg_kko] = {avgScore["kakao"]}')
logging.info(f'[avg_kko] = {avgScore["kakao"]}')