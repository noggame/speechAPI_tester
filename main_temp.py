from operator import itemgetter
import os
import json
import re

from cv2 import sort
from torch import div
import config.cfgParser as cfg
import requests
from datetime import datetime
from data.Vision.FaceInfo import Face
from modules.APICaller.Vision.Kakao_FaceDetect import Kakao_FaceAPI


target_file = "/Users/songdonghun/document/research/Vision/people_01.jpeg"
ka = Kakao_FaceAPI(url=cfg.get('kakao', 'url_face'), key=cfg.get('kakao', 'key_sdh'))
data = ka.request(targetFile=target_file)

print(*data, sep='\n')

# /Users/songdonghun/workspace/dataset/vision/Face Counting Challenge