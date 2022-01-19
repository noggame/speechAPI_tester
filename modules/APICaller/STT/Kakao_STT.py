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
                
                return ttsResultList
            except:
                logging.exception(f'[Exception] {__class__.__name__} - json, "finalResult" not found')
        elif response.status_code == 401:
            logging.exception(f'[Exception] {__class__.__name__} - un-registered ips. reponse = {response}')
            return None
        else:
            logging.exception(f'[Exception] {__class__.__name__} - not-expected exception occured. response = {response}')
            return None
            
        return response


