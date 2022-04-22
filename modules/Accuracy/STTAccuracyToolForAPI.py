import logging
import os
import config.cfgParser as cfg
from datetime import datetime
from modules.TestController import TestController
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT
from modules.DataParser.STT.AIHubParser import AIHubParser
from modules.DataParser.STT.ClovaAIParser import ClovaAIParser

# Analysis
from modules.Accuracy.AccuracyFilter import AccuracyFilter
from datetime import datetime


class STTAccuracyTool:

    def __init__(self) -> None:
        self._tc = TestController()

    def STTtestWith(self, data_name, api_name, number=0):
        now = datetime.now()
        current_time = now.strftime("%Y%m%d_%H%M%S_")
        time_stamp = str(current_time)+str(now.microsecond)

        # Log
        logging.basicConfig(filename=f'{os.getcwd()}/logs/log_{time_stamp}.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
        
        # data
        target_data = self.__setTestData(data_name)

        # API
        target_api = self.__setAPIwith(api_name)

        if target_data == None or target_api == None:
            return None

        # STT API 호출 및 결과 저장
        resultLogPath = f'{os.getcwd()}/logs/result_stt_{time_stamp}.log'
        sttResultList = self._tc.startSTTRequest(limit=number, record=f'{resultLogPath}')    # 전체 데이터 테스트
        # sttResultList = tc.startSTTRequest(limit=10, record=f'{os.getcwd()}/logs/result_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log') # 데이터 개수 제한

        ### 테스트 결과 파일 불러와 결과 도출
        analysisResultList = self._tc.startAnalysisSTTResult(accuracyFilter=[AccuracyFilter.WER],
                                                    categoryFilter=[],
                                                    sttResultData = None,
                                                    # sttResultData = sttResultList,
                                                    targetFile = f'{resultLogPath}',
                                                    record = f'{os.getcwd()}/logs/analysis_stt_{time_stamp}.log')

        return analysisResultList


    def __setTestData(self, data_name, number=0):
        ### @@@@@@@@@@@@@ DB 또는 로컬에서 data_name으로 data를 찾아 반환
        target_data = None

        if data_name == 'ClovaCall':
            target_data = ClovaAIParser(f'{os.getcwd()}/sample/clova_dataset')   # ClovaAI
        elif data_name == 'AIHub':
            target_data = AIHubParser(f'{os.getcwd()}/sample/sample_100')        # AIHub

        
        if target_data:
            self._tc.add_STT_TestData(target_data)
        
        return target_data


    def __setAPIwith(self, api_name):
        target_api = None

        if api_name == 'KT':
            target_api = KT_STT(options={
                'client_id': cfg.get('kt', 'client_id'),
                'client_key': cfg.get('kt', 'client_key'),
                'client_secret': cfg.get('kt', 'client_secret')
            })

        elif api_name == 'Kakao':
            target_api = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize', key=cfg.get('kakao', 'key_sdh'))       # SDH
            # kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize', key=key.kakao['KJH'])         # KJH
            # kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize', key=key.kakao['YJE'])         # YJE


        if target_api:
            self._tc.add_STT_API(target_api)

        return target_api
        






