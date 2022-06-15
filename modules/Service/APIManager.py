import config.cfgParser as cfg
from modules.Service.Type import SUPPORT
# from modules.Service.API.APICaller import APICaller
import modules.Service.API.BaseAPICaller as BaseAPICaller
from modules.Service.API.APICaller.STT.KT_STT import KT_STT
from modules.Service.API.APICaller.STT.Kakao_STT import Kakao_STT
from enum import Enum

class APIInfo():
    def __init__(self, name:str, caller:BaseAPICaller, support:SUPPORT) -> None:
        self.name = name
        self.caller = caller
        self.support = support


class ServiceProvider():
    def __init__(self, name:str) -> None:
        self.name = name
        self.apiList= []

    def addAPI(self, api:APIInfo):
        self.apiList.append(api)

    def findAPICaller(self, support:SUPPORT) -> APIInfo:
        for api in self.apiList:
            api:APIInfo = api
            if api.support == support:
                return api
        return None


class ServiceManager():
    def __init__(self) -> None:
        self.serviceProviderList = []

        # KT - STT
        KT = ServiceProvider("KT")
        KT.addAPI(APIInfo(
            name = "KT_STT",
            caller = KT_STT(url="", key={
                'client_id': cfg.get('kt', 'client_id'),
                'client_key': cfg.get('kt', 'client_key'),
                'client_secret': cfg.get('kt', 'client_secret')
            }),
            support = SUPPORT.STT
        ))
        self.serviceProviderList.append(KT)

        # Kakao - STT
        Kakao = ServiceProvider("Kakao")
        Kakao.addAPI(APIInfo(
            name = "Kakao_STT",
            caller = Kakao_STT(url=cfg.get('kakao', 'url_stt'),
                                key=cfg.get('kakao', 'key_sdh')),
            support = SUPPORT.STT
        ))
        self.serviceProviderList.append(Kakao)


    def findServiceProvider(self, service_provider_name:str):
        for sp in self.serviceProviderList:
            sp:ServiceProvider = sp
            if sp.name == service_provider_name:
                return sp
        return None


class REG_SERVICE(Enum):
    KT = "KT_STT"
    Kakao = "Kakao_STT"



