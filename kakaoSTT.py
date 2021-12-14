import requests
import json
from aihubData import AIDataHub

class kakaoAPI:
    def __init__(self) -> None:
        self.url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize'
        self.header = {
                # 'Transfer-Encoding': 'chunked',
                'Content-Type': 'application/octet-stream',
                'Authorization': 'KakaoAK 697f04dd01214c2a532634d6df4d1126'
        }
        self.data = "/home/sdh/workspace/api_tester/sample/S00000001/0001.wav"

    def changeRequest(self, url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize',
                            header={
                                'Content-Type': 'application/octet-stream',
                                'Authorization': 'KakaoAK 697f04dd01214c2a532634d6df4d1126'
                            },
                            data='/home/sdh/workspace/api_tester/sample/S00000001/0001.wav'):
        self.url = url
        self.header = header
        self.data = data

    def requestSTT(self, file = '/home/sdh/workspace/api_tester/sample/S00000001/0001.wav'):
        data = open(file, 'rb')
        response = requests.post(url = self.url, headers = self.header, data = data)

        if response.status_code == 200:
            try:
                result_data = response.text[response.text.index('{"type":"finalResult"'):response.text.rindex('}')+1]   # response 데이터 파싱 (type=finalResult인 json데이터의 value값)
                result_value = json.loads(result_data)['value']
                return result_value
            except:
                print("fail parsing result")
            
        return response

