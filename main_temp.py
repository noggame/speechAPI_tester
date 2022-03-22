import os
import json
import re

_baseDir = f'{os.getcwd()}/sample/shinhan/split/1_20220111_101404438_2011.raw_Callee'
# _baseDir = f'{os.getcwd()}/sample/shinhan/split/1_20220111_154036778_2010.raw_Callee'
# _baseDir = f'{os.getcwd()}/sample/shinhan/split/1_20220111_160954259_2108.raw_Callee'
# _baseDir = f'{os.getcwd()}/sample/shinhan/split/1_20220111_164634311_2002.raw_Callee'
_resultFileName = 'result_kakao.txt'

f = open(f'{_baseDir}/{_resultFileName}')

expectedSentence = ''
actualSentence = ''

for line in f.readlines():
    lj = json.loads(line)
    exp = lj['expected'][0]
    act = lj['actual'][0]

    if re.findall('[a-zA-Z0-9]+', act):
        print(exp, act)
    