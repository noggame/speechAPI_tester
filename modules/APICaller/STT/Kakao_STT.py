from typing import List
from modules.APICaller.APICaller import APICaller
import requests
import json
import logging

class Kakao_STT(APICaller):
    def __init__(self, url=None, key=None, targetFile=None, options=None) -> None:
        super().__init__(url, key, targetFile, options)

    def request(self, url=None, key=None, targetFile=None, options=None) -> List:
        _url = url if url else self.url
        _key = key if key else self.key
        _targetFile = targetFile if targetFile else self.targetFile
        # _options = options if options else self.options

        _header = {
            'Content-Type': 'application/octet-stream',
            'Authorization': _key
        }

        try:
            wav = open(_targetFile, 'rb')
        except FileNotFoundError:
            logging.exception("File not found")
            
        try:
            response = requests.post(url = _url, headers = _header, data = wav)
        except ConnectionError as ce:
            logging.exception(f'[Exception] {__class__.__name__} - {ce}')

        if response.status_code == 200:
            try:
                ttsResultList = []
                result_data = response.text[response.text.index('{"type":"finalResult"'):response.text.rindex('}')+1]   # response 데이터 파싱 (type=finalResult인 json데이터의 value값)
                ttsResultList.append(json.loads(result_data)['value'])
                logging.info(f'[KAKAO_STT] {ttsResultList}')
                return ttsResultList
            except:
                logging.exception(f'[Exception] {__class__.__name__} - json, "finalResult" not found')
            
        return response


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

