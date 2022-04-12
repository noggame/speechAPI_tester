import config.cfgParser as cfg
from modules.DataParser.Vision.FaceDetectParser import FaceCountingParser
from modules.APICaller.Vision.Kakao_FaceDetect import Kakao_FaceAPI
from modules.TestController import TestController
import logging
from datetime import datetime
import os

# logging
logging.basicConfig(filename=f'{os.getcwd()}/logs/{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

### main
tc = TestController()
tc.add_Vision_API(Kakao_FaceAPI(url=cfg.get('kakao', 'url_face'), key=cfg.get('kakao', 'key_sdh')))
tc.add_Vision_TestData(FaceCountingParser(targetFile="/Users/songdonghun/workspace/dataset/vision/Face Counting Challenge"))
tc.startVisionRequest(limit=1)

