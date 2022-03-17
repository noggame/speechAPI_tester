import logging
import os
from datetime import datetime
from data.TestResult import TestResult
from modules.APICaller.STT.Kakao_STT import Kakao_STT
from modules.TestController import TestController
from modules.AIDataParser.ShinhanDataParser import ShinhanDataParser

# Analysis
from modules.Accuracy.AccuracyFilter import AccuracyFilter

logging.basicConfig(filename=f'{os.getcwd()}/logs/log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')


tc = TestController()

# set data
_targetPath = '/mnt/d/Workspace/python/speechAPI_tester/sample/shinhan/1_20220111_101404438_2011.raw_Callee'
sdp = ShinhanDataParser(f'{_targetPath}')
tc.add_STT_TestData(sdp)

# set api
kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize', key='KakaoAK 697f04dd01214c2a532634d6df4d1126') # SDH
tc.add_STT_API(kakaoapi)

# test
sttResultList = tc.startSTTRequest(record=f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')    # 전체 데이터 테스트

# # analysis
# analysisResultList = tc.getStaticInfo(accuracyFilter=[AccuracyFilter.EXP_BASED, AccuracyFilter.WER],
#                                             categoryFilter=['예약', '주차', '메뉴', '영업', '시간'],
#                                             sttResultData = None,
#                                             # file = f'{os.getcwd()}/logs/result_stt_20220127_112117.log',
#                                             targetFile = f'{os.getcwd()}/logs/result_stt_20220315_133525.txt',
#                                             # targetFile = f'{os.getcwd()}/logs/0_end/cmb_47182.txt',
#                                             record = f'{os.getcwd()}/logs/analysis_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')