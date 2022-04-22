import config.cfgParser as cfg
from modules.DataParser.Vision.FaceDetectParser import FaceCountingParser
from modules.APICaller.Vision.Kakao_FaceDetect import Kakao_FaceAPI
from modules.Controller.VisionTestController import FaceTestController
import logging
from datetime import datetime
import os

# logging
curTime = datetime.now().strftime('%Y%m%d_%H%M%S')
# logging.basicConfig(filename=f'{os.getcwd()}/logs/{curTime}.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

### main
ftc = FaceTestController()
# ftc.addAPICaller(Kakao_FaceAPI(url=cfg.get('kakao', 'url_face'), key=cfg.get('kakao', 'key_sdh')))
# ftc.addTestData(FaceCountingParser(targetFile="/Users/songdonghun/workspace/dataset/vision/Face Counting Challenge"))
# resultList = ftc.startRequest(limit=3, record=f"{os.getcwd()}/logs/{curTime}_result.txt")

list = ftc.startAnalysis(targetFile=f"{os.getcwd()}/logs/20220419_135936_result.txt", record=f'/Users/songdonghun/workspace/dataset/vision/Face Counting Challenge/analysis_result')
# print(*list, sep='\n\n')
# ftc.startAnalysis(resultList=resultList)

