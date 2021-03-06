
from modules.Service.APICaller.STT.KT_STT import KT_STT
from modules.Service.APICaller.STT.Kakao_STT import Kakao_STT
from modules.Service.APICaller.BaseAPICaller import BaseAPICaller
from modules.Service.APICaller.STT.VITO_STT import VITO_STT
from modules.Service.APICaller.Vision.Google_FaceDetect import Google_FaceDetection
from modules.Service.APICaller.Vision.KT_FaceDetect import KT_FaceDatect
from modules.Service.APICaller.Vision.Kakao_FaceDetect import Kakao_FaceDetect
from modules.Service.DataParser.Vision.FaceDetectParser import FaceCountingParser
from modules.Service.ResultAnalyzer.BaseResultAnalyzer import BaseResultAnalyzer
from modules.Service.ResultAnalyzer.Vision.FDResultAnalyzer import FDResultAnalyzer
from modules.Service.ResultAnalyzer.Voice.STTResultAnalyzer import STTResultAnalyzer
from modules.Service.DataParser.BaseDataParser import BaseDataParser
from modules.Service.DataParser.STT.AIHubParser import AIHubParser
from modules.Service.DataParser.STT.ClovaAIParser import ClovaAIParser
from modules.Service.Type import SERVICE_TYPE

from enum import Enum
import logging
import config.cfgParser as cfg
import os

class DataParserFactory():
    class DATA_NAME(Enum):
        AIHub = {'origin' : 'ETRI', 'type':'text'}
        ClovaAI = {'origin' : 'Naver', 'type':'text'}
        FCC = {'origin' : 'Kaggle', 'type':'image'}


    def getDataParser(self, testdata:DATA_NAME, service_type:SERVICE_TYPE, base_dir:str) -> BaseDataParser:
        if not os.path.exists(base_dir):
            logging.warning("[WARNINIG]::DataParserFactory base_dir is not found - {}".format(base_dir))

        if testdata == self.DATA_NAME.AIHub and service_type == SERVICE_TYPE.STT:
            return AIHubParser(targetPath = base_dir)
        elif testdata == self.DATA_NAME.ClovaAI and service_type == SERVICE_TYPE.STT:
            return ClovaAIParser(targetPath = base_dir)
        elif testdata == self.DATA_NAME.FCC and service_type == SERVICE_TYPE.FD: 
            return FaceCountingParser(targetFile = base_dir)
        else:
            logging.warning("[WARNINIG] {} data parser is not defined".format(testdata.name))

        return None


class ServiceFactory():
    class PROVIDER(Enum):
        KT = "KT"
        Kakao = "Kakao"
        Google = "Google"
        VITO = "VITO"


    def getAPICaller(self, service_provider:PROVIDER, service_type:SERVICE_TYPE, service_info:dict) -> BaseAPICaller:
        service_url:str = service_info['url']
        service_keys:list = service_info['keys']    # service_keys[??????][(??????, ??????)]

        ### KT_STT
        if service_provider == self.PROVIDER.KT and service_type == SERVICE_TYPE.STT:
            KT_keys = {}
            for k_name, k_value in service_keys:
                KT_keys[k_name] = k_value

            return KT_STT(url="", key=KT_keys)

        ### Kakao_STT
        elif service_provider == self.PROVIDER.Kakao and service_type == SERVICE_TYPE.STT:
            return Kakao_STT(url = service_url, key = service_keys[0][1])

        ### VITO_STT
        elif service_provider == self.PROVIDER.VITO and service_type == SERVICE_TYPE.STT:
            VITO_keys = {}
            for k_name, k_value in service_keys:
                VITO_keys[k_name] = k_value

            return VITO_STT(url=service_url, key=VITO_keys)

        ### Kakao_FaceDetection
        elif service_provider == self.PROVIDER.Kakao and service_type == SERVICE_TYPE.FD:
            return Kakao_FaceDetect(url = service_url, key = service_keys[0][1])

        ### KT_FaceDetection
        elif service_provider == self.PROVIDER.KT and service_type == SERVICE_TYPE.FD:
            return KT_FaceDatect(url = service_url)

        ### Google_FaceDetection (??????)
        # elif service_provider == self.PROVIDER.Google and service_type == SERVICE_TYPE.FD:
        #     return Google_FaceDetection(url = service_url, key = service_keys[0][1])
            
        else:
            logging.warning("[WARNINIG] {} API Caller is not defined or {} is not supperted".format(service_provider.name, service_type.name))

        return None

class AnlalyzerFactory():

    def getAnalyzer(self, service_type:SERVICE_TYPE) -> BaseResultAnalyzer:
        if service_type == SERVICE_TYPE.STT:
            return STTResultAnalyzer()
        elif service_type == SERVICE_TYPE.FD:
            return FDResultAnalyzer()
        else:
            logging.warning("[WARNINIG] {} Analyzer is not defined".format(service_type.name))

        return None
