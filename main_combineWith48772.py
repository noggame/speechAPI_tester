import json
from data.TestResult import TestResult

f_cmb = open('/mnt/d/Workspace/python/speechAPI_tester/logs/0_end/combinedResult.txt', 'r')
cmbDict:dict = {}

for line in f_cmb.readlines():
    tr = json.loads(line)

    if tr['service'] == 'Kakao_STT':
        cmbDict[tr['id']] = {}
        cmbDict[tr['id']]['source'] = tr['source']
        cmbDict[tr['id']]['expected'] = tr['expected']
        cmbDict[tr['id']]['actual'] = tr['actual']

f_cmb.close()

f = open('/mnt/d/Workspace/python/speechAPI_tester/sample/kt_stt_50000/reference-KT-48772-share.txt', 'r')
f_write = open('/mnt/d/Workspace/python/speechAPI_tester/logs/0_end/cmb_48772.txt', 'w')

for line in f.readlines():
    div = line.split('\t')
    filename = div[0][div[0].rindex('/')+1:]
    expected = div[1]
    actual = div[2].splitlines()[0]

    if cmbDict.get(filename[:-5]) != None: # cmbDict[filename[:-5]]:
        tr_kt = TestResult(id = filename, source = cmbDict[filename[:-5]]['source'], service = 'KT_STT', expected = [expected], actual = [actual])
        tr_kakao = TestResult(id = filename, source = cmbDict[filename[:-5]]['source'], service = 'Kakao_STT', expected = cmbDict[filename[:-5]]['expected'], actual = cmbDict[filename[:-5]]['actual'])

        f_write.write(str(tr_kt)+'\n')
        f_write.write(str(tr_kakao)+'\n')


f_write.close()


