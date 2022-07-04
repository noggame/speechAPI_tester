
from modules.Service.APICaller.STT.KT_STT import KT_STT
from modules.Service.APICaller.STT.Kakao_STT import Kakao_STT
from modules.Service.APICaller.BaseAPICaller import BaseAPICaller
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

class DataParserFactory():
    class DATA_NAME(Enum):
        AIHub = {'origin' : 'ETRI', 'type':'text'}
        ClovaAI = {'origin' : 'Naver', 'type':'text'}
        FCC = {'origin' : 'Kaggle', 'type':'image'}


    def getDataParser(self, testdata:DATA_NAME, service_type:SERVICE_TYPE) -> BaseDataParser:
        if testdata == self.DATA_NAME.AIHub and service_type == SERVICE_TYPE.STT:
            return AIHubParser(targetPath = cfg.get("data", "AIHub"))
        elif testdata == self.DATA_NAME.ClovaAI and service_type == SERVICE_TYPE.STT:
            return ClovaAIParser(targetPath = cfg.get("data", "ClovaAI"))
        elif testdata == self.DATA_NAME.FCC and service_type == SERVICE_TYPE.FD: 
            return FaceCountingParser(targetFile = cfg.get("data", "FCC"))
        else:
            logging.warning("[WARNINIG] {} data parser is not defined".format(testdata.name))
            raise "[WARNINIG] {} data parser is not defined".format(testdata.name)


class ServiceFactory():
    class PROVIDER(Enum):
        KT = "KT"
        Kakao = "Kakao"
        Google = "Google"


    def getAPICaller(self, service_provider:PROVIDER, service_type:SERVICE_TYPE, service_info:dict) -> BaseAPICaller:
        service_url:str = service_info['url']
        service_keys:list = service_info['keys']    # service_keys[순번][(키명, 키값)]

        ### KT_STT
        if service_provider == self.PROVIDER.KT and service_type == SERVICE_TYPE.STT:
            KT_keys = {}
            for k_name, k_value in service_keys:
                KT_keys[k_name] = k_value

            return KT_STT(url="", key=KT_keys)

        ### Kakao_STT
        elif service_provider == self.PROVIDER.Kakao and service_type == SERVICE_TYPE.STT:
            return Kakao_STT(url = service_url, key = service_keys[0][1])

        ### Kakao_FaceDetection
        elif service_provider == self.PROVIDER.Kakao and service_type == SERVICE_TYPE.FD:
            return Kakao_FaceDetect(url = service_url, key = service_keys[0][1])

        ### KT_FaceDetection
        elif service_provider == self.PROVIDER.KT and service_type == SERVICE_TYPE.FD:
            return KT_FaceDatect(url = service_url, options={'threshold':'0', 'fileName':'10001.jpg'})

        ### Google_FaceDetection (만료)
        # elif service_provider == self.PROVIDER.Google and service_type == SERVICE_TYPE.FD:
        #     return Google_FaceDetection(url = service_url, key = service_keys[0][1])
            
        else:
            logging.warning("[WARNINIG] {} API Caller is not defined or {} is not supperted".format(service_provider.name, service_type.name))
            raise "[WARNINIG] {} API Caller is not defined or {} is not supperted".format(service_provider.name, service_type.name)


class AnlalyzerFactory():

    def getAnalyzer(self, service_type:SERVICE_TYPE) -> BaseResultAnalyzer:
        if service_type == SERVICE_TYPE.STT:
            return STTResultAnalyzer()
        elif service_type == SERVICE_TYPE.FD:
            return FDResultAnalyzer()
        else:
            logging.warning("[WARNINIG] {} Analyzer is not defined".format(service_type.name))
            raise "[WARNINIG] {} Analyzer is not defined".format(service_type.name)

