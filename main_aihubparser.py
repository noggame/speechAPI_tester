from modules.AIDataParser.AIHubParser import AIHubParser
from modules.AIDataParser.ClovaAIParser import ClovaAIParser
import logging
import os
from datetime import datetime
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT

from modules.TestController import TestController

logging.basicConfig(filename=f'{os.getcwd()}/logs/result_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

# TestData
aihp = AIHubParser(f'{os.getcwd()}/sample/sample_100')
clvp = ClovaAIParser(f'{os.getcwd()}/sample/clova_dataset')

# KT API
ktapi = KT_STT(options={
    'client_id':'3fd7261c-7d08-487b-a104-b867919e497b',
    'client_key':'d8613f5b-43f1-5a11-b183-35261da543a6',
    'client_secret':'693bc75a1bf4f80d2636372c02b64d0c5a636757e1b9ae6ddfd5c209f9d32892'
})

# KAKAO API
kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize',
                    key='KakaoAK 697f04dd01214c2a532634d6df4d1126')

### Test TestController
tc = TestController()
tc.addTestData(aihp)
tc.addTestData(clvp)
tc.addAPICaller(ktapi)
tc.addAPICaller(kakaoapi)

tc.start(limit=1)
