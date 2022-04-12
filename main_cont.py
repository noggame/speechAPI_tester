import re
import config.cfgParser as cfg
from modules.DataParser.STT.AIHubParser import AIHubParser
from modules.DataParser.STT.ClovaAIParser import ClovaAIParser
import logging
import os
from datetime import datetime
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT

from modules.TestController import TestController

logging.basicConfig(filename=f'{os.getcwd()}/logs/log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')


### Test TestController
tc = TestController()
# tc.add_STT_TestData(AIHubParser(f'{os.getcwd()}/sample/sample_100'))
tc.add_STT_TestData(ClovaAIParser(f'{os.getcwd()}/sample/clova_dataset'))
tc.add_STT_API(KT_STT(options={'client_id': cfg.get('kt', 'cliend_id'), 'client_key': cfg.get('kt', 'client_key'), 'client_secret': cfg.get('kt', 'cliend_secret')}))
tc.add_STT_API(Kakao_STT(url=cfg.get('kt', 'url_stt'), key=cfg.get('kt', 'key_sdh')))


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

