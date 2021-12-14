# from kakaoSTT 
from kakaoSTT import kakaoAPI
from aihubData import AIDataHub
import os

sample = '안녕하세요 (만나서)/(처음 뵈었지만) 반갑습니다. 오늘은 (날씨가)/(기분이)/(공기가) (매우)/(정말) 좋습니다'

##### get sample data list
aidata = AIDataHub(baseDir=str(os.getcwd()+"/sample"),
                    targetFile='0001.txt',
                    wavFile='0001.wav')

for txt, wav in aidata.getTargetList():
    print(txt + " - " + wav)
    aidata.extractExpectedSentence(txt)


# print(*aidata.splitSentence(sample), sep="\n")
# print(*aidata.getExpectedResultList(sample), sep="\n")





# kapi = kakaoAPI()
# kapi_result = kapi.requestSTT(sample)
# print(kapi_result)

# print(aidata.getTargetList())
