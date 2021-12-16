
from aihubData import AIDataHub
from kakaoSTT import kakaoAPI
from compareSTT import CompareData
import os



##### get sample data list
aidata = AIDataHub(baseDir=str(os.getcwd()+"/sample"),
                    targetFile='0001.txt',
                    wavFile='0001.wav')

temp_cnt = 20                                      ################# tmp1
for txt, wav in aidata.getTargetList():
    print(txt + " - " + wav)

    # 기대결과
    expectedList = aidata.extractExpectedSentence(txt)
    
    # 실제결과
    k_api = kakaoAPI()
    k_sttResult = k_api.requestSTT(wav)
    # k_sttResult = '아이스 아메리카노 하나요'        ################# tmp1-1
    print(f"STT Result = {k_sttResult}", sep='\n')

    # 결과비교
    #2) 기대결과 리스트 중 실제결과와 가장 일치율이 높은 점수 반환
    bestScore = CompareData.compareWithKakaoSTT(expectedList, k_sttResult)
    # aa.compareWithKakaoSTT("b", "C")
    print(bestScore)

    # print(expectedList, sep="\n")

    temp_cnt -= 1               ################# tmp1
    if temp_cnt <= 0:           ################# tmp1
        break                   ################# tmp1
