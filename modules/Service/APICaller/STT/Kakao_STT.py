from typing import List
from modules.Service.APICaller.BaseAPICaller import BaseAPICaller
import requests
import json
import logging
import modules.SoundConverter as SoundConverter


class Kakao_STT(BaseAPICaller):
    def __init__(self, url, key, targetFile=None, options=None):
        super().__init__(url, key, targetFile, options)

    def request(self, url=None, key=None, targetFile=None, options=None):
        _url = url if url else self.url
        _key = key if key else self.key
        _targetFile = targetFile if targetFile else self.targetFile
        # _options = options if options else self.options

        _header = {
            'Content-Type': 'application/octet-stream',
            'Authorization': _key
        }
        ttsResultList = []

        wav=open(_targetFile, 'rb')
            
        try:
            response = requests.post(url = _url, headers = _header, data = wav)
        except ConnectionError as ce:
            logging.error(f'[ERROR] Connection error :: {__class__.__name__} - {ce}')
        except Exception as e:
            logging.error(f'[ERROR] Unexpected error occured :: {__class__.__name__} - {e}')

        if response.status_code == 200:
            responseText = response.text
            finalIndex = responseText.find('{"type":"finalResult"')
            finalResult = self._getJsonDataFromIndex(responseText, finalIndex)

            if not finalResult or finalIndex == -1:
                # 정상응답 받았으나 실데이터가 없는 경우
                ttsResultList.append("")
                logging.warning("[WARNING] Response data is empty :: {} - {}".format(__class__.__name__, response.text))
            else:
                ttsResultList.append(f"\"{json.loads(finalResult)['value']}\"")

        elif response.status_code == 401:
            logging.error("[ERROR] Unauthorized, un-registered ip. :: {} - {}".format(__class__.__name__, response.text))
            return None
        else:
            logging.error("[ERROR] Unexpected response status :: {} - {}".format(__class__.__name__, response.text))
            return None
            
        return ttsResultList


    def _getJsonDataFromIndex(self, target:str, startIndex:int):
        numOfBracket = 0
        result = ''

        for c in target[startIndex:]:
            if c == '{':
                numOfBracket += 1
            elif c == '}':
                numOfBracket -= 1
            
            result += c
            if numOfBracket == 0:
                return result

        return 