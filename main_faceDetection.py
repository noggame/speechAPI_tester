import config.cfgParser as cfg
from modules.APICaller.Vision.KT_FaceDetect import KT_FaceAPI
from modules.DataParser.Vision.FaceDetectParser import FaceCountingParser
from modules.APICaller.Vision.Kakao_FaceDetect import Kakao_FaceAPI
from modules.Controller.VisionTestController import FaceTestController
import logging
from datetime import datetime
import os

# logging
curTime = datetime.now().strftime('%Y%m%d_%H%M%S')
# logging.basicConfig(filename=f'{os.getcwd()}/logs/Vision/{curTime}.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

### main
ftc = FaceTestController()
ftc.addAPICaller(Kakao_FaceAPI(url=cfg.get('kakao', 'url_face'), key=cfg.get('kakao', 'key_sdh')))      # TODO: Threshold 값에 따라 얼굴 인식으로 처리
ftc.addAPICaller(KT_FaceAPI(url=cfg.get('kt', 'url_face'), options={"threshold":0.5}))
ftc.addTestData(FaceCountingParser(targetFile="/Users/songdonghun/dataset/vision/Face Counting Challenge"))
resultList = ftc.startRequest(limit=5, record=f"{os.getcwd()}/logs/Vision/{curTime}_result.txt")

testResult = ftc.startAnalysis(targetFile=f"{os.getcwd()}/logs/Vision/{curTime}_result.txt", record=f'/Users/songdonghun/dataset/vision/Face Counting Challenge/analysis_result')
print(testResult)
# print(*list, sep='\n\n')

