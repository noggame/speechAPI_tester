import re
import os
from data.TestData import TestData
from data.ResultFlag import ResultFlag
import modules.compareSTT as cs


# user configuration
# target = 'result_test_KT_KAKAO.txt'
target = 'result_test_KT_ONLY_RESULT.txt'
# target = 'result_test_KT_KAKAO_ONLY_RESULT.txt'

# system variable
flag = ResultFlag()
cnt_skip = 0    # Num Of Skip
tdList = []

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
                print(f'[SKIP] contains ALPHA or DIGIT. {td.expected} / {td.id}')
                continue

        # SKIP
        if flag.SKIP:
            continue

        # calc. acc.
        if el.find('KT_STT') > 0:
            flag.KT = True
            td.stt_kt = re.sub('\[KT_STT\]', '', el).strip()
            if len(td.stt_kt) == 0:
                flag.SKIP = True
                cnt_skip += 1
                print(f'[SKIP] KT_STT data is None. {td.expected} / {td.id}')
                continue

        elif el.find('KAKAO_STT') > 0:
            flag.KAKAO = True
            td.stt_kakao = re.sub('\[KAKAO_STT\]', '', el).strip()

            # [EXCEPTION] KT_STT not exist
            if flag.KT == False:
                flag.SKIP = True
                cnt_skip += 1
                print(f'[SKIP] not found ACC_INFO. {td.expected} / {td.id}')
                continue
        
        if flag.KT and not flag.KAKAO:
            td.acc_kt = cs.calculateAccuracy_exp([td.expected], td.stt_kt)
            # td.acc_kt = cs.calculateAccuracy_actual([td.expected], td.stt_kt)
            # td.acc_kt = cs.calculateCMPlib([td.expected], td.stt_kt)
        elif flag.KT and flag.KAKAO:
            td.acc_kakao = cs.calculateAccuracy_exp([td.expected], td.stt_kakao)
            # td.acc_kakao = cs.calculateAccuracy_actual([td.expected], td.stt_kakao)
            # td.acc_kakao = cs.calculateCMPlib([td.expected], td.stt_kakao)

        # END
        if flag.KT and flag.KAKAO:
            if td.acc_kt > td.acc_kakao:
                td.winner = 'KT'
            elif td.acc_kt < td.acc_kakao:
                td.winner = "KAKAO"
            else:
                td.winner = "DRAW"

            tdList.append(td)

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
sum_kakao = {
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
cnt_winner = {
    'reserve' : {'KT':0, 'KAKAO':0, 'DRAW':0},
    'parking' : {'KT':0, 'KAKAO':0, 'DRAW':0},
    'menu' : {'KT':0, 'KAKAO':0, 'DRAW':0},
    'openhour' : {'KT':0, 'KAKAO':0, 'DRAW':0},
    'etc' : {'KT':0, 'KAKAO':0, 'DRAW':0}
}

for td in tdList:
    # id = td.id
    # expected = td.expected
    # stt_kt = td.stt_kt
    # stt_kakao = td.stt_kakao
    # acc_kt = td.acc_kt
    # acc_kakao = td.acc_kakao
    # print(f'{id}{expected}{stt_kt}{stt_kakao}{acc_kt}{acc_kakao}')

    if any(x in str(td.expected) for x in ['예약']):
        cnt['reserve'] += 1
        cnt_winner['reserve'][td.winner] += 1
        sum_kt['reserve'] += float(td.acc_kt)
        sum_kakao['reserve'] += float(td.acc_kakao)

    if any(x in str(td.expected) for x in ['주차']):
        cnt['parking'] += 1
        cnt_winner['parking'][td.winner] += 1
        sum_kt['parking'] += float(td.acc_kt)
        sum_kakao['parking'] += float(td.acc_kakao)

    if any(x in str(td.expected) for x in ['메뉴']):
        cnt['menu'] += 1
        cnt_winner['menu'][td.winner] += 1
        sum_kt['menu'] += float(td.acc_kt)
        sum_kakao['menu'] += float(td.acc_kakao)

    if any(x in str(td.expected) for x in ['영업']):
        cnt['openhour'] += 1
        cnt_winner['openhour'][td.winner] += 1
        sum_kt['openhour'] += float(td.acc_kt)
        sum_kakao['openhour'] += float(td.acc_kakao)

    if not any(x in str(td.expected) for x in ['예약', '주차', '메뉴', '영업']):
        cnt['etc'] += 1
        cnt_winner['etc'][td.winner] += 1
        sum_kt['etc'] += float(td.acc_kt)
        sum_kakao['etc'] += float(td.acc_kakao)

print("\n[KT_RESULT]")
print(f"예약 : {sum_kt['reserve']/cnt['reserve']} ({cnt['reserve']})")
print(f"주차 : {sum_kt['parking'] / cnt['parking']} ({cnt['parking']})")
print(f"메뉴 : {sum_kt['menu'] / cnt['menu']} ({cnt['menu']})")
print(f"영업 : {sum_kt['openhour'] / cnt['openhour']} ({cnt['openhour']})")
print(f"기타 : {sum_kt['etc'] / cnt['etc']} ({cnt['etc']})")

print("\n[KAKAO_RESULT]")
print(f"예약 : {sum_kakao['reserve']/cnt['reserve']} ({cnt['reserve']})")
print(f"주차 : {sum_kakao['parking'] / cnt['parking']} ({cnt['parking']})")
print(f"메뉴 : {sum_kakao['menu'] / cnt['menu']} ({cnt['menu']})")
print(f"영업 : {sum_kakao['openhour'] / cnt['openhour']} ({cnt['openhour']})")
print(f"기타 : {sum_kakao['etc'] / cnt['etc']} ({cnt['etc']})")

print("\n[WINNER] - (KT / KAKAO / DRAW)")
print(f"예약 : {cnt_winner['reserve']['KT']} / {cnt_winner['reserve']['KAKAO']} / {cnt_winner['reserve']['DRAW']}")
print(f"주차 : {cnt_winner['parking']['KT']} / {cnt_winner['parking']['KAKAO']} / {cnt_winner['parking']['DRAW']}")
print(f"메뉴 : {cnt_winner['menu']['KT']} / {cnt_winner['menu']['KAKAO']} / {cnt_winner['menu']['DRAW']}")
print(f"영업 : {cnt_winner['openhour']['KT']} / {cnt_winner['openhour']['KAKAO']} / {cnt_winner['openhour']['DRAW']}")
print(f"기타 : {cnt_winner['etc']['KT']} / {cnt_winner['etc']['KAKAO']} / {cnt_winner['etc']['DRAW']}")

