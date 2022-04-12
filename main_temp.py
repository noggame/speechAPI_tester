from operator import itemgetter
import os
import json
import re
from shutil import copyfile

import config.cfgParser as cfg
import requests
from datetime import datetime
from data.Vision.FaceInfo import Face
from modules.APICaller.Vision.Kakao_FaceDetect import Kakao_FaceAPI
from modules.TestController import TestController
from PIL import Image, ImageDraw
import csv


kapi = Kakao_FaceAPI(url=cfg.get('kakao', 'url_face'), key=cfg.get('kakao', 'key_sdh'))
target_src = "/Users/songdonghun/workspace/dataset/vision/Face Counting Challenge/image_data/10071.jpg"
faceList = kapi.request(targetFile=target_src)

# init.
img = Image.open(target_src)
_width, _height = img.size
draw = ImageDraw.Draw(img)

# get rectangle data & draw
# for x, y, width, height, gender in target.actual:
for face in faceList:
    face:Face = face
    abs_x = _width * face.x
    abs_y = _height * face.y
    abs_width = _width * face.width
    abs_height = _height * face.height
    print(face)
    draw.rectangle(xy=[(abs_x, abs_y), (int(abs_x+abs_width), int(abs_y+abs_height))], outline="#00FF00")
    # print(abs_width, abs_height, abs_x, abs_y)

# save
idxOfExt = str(target_src).rindex('.')
img.save(target_src[:idxOfExt] + "_rec" + target_src[idxOfExt:])
img.close()

print(faceList)
# 10070





####### save selected_file
# answerFile = open('/Users/songdonghun/workspace/dataset/vision/Face Counting Challenge/train.csv', 'r')
# csvData = csv.reader(answerFile)

# next(csvData)  # pass header

# # get data
# for name, num in csvData:
#     id = name
#     target_img = f'/Users/songdonghun/workspace/dataset/vision/Face Counting Challenge/image_data/{name}'
#     copy_path = f'/Users/songdonghun/workspace/dataset/vision/Face Counting Challenge/train_data/{name}'

#     copyfile(target_img, copy_path)

# answerFile.close()