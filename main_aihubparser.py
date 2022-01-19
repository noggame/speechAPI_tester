import re
from modules.AIDataParser.AIHubParser import AIHubParser
from modules.AIDataParser.ClovaAIParser import ClovaAIParser
import logging
import os
from datetime import datetime
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT

from modules.TestController import TestController

logging.basicConfig(filename=f'{os.getcwd()}/logs/log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

### TestData (AIHub / Clova)
# aihp = AIHubParser(f'{os.getcwd()}/sample/sample_100')
clvp = ClovaAIParser(f'{os.getcwd()}/sample/clova_dataset')

### API (KT / Kakao)
ktapi = KT_STT(options={
    'client_id':'3fd7261c-7d08-487b-a104-b867919e497b',
    'client_key':'d8613f5b-43f1-5a11-b183-35261da543a6',
    'client_secret':'693bc75a1bf4f80d2636372c02b64d0c5a636757e1b9ae6ddfd5c209f9d32892'
})
kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize',
                    key='KakaoAK 697f04dd01214c2a532634d6df4d1126')

### Test TestController
tc = TestController()
# tc.addTestData(aihp)
tc.add_STT_TestData(clvp)
tc.add_STT_API(ktapi)
tc.add_STT_API(kakaoapi)


### STT API 호출 및 결과 저장
sttResultList = tc.startSTTRequest(record=f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d")}.log')
# sttResultList = tc.startSTTRequest(limit=5, record=f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d")}.log')

### 테스트 결과 파일 불러와 결과 도출
# analysisResultList = tc.startAnalysisSTTResult(categoryFilter=['예약', '주차', '메뉴', '영업'],
#                                             # sttResultData = sttResultList,
#                                             file = f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d")}_2000.log',
#                                             record = f'{os.getcwd()}/logs/analysis_stt_{datetime.now().strftime("%Y%m%d")}.log')

