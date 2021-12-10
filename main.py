# from kakaoSTT 
from kakaoSTT import kakaoAPI

sample = '/home/sdh/workspace/api_tester/sample/S00000013/0001.wav'

kapi = kakaoAPI()
kapi_result = kapi.requestSTT(sample)

print(kapi_result)


