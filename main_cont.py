import re
import config.key as key
from modules.AIDataParser.STT.AIHubParser import AIHubParser
from modules.AIDataParser.STT.ClovaAIParser import ClovaAIParser
import logging
import os
from datetime import datetime
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT

from modules.TestController import TestController

logging.basicConfig(filename=f'{os.getcwd()}/logs/log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

## set Sample
# aihp = AIHubParser(f'{os.getcwd()}/sample/sample_100')        # AIHub
clvp = ClovaAIParser(f'{os.getcwd()}/sample/clova_dataset')   # ClovaAI

## set API
# KT
ktapi = KT_STT(options={
    'client_id': key.kt['client_id'],
    'client_key': key.kt['client_key'],
    'client_secret': key.kt['client_secret']
})

# KAKAO
kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize', key=key.kakao['SDH'])       # SDH
# kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize', key=key.kakao['KJH'])         # KJH
# # kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize', key=key.kakao['YJE'])       # YJE

### Test TestController
tc = TestController()
# tc.add_STT_TestData(aihp)
tc.add_STT_TestData(clvp)
tc.add_STT_API(ktapi)
tc.add_STT_API(kakaoapi)


### STT API 호출 및 결과 저장
sttResultList = tc.startSTTRequest(record=f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')    # 전체 데이터 테스트
# sttResultList = tc.startSTTRequest(limit=10, record=f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log') # 데이터 개수 제한

### 테스트 결과 파일 불러와 결과 도출
# analysisResultList = tc.startAnalysisSTTResult(categoryFilter=['예약', '주차', '메뉴', '영업'],
#                                             # sttResultData = sttResultList,
#                                             # file = f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d")}_2000.log',
#                                             # record = f'{os.getcwd()}/logs/analysis_stt_{datetime.now().strftime("%Y%m%d")}.log')
#                                             file = f'{os.getcwd()}/logs/result_stt_20220124_3000.log',
#                                             record = f'{os.getcwd()}/logs/analysis_stt_{datetime.now().strftime("%Y%m%d")}.log')

