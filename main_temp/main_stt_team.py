import logging
import os
from modules.AIDataParser.ClovaAIParser import ClovaDataController
from datetime import datetime
import modules.similarity.STT.compareSTT as cs
import re


clovaCTL = ClovaDataController(baseDir=f'{os.getcwd()}/sample/clova_dataset', answer="train_ClovaCall.json")
logging.basicConfig(filename=f'{os.getcwd()}/logs/result_test_{datetime.now().strftime("%Y%d%m%H%M%S")}.log',
                            level=logging.INFO,
                            format='%(asctime)s %(message)s')

f_stt_team = open(f'{os.getcwd()}/sample/voiceteam/20220110.txt', 'r')
dic_sr = {}

for std in f_stt_team.readlines():
    last = std.split('/')
    last = last[len(last)-1]

    wav = last[:26]
    stt_result = last[27:].strip()
    dic_sr[wav] = stt_result

numOfSample = 0
numOfAvSample = 1
flag_classify = {
    'NA'   : False,
    '예약' : False,
    '주차' : False,
    '메뉴' : False,
    '영업' : False,
    'NC'   : False
}
cnt_classify = {
    'NA'   : 0,
    '예약' : 0,
    '주차' : 0,
    '메뉴' : 0,
    '영업' : 0,
    'NC'   : 0
}
acc_sum = {
    'total': 0,
    '예약' : 0,
    '주차' : 0,
    '메뉴' : 0,
    '영업' : 0,
    'NC'   : 0
}

# acc_sum = 0

for dataset in clovaCTL.getExpectedList():
    wav, expected, speaker_id = dataset['wav'], dataset['text'], dataset['speaker_id']
    numOfSample += 1
    result_str = ''
    result_str += f'{numOfAvSample} / {wav} / {expected}'


    if wav not in dic_sr:
        continue


    print(numOfSample)
    expected = combSentence = re.sub("[n/\.\?]*", '', expected)

    acc_kt = cs.calculateAccuracy_exp([expected], dic_sr[wav])
    result_str += f' / {dic_sr[wav]} / acc: {acc_kt}%'

    acc_sum['total'] += acc_kt
    # cs.calculateAccuracy_actual([td.expected], td.stt_kt)
    # cs.calculateCMPlib([td.expected], td.stt_kt)

    if re.findall('[a-zA-Z0-9]+', expected):
        flag_classify['NA'] = True
        cnt_classify['NA'] += 1
    else:
        numOfAvSample += 1
        if any(x in str(expected) for x in ['예약']):
            flag_classify['예약'] = True
            cnt_classify['예약'] += 1
            acc_sum['예약'] += acc_kt

        if any(x in str(expected) for x in ['주차']):
            flag_classify['주차'] = True
            cnt_classify['주차'] += 1
            acc_sum['주차'] += acc_kt

        if any(x in str(expected) for x in ['메뉴']):
            flag_classify['메뉴'] = True
            cnt_classify['메뉴'] += 1
            acc_sum['메뉴'] += acc_kt

        if any(x in str(expected) for x in ['영업']):
            flag_classify['영업'] = True
            cnt_classify['영업'] += 1
            acc_sum['영업'] += acc_kt

        if not any(x in str(expected) for x in ['예약', '주차', '메뉴', '영업']):
            flag_classify['NC'] = True
            cnt_classify['NC'] += 1
            acc_sum['NC'] += acc_kt

    for fc in flag_classify:
        if flag_classify[fc]:
            result_str += f' / [{fc}]'
            if fc == 'NA':
                break

    print(result_str)

    # init.
    flag_classify = {
        'NA' : False,
        '예약' : False,
        '주차' : False,
        '메뉴' : False,
        '영업' : False,
        'NC' : False
    }

print(f'\n[Test Dataset 총계] = {numOfAvSample-1}')
sum_classified = cnt_classify["예약"] + cnt_classify["주차"] + cnt_classify["메뉴"] + cnt_classify["영업"] + cnt_classify["NC"]
avg = {
    'total': round(acc_sum["total"]/numOfAvSample, 2),
    '예약': round(acc_sum["예약"]/cnt_classify["예약"], 2),
    '주차': round(acc_sum["주차"]/cnt_classify["주차"], 2),
    '메뉴': round(acc_sum["메뉴"]/cnt_classify["메뉴"], 2),
    '영업': round(acc_sum["영업"]/cnt_classify["영업"], 2),
    'NC': round(acc_sum["NC"]/cnt_classify["NC"], 2)
}
print(f'[예약] = {cnt_classify["예약"]} ({avg["예약"]} %)')
print(f'[주차] = {cnt_classify["주차"]} ({avg["주차"]} %)')
print(f'[메뉴] = {cnt_classify["메뉴"]} ({avg["메뉴"]} %)')
print(f'[영업] = {cnt_classify["영업"]} ({avg["영업"]} %)')
print(f'[NotClassified] = {cnt_classify["NC"]} ({avg["NC"]} %) (분류되지 않음)')
print(f'[NotAvailable] = {cnt_classify["NA"]} (숫자, 영문자 제외)')
# avg_acc = round(acc_sum/numOfAvSample, 2)
# print(f'[AVG] = {round(acc_sum/numOfAvSample, 2)} %')
print(f'[AVG] = {avg["total"]} %')