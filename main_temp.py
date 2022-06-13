# -*- coding: utf-8 -*-

from itertools import zip_longest
from operator import itemgetter
import os
import json
import re
from tkinter import EXCEPTION

import config.cfgParser as cfg
import requests
from datetime import datetime
from data.TestData import TestData
from data.Vision.FaceInfo import Face
from modules.APICaller.Vision.Kakao_FaceDetect import Kakao_FaceAPI
from PIL import Image, ImageDraw
import csv
from data.Vision.Image import RectangleBox
import modules.Accuracy.STTAccuracyTool as sta
from modules.Controller.TestController import TestController, TestControllerWithDB
from modules.Controller.VisionTestController import FaceTestController
from modules.APICaller.Vision.KT_FaceDetect import KT_FaceAPI

import psycopg2
import data.TestVars as TV

from modules.Database.Controller import APIDatabaseController

import time

### DB init.
apidb = APIDatabaseController()
apidb.connect()

### TestController init.
tc = TestControllerWithDB()
# option = {}
option = {"limit":2}

st = time.time()
### Request API & DB
# testResultList = tc.testWith(data=TV.DATA.ClovaAI, api=TV.API.Kakao_STT, purpose=TV.PURPOSE.STT, option=option)   # ClovaAI - Kakao_STT
# testResultList = tc.testWith(data=TV.DATA.ClovaAI, api=TV.API.KT_STT, purpose=TV.PURPOSE.STT, option=option)      # ClovaAI - KT_STT
testResultList = tc.testWith(data=TV.DATA.AIHub, api=TV.API.Kakao_STT, purpose=TV.PURPOSE.STT, option=option)        # AIHub - Kakao_STT
# testResultList = tc.testWith(data=TV.DATA.AIHub, api=TV.API.KT_STT, purpose=TV.PURPOSE.STT, option=option)        # AIHub - KT_STT

### Statics



et = time.time()

print(et - st)

# for td in testResultList:
#     td:TestData = td
#     print(td)

# 2) 테스트 요청 (data_name, api_name, [개수], [옵션])
# 3) 테스트 결과 확인




# apidb.addDataset(source="/usr/src/mysrc", origin="AIHub", data_type="image", data_format="jpeg")
# testset_number = apidb.addTestset(source="/usr/src/mysrc", service_type="KT_STT", expected="first testset")
# apidb.addResult(source="/usr/src/mysrc", service_type="KT_STT", number=testset_number, actual="first result")
