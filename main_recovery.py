import json
import copy
from modules.APICaller.STT.KT_STT import KT_STT
from modules.APICaller.STT.Kakao_STT import Kakao_STT

ktapi = KT_STT(options={
    'client_id':'3fd7261c-7d08-487b-a104-b867919e497b',
    'client_key':'d8613f5b-43f1-5a11-b183-35261da543a6',
    'client_secret':'693bc75a1bf4f80d2636372c02b64d0c5a636757e1b9ae6ddfd5c209f9d32892'
})
kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize', key='KakaoAK a6d5effd95f8bfa5c5b31c982015dfd4') # SDH

targetFile = "14.txt"
recoveredFile = "r"+targetFile

f = open(f'/mnt/d/Workspace/python/speechAPI_tester/logs/0_end/{targetFile}', 'r')
rf = open(f'/mnt/d/Workspace/python/speechAPI_tester/logs/0_end/{recoveredFile}', 'w')

prevInfo = {}
id_cnt = 0
serviceList = ['KT_STT', 'Kakao_STT']

for st in f.readlines():
    idx = id_cnt%len(serviceList)

    targetInfo:dict = json.loads(st)
    service = targetInfo.get("service")

    if prevInfo.get('id') == targetInfo.get('id'):    # 동일 데이터에 대한 타 API 호출
        
        # Exception (API 호출 누락)
        if service != serviceList[idx]:     

            print(f'[{serviceList[idx]} 누락] {targetInfo}')

            wavFile = targetInfo.get("source")
            mp3File = wavFile[:-3]+'mp3'
            exp = ""

            # Static Process - 서비스 추가시 추가구현 필요
            if serviceList[idx] == 'KT_STT':
                exp = ktapi.request(targetFile=mp3File)
            elif serviceList[idx] == 'Kakao_STT':
                exp = kakaoapi.request(targetFile=wavFile)

            # update TestResult data
            targetInfo['service'] = serviceList[idx]
            targetInfo['actual'] = exp

            print(f"[Recovering] {targetInfo}\n")

            rf.write(str(targetInfo).replace("\'","\"")+"\n")
            id_cnt += 1

        prevInfo:dict = json.loads(st)
        rf.write(st)
        id_cnt += 1
        
    else:                                               # 신규 데이터 테스트
        if prevInfo and id_cnt < len(serviceList):      # 이전 데이터에 대해 모든 api로 테스트가 진행되었는지 확인

            # prevInfo 정보 기반으로 serviceList[id_cnt] api 호출해 값을 갱신하여 누락된 정보를 채울 수 있다.
            # 다만, api 개수가 2개 이상 누락된 경우에는 id_cnt 부터 len(serviceList) 이하의 모든 api 순번에 대해 누락된 정보를 채워야함
            # >> 추후 dynamic하게 동작이 필요한 경우 구현
            print(f'[교차오류] {st}')                                   # Exception
            break
        else:
            idx = 0
            id_cnt = 0

            # Exception (첫 번째 API 호출 누락 > 두 번째 이상의 API 호출은 정상이었다는 가정하에 Recovery 진행)
            if service != serviceList[0]:

                print(f'[{serviceList[0]} 누락] {targetInfo}')

                wavFile = targetInfo.get("source")
                mp3File = wavFile[:-3]+'mp3'
                exp = ""

                # Static Process - 서비스 추가시 추가구현 필요
                if serviceList[0] == 'KT_STT':
                    exp = ktapi.request(targetFile=mp3File)
                elif serviceList[0] == 'Kakao_STT':
                    exp = kakaoapi.request(targetFile=wavFile)

                # update TestResult data
                targetInfo['service'] = serviceList[0]
                targetInfo['actual'] = exp

                print(f"[Recovering] {targetInfo}\n")

                rf.write(str(targetInfo).replace("\'","\"")+"\n")
                id_cnt += 1

            prevInfo:dict = json.loads(st)
            rf.write(st)
            id_cnt+=1

    

