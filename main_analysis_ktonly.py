import re
import os
from data.TestData import TestData
from data.ResultFlag import ResultFlag
import modules.compareSTT as cs
import copy


# user configuration
# target = 'result_test_KT_KAKAO.txt'
target = 'result_test_KT_ONLY_RESULT.txt'
# target = 'result_test_KT_KAKAO_ONLY_RESULT.txt'

# system variable
flag = ResultFlag()
cnt_skip = 0    # Num Of Skip
tdList = []
update_td = None

try:
    td = TestData()
    # f = open(f'{os.getcwd()}/data/{target}', 'r')
    f = open(f'{os.getcwd()}/logs/{target}', 'r')
    
    for el in f.readlines():
        print(el, end='')

        # START
        if el.find('.wav') > 0:
            # init.
            flag.init()

            # 매번 시작에 앞서 이전 TestData의 최종값 저장
            if update_td:
                tdList.append(update_td)
                update_td = None

            td = TestData()
            flag.SKIP = False

            # get data info.
            wav, expected, id = el.split('/')
            td.expected = expected.strip()
            td.id = id.strip()

            # except [alpha / digit]
            if re.findall('[a-zA-Z0-9]+', td.expected):
                flag.SKIP = True
                cnt_skip += 1
                update_td = None
                print(f'[SKIP] contains ALPHA or DIGIT. {td.expected} / {td.id}')
                continue

        # SKIP
        if flag.SKIP:
            continue

        # calc. acc.
        if el.startswith("[KT_STT]"):
            flag.KT = True
            stt_kt = re.sub('\[KT_STT\]', '', el).strip()

            if len(stt_kt) == 0:
                continue

            acc_kt = cs.calculateAccuracy_cmplib([td.expected], stt_kt)

            if acc_kt > td.acc_kt:
                td.acc_kt = acc_kt
                td.stt_kt = stt_kt
                update_td = td
                print(f'[UPDATE] ACC to {td.acc_kt}')


    if update_td:
        tdList.append(update_td)

    f.close()
except FileNotFoundError:
    print('file read err')


# total
print(f'\ntotal = {len(tdList)} (except skip : {cnt_skip})')


# statics.
sum_kt = {
    'reserve' : 0,
    'parking' : 0,
    'menu' : 0,
    'openhour' : 0,
    'etc' : 0
}

cnt = {
    'reserve' : 0,
    'parking' : 0,
    'menu' : 0,
    'openhour' : 0,
    'etc' : 0
}

for etd in tdList:
    if any(x in str(etd.expected) for x in ['예약']):
        cnt['reserve'] += 1
        sum_kt['reserve'] += float(etd.acc_kt)

    if any(x in str(etd.expected) for x in ['주차']):
        cnt['parking'] += 1
        sum_kt['parking'] += float(etd.acc_kt)

    if any(x in str(etd.expected) for x in ['메뉴']):
        cnt['menu'] += 1
        sum_kt['menu'] += float(etd.acc_kt)

    if any(x in str(etd.expected) for x in ['영업']):
        cnt['openhour'] += 1
        sum_kt['openhour'] += float(etd.acc_kt)

    if not any(x in str(etd.expected) for x in ['예약', '주차', '메뉴', '영업']):
        cnt['etc'] += 1
        sum_kt['etc'] += float(etd.acc_kt)

print("\n[KT_RESULT]")
print(f"예약 : {sum_kt['reserve']/cnt['reserve']} ({cnt['reserve']})")
print(f"주차 : {sum_kt['parking'] / cnt['parking']} ({cnt['parking']})")
print(f"메뉴 : {sum_kt['menu'] / cnt['menu']} ({cnt['menu']})")
print(f"영업 : {sum_kt['openhour'] / cnt['openhour']} ({cnt['openhour']})")
print(f"기타 : {sum_kt['etc'] / cnt['etc']} ({cnt['etc']})")


