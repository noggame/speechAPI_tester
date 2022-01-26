import os


try:
    f = open(f'{os.getcwd()}/logs/result_test_KT.txt', 'r')
    fw = open(f'{os.getcwd()}/logs/result_test_KT_ONLY_RESULT.txt', 'w')
    for line in f.readlines():
        if any(x in line for x in ['[EXP]', '[KT_STT]', '[KAKAO_STT]','.wav']):
            fw.write(line)

except FileNotFoundError:
    print("[ERR] file not found")

