import logging
import os
import config.cfgParser as cfg
from datetime import datetime
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT
from modules.Controller.VoiceTestController import STTTestController
from modules.DataParser.STT.ShinhanDataParser import ShinhanDataParser
import modules.Accuracy.STTAccuracyTool as sat
import json

# Analysis
from modules.Accuracy.AccuracyFilter import AccuracyFilter


### User Configuration
_baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_101404438_2011.raw_Callee"
# _baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_154036778_2010.raw_Callee"
# _baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_160954259_2108.raw_Callee"
# _baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_164634311_2002.raw_Callee"

_resultFileName = 'result_kakao.txt'

### System Configuration
logging.basicConfig(filename=f'{_baseDir}/logs/STT/log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
stt_tc = STTTestController()
stt_tc.addTestData(ShinhanDataParser(f'{_baseDir}'))
stt_tc.addAPICaller(KT_STT(options={'client_id': cfg.get('kt', 'cliend_id'), 'client_key': cfg.get('kt', 'client_key'), 'client_secret': cfg.get('kt', 'cliend_secret')}))
stt_tc.addAPICaller(Kakao_STT(url=cfg.get('kakao', 'url_stt'), key=cfg.get('kakao', 'key_kjh')))

### test
# API
sttResultList = stt_tc.startRequest(record=f'{_baseDir}/{_resultFileName}')    # 전체 데이터 테스트

# # Analysis
# analysisResultList = stt_tc.getStaticInfo(accuracyFilter=[AccuracyFilter.EXP_BASED, AccuracyFilter.WER],
#                                             categoryFilter=[],
#                                             sttResultData = None,
#                                             # targetFile = f'{_targetPath}/result_overall.txt',
#                                             targetFile = f'{_baseDir}/{_resultFileName}',
#                                             record = f'{_baseDir}/analysis_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')


### Combine-Analysis
# f = open(f'{_baseDir}/{_resultFileName}', 'r')
# expectedSentence = ''
# actualSentence = ''
# for line in f.readlines():
#     expectedSentence += json.loads(line)['expected'][0] + " "
#     actualSentence += json.loads(line)['actual'][0] + " "
### Acc
# exp, act, wer = sat.calculateWERAccuracyWithNomalize([expectedSentence], [actualSentence])
# print(wer)







######## Result
# 124 / 130
# 61.98801198801198

# 65 / 71
# 58.790276992651215

# 149 / 160
# 48.98550724637681

# 79 / 93
# 59.39933259176864
