import logging
import os
import config.cfgParser as cfg
from datetime import datetime
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT
from trash.VoiceTestController import STTTestController
from modules.DataParser.STT.ShinhanDataParser import ShinhanDataParser
import modules.Accuracy.STTAccuracyTool as sat
import json

# Analysis
from modules.Accuracy.AccuracyFilter import AccuracyFilter


### User Configuration
# _baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_101404438_2011.raw_Callee"
# _baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_154036778_2010.raw_Callee"
# _baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_160954259_2108.raw_Callee"
_baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_164634311_2002.raw_Callee"
# _baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/result_yes/union"

_baseDirSplt = _baseDir.split("/")
# _resultFileName = f'result_kakao_{_baseDirSplt[len(_baseDirSplt)-1]}.txt'
_resultFileName = f"/Users/songdonghun/dataset/STT/shinhan/0422_yes/result_yes/union_yes_yeng/result_kakao_{_baseDirSplt[len(_baseDirSplt)-1]}.txt"

### System Configuration
# logging.basicConfig(filename=f'{os.getcwd()}/logs/STT/log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
# stt_tc = STTTestController()
# stt_tc.addTestData(ShinhanDataParser(f'{_baseDir}'))
# # stt_tc.addAPICaller(KT_STT(options={'client_id': cfg.get('kt', 'cliend_id'), 'client_key': cfg.get('kt', 'client_key'), 'client_secret': cfg.get('kt', 'cliend_secret')}))    # KT
# stt_tc.addAPICaller(Kakao_STT(url=cfg.get('kakao', 'url_stt'), key=cfg.get('kakao', 'key_sdh')))    # Kakao

### test
# sttResultList = stt_tc.startRequest(record=f'{_baseDir}/{_resultFileName}')    # 전체 데이터 테스트

# # Analysis
# analysisResultList = stt_tc.getStaticInfo(accuracyFilter=[AccuracyFilter.EXP_BASED, AccuracyFilter.WER],
#                                             categoryFilter=[],
#                                             sttResultData = None,
#                                             # targetFile = f'{_targetPath}/result_overall.txt',
#                                             targetFile = f'{_baseDir}/{_resultFileName}',
#                                             record = f'{_baseDir}/analysis_stt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')


### Combine-Analysis
# f = open(f'{_baseDir}/{_resultFileName}', 'r')
f = open(f'{_resultFileName}', 'r')
expectedSentence = ''
actualSentence = ''
for line in f.readlines():
    result = json.loads(line)
    expectedSentence += result['expected'][0] + " "
    actualSentence += result['actual'][0] + " "
### Acc
exp, act, wer = sat.calculateWERAccuracyWithNomalize([expectedSentence], [actualSentence])
print(exp+"\n")
print(act)
print(wer)

