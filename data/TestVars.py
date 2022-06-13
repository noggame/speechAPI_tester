from enum import Enum
import config.cfgParser as cfg
from modules.DataParser.STT.AIHubParser import AIHubParser
from modules.DataParser.STT.ClovaAIParser import ClovaAIParser
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT

### DATA
DATA_PARSER = {
    "AIHub": AIHubParser,
    "ClovaAI": ClovaAIParser
}

class DATA(Enum):
    AIHub = cfg.get("data", "AIHub")
    ClovaAI = cfg.get("data", "ClovaAI")

    def ORIGIN(name):
        origin = {
            'Naver': ['ClovaAI'],
            'ETRI': ['AIHub']
        }

        for key in origin:
            if name in origin[key]:
                return key

        return ""


### API Info.
API_CALLER = {
    "Kakao_STT": Kakao_STT,
    "KT_STT": KT_STT
}

class API(Enum):
    Kakao_STT = {
        'url': cfg.get('kakao', 'url_stt'),
        'key': cfg.get('kakao', 'key_sdh')
    }
    KT_STT = {
        'url': "",
        'key': {
            'client_id': cfg.get('kt', 'client_id'),
            'client_key': cfg.get('kt', 'client_key'),
            'client_secret': cfg.get('kt', 'client_secret')
        }
    }


### Purpose Info.
class PURPOSE(Enum):
    STT = "STT"
    FACE_DETECTION = "FD"