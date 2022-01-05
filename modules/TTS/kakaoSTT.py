import requests
import json
import logging

def requestKakaoSTT(file_path, authorization=None):
    url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize'
    header = {
        'Content-Type': 'application/octet-stream',
        'Authorization': authorization if authorization else 'KakaoAK 697f04dd01214c2a532634d6df4d1126'
    }

    try:
        data = open(file_path, 'rb')
    except FileNotFoundError:
        logging.exception("File not found")
    
    response = requests.post(url = url, headers = header, data = data)

    if response.status_code == 200:
        try:
            result_data = response.text[response.text.index('{"type":"finalResult"'):response.text.rindex('}')+1]   # response 데이터 파싱 (type=finalResult인 json데이터의 value값)
            result_value = json.loads(result_data)['value']
            logging.info(f'[KAKAO_STT] {result_value}')
            return result_value
        except:
            logging.exception("fail parsing result")
        
    return response


# class kakaoAPI:
#     def __init__(self, url ='https://kakaoi-newtone-openapi.kakao.com/v1/recognize',
#                         authorization = 'KakaoAK 697f04dd01214c2a532634d6df4d1126',
#                         data = None) -> None:

#         self._url = url
#         self._header = {
#             'Content-Type': 'application/octet-stream',
#             'Authorization': authorization
#         }
#         self._data = data

#     @property
#     def url(self):
#         return self._url

#     @property
#     def data(self):
#         return self._data

#     @property
#     def header(self):
#         return self._header

#     @url.setter
#     def url(self, url):
#         self._url = url

#     @data.setter
#     def data(self, data):
#         self._data = data

#     @header.setter
#     def header(self, authorization):
#         self.header = {
#             'Content-Type': 'application/octet-stream',
#             'Authorization': authorization
#         }

#     def requestSTT(self, file):
#         try:
#             if file is None:
#                 file = self._data
#             data = open(file, 'rb')
#         except FileNotFoundError:
#             logging.exception("File not found")
        
#         response = requests.post(url = self.url, headers = self.header, data = data)
        
#         # logging.info(response.headers)
#         # logging.info(response.text)

#         if response.status_code == 200:
#             try:
#                 result_data = response.text[response.text.index('{"type":"finalResult"'):response.text.rindex('}')+1]   # response 데이터 파싱 (type=finalResult인 json데이터의 value값)
#                 result_value = json.loads(result_data)['value']
#                 logging.info(f'[KAKAO_STT] {result_value}')
#                 return result_value
#             except:
#                 logging.exception("fail parsing result")
            
#         return response

