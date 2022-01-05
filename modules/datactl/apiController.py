from modules.datactl.clovaData import ClovaDataController
import os
import logging
from datetime import datetime
from pydub import AudioSegment
import time

import re
import modules.TTS.kakaoSTT as kakao_api
import modules.TTS.ktSTT as kt_api
from modules.compareSTT import CompareData



def makeSTTResultWithClovaData(writeFilePath=f'{os.getcwd()}/data/tts_result/result_clova_{datetime.now().strftime("%Y%d%m%H%M%S")}.log',
                                targetBasePath=f'{os.getcwd()}/sample/clova_dataset',
                                answerFileName="train_ClovaCall.json",
                                numOfSample:int = -1):

    # init.
    clovaCTL = ClovaDataController(baseDir = targetBasePath, answer = answerFileName)
    fw = open(writeFilePath, 'w')
    
    
    SampleIdx = 1
    for dataset in clovaCTL.getExpectedList():

        wav, text, speaker_id = dataset['wav'], dataset['text'], dataset['speaker_id']

        # define classification rule if you need (ex_ 주차 / 예약 / ... )
        # if not any(x in text for x in ["주차"]):
        #       fw.write(f'[SKIP] {wav} / {text} / {speaker_id}')
        #       continue
        
        fw.write(f'{wav} / {text} / {speaker_id}')
        
        # logging.info(f'{wav} / {text} / {speaker_id}')
        # print(f'{wav} / {text} / {speaker_id}')
        ext_wav = f'{clovaCTL.baseDir}/wavs_train/{wav}'
        

        # mp3 파일이 없는경우 wav 파일을 변환하여 사용
        ext_mp3 = ext_wav[:-4]+'.mp3'
        if not os.path.isfile(ext_mp3): 
            try:
                voice = AudioSegment.from_file(file=ext_wav)
                voice.export(ext_mp3, format="mp3")
                logging.exception(f'[SUCCESS] convert {ext_wav} wav to mp3')

                while True:
                    time.sleep(1)
                    if os.path.isfile(ext_mp3):
                        break

            except FileNotFoundError:
                fw.write('[ERROR] Fail to converting wav to mp3')
                logging.exception('[ERROR] Fail to converting wav to mp3')


        # 기대결과
        expectedList = [re.sub("[n/\.\?]*", '', text)]
        logging.info(f'[EXP] = {expectedList}')


        # STT 요청 및 결과비교
        ##### @@@ [implement] String Comparison/Similarity algorithm
        sttResult_kt = kt_api.requestKtSTT(ext_mp3)             # KT STT 결과
        # matchingScore['kt'] = CompareData.calculateAccuracy(expectedList, sttResult_kt)

        sttResult_kakao = kakao_api.requestKakaoSTT(ext_wav)    # KAKAO STT 결과
        # matchingScore['kakao'] = CompareData.calculateAccuracy(expectedList, sttResult_kakao)


        # 결과비교
        # totalScore['kt'] += matchingScore['kt']
        # totalScore['kakao'] += matchingScore['kakao']

        SampleIdx += 1

        if numOfSample == -1:
            continue
        elif numOfSample < SampleIdx:
            break


    ##### 평균
    avgScore['kt'] = round(totalScore['kt']/NumOfSample, 2)
    print(f'\n[avg_kt] = {avgScore["kt"]}')
    logging.info(f'[avg_kt] = {avgScore["kt"]}')

    avgScore['kakao'] = round(totalScore['kakao']/NumOfSample, 2)
    print(f'\n[avg_kko] = {avgScore["kakao"]}')
    logging.info(f'[avg_kko] = {avgScore["kakao"]}')