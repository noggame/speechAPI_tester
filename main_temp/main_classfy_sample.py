import os
from modules.datactl.clovaData import ClovaDataController
import re

# fw = open(f'{os.getcwd()}/logs/result_classfy.log', 'w')

clovaCTL = ClovaDataController(baseDir=f'{os.getcwd()}/sample/clova_dataset', answer="train_ClovaCall.json")
# logging.basicConfig(filename=f'{os.getcwd()}/logs/result_test_{datetime.now().strftime("%Y%d%m%H%M%S")}.log',
#                     level=logging.INFO,
#                     format='%(asctime)s %(message)s')

matchingScore = {}
numOfSample = 0
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

for dataset in clovaCTL.getExpectedList():
    wav, text, speaker_id = dataset['wav'], dataset['text'], dataset['speaker_id']
    numOfSample += 1
    result_classify = f'{numOfSample} / {wav} / {text} /'

    ### classify
    # except [alpha / digit]
    if re.findall('[a-zA-Z0-9]+', text):
        flag_classify['NA'] = True
        cnt_classify['NA'] += 1
    else:
        if any(x in str(text) for x in ['예약']):
            flag_classify['예약'] = True
            cnt_classify['예약'] += 1

        if any(x in str(text) for x in ['주차']):
            flag_classify['주차'] = True
            cnt_classify['주차'] += 1

        if any(x in str(text) for x in ['메뉴']):
            flag_classify['메뉴'] = True
            cnt_classify['메뉴'] += 1

        if any(x in str(text) for x in ['영업']):
            flag_classify['영업'] = True
            cnt_classify['영업'] += 1

        if not any(x in str(text) for x in ['예약', '주차', '메뉴', '영업']):
            flag_classify['NC'] = True
            cnt_classify['NC'] += 1

    for fc in flag_classify:
        if flag_classify[fc]:
            result_classify += f' [{fc}]'
            if fc == 'NA':
                break

    print(result_classify)
    # fw.write(result_classfy)

    # init.
    flag_classify = {
        'NA' : False,
        '예약' : False,
        '주차' : False,
        '메뉴' : False,
        '영업' : False,
        'NC' : False
    }
    

print(f'\n[Test Dataset 총계] = {numOfSample}')
sum_classified = cnt_classify["예약"] + cnt_classify["주차"] + cnt_classify["메뉴"] + cnt_classify["영업"] + cnt_classify["NC"]
print(f'[예약] = {cnt_classify["예약"]}')
print(f'[주차] = {cnt_classify["주차"]}')
print(f'[메뉴] = {cnt_classify["메뉴"]}')
print(f'[영업] = {cnt_classify["영업"]}')
print(f'[NotClassified] = {cnt_classify["NC"]} (분류되지 않음)')
print(f'[NotAvailable] = {cnt_classify["NA"]} (숫자, 영문자 제외)')