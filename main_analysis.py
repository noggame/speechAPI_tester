import re
import config.key as key
from modules.AIDataParser.AIHubParser import AIHubParser
from modules.AIDataParser.ClovaAIParser import ClovaAIParser
import logging
import os
from datetime import datetime
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT
from modules.Accuracy.AccuracyFilter import AccuracyFilter

from modules.TestController import TestController

logging.basicConfig(filename=f'{os.getcwd()}/logs/log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

### TestData (AIHub / Clova)
# aihp = AIHubParser(f'{os.getcwd()}/sample/sample_100')
# clvp = ClovaAIParser(f'{os.getcwd()}/sample/clova_dataset')

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
# tc.addTestData(aihp)
# tc.add_STT_TestData(clvp)
tc.add_STT_API(ktapi)
tc.add_STT_API(kakaoapi)


### STT API 호출 및 결과 저장
## 전체 데이터 테스트
# sttResultList = tc.startSTTRequest(record=f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d")}.log')
## 데이터 개수 제한
# sttResultList = tc.startSTTRequest(limit=5, record=f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d")}.log')  # 개수 제한

### 테스트 결과 파일 불러와 결과 도출
# analysisResultList = tc.startAnalysisSTTResult(accuracyFilter=[AccuracyFilter.EXP_BASED, AccuracyFilter.WER],
#                                             categoryFilter=['예약', '주차', '메뉴', '영업', '시간'],
#                                             # sttResultData = sttResultList,
#                                             # file = f'{os.getcwd()}/logs/result_stt_20220127_112117.log',
#                                             targetFile = f'{os.getcwd()}/logs/0_end/cmb_48772.txt',
#                                             record = f'{os.getcwd()}/logs/analysis_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

analysisResultList = tc.getStaticInfo(accuracyFilter=[AccuracyFilter.EXP_BASED, AccuracyFilter.WER],
                                            categoryFilter=['예약', '주차', '메뉴', '영업', '시간'],
                                            sttResultData = None,
                                            # file = f'{os.getcwd()}/logs/result_stt_20220127_112117.log',
                                            targetFile = f'{os.getcwd()}/logs/0_end/cmb_48772.txt',
                                            # targetFile = f'{os.getcwd()}/logs/0_end/cmb_47182.txt',
                                            record = f'{os.getcwd()}/logs/analysis_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
# startAnalysisSTTResult(accuracyFilter=[AccuracyFilter.EXP_BASED, AccuracyFilter.WER],
#                                             categoryFilter=['예약', '주차', '메뉴', '영업', '시간'],
#                                             # sttResultData = sttResultList,
#                                             # file = f'{os.getcwd()}/logs/result_stt_20220127_112117.log',
#                                             targetFile = f'{os.getcwd()}/logs/0_end/cmb_48772.txt',
#                                             record = f'{os.getcwd()}/logs/analysis_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

