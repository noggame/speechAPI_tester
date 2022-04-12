import logging
import os
import config.cfgParser as cfg
from datetime import datetime
from modules.APICaller.STT.Kakao_STT import Kakao_STT
from modules.TestController import TestController
from modules.DataParser.STT.ShinhanDataParser import ShinhanDataParser
import modules.Accuracy.STTAccuracyTool as sat
import json

# Analysis
from modules.Accuracy.AccuracyFilter import AccuracyFilter


### User Configuration
_baseDir = f'{os.getcwd()}/sample/shinhan/split/1_20220111_164634311_2002.raw_Callee'
_resultFileName = 'result_kakao.txt'

### System Configuration
logging.basicConfig(filename=f'{_baseDir}/log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
tc = TestController()
tc.add_STT_TestData(ShinhanDataParser(f'{_baseDir}'))
tc.add_STT_API(Kakao_STT(url=cfg.get('kakao', 'url_stt'), key=cfg.get('kakao', 'key_kjh')))


### test
# API
# sttResultList = tc.startSTTRequest(record=f'{_baseDir}/{_resultFileName}')    # 전체 데이터 테스트

# # Analysis
# analysisResultList = tc.getStaticInfo(accuracyFilter=[AccuracyFilter.EXP_BASED, AccuracyFilter.WER],
#                                             categoryFilter=[],
#                                             sttResultData = None,
#                                             # targetFile = f'{_targetPath}/result_overall.txt',
#                                             targetFile = f'{_baseDir}/{_resultFileName}',
#                                             record = f'{_baseDir}/analysis_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')


# Combine-Analysis
f = open(f'{_baseDir}/{_resultFileName}', 'r')
expectedSentence = ''
actualSentence = ''
for line in f.readlines():
    expectedSentence += json.loads(line)['expected'][0] + " "
    actualSentence += json.loads(line)['actual'][0] + " "
### Acc
exp, act, wer = sat.calculateWERAccuracyWithNomalize([expectedSentence], [actualSentence])
print(wer)







######## Result
# 124 / 130
# 61.98801198801198

# 65 / 71
# 58.790276992651215

# 149 / 160
# 48.98550724637681

# 79 / 93
# 59.39933259176864
