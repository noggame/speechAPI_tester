from typing import List
from modules.APICaller.APICaller import APICaller
import requests
import json
import logging
import modules.SoundConverter as SoundConverter


class Kakao_OCR(APICaller):
    def __init__(self, url=None, key=None, targetFile=None, options=None) -> None:
        super().__init__(url, key, targetFile, options)

    def _getJsonDataFromIndex(self, target:str, startIndex:int):
        pass
        # numOfBracket = 0
        # result = ''

        # for c in target[startIndex:]:
        #     if c == '{':
        #         numOfBracket += 1
        #     elif c == '}':
        #         numOfBracket -= 1
            
        #     result += c
        #     if numOfBracket == 0:
        #         return result

        # return 

    def request(self, url=None, key=None, targetFile=None, options=None) -> List:
        pass
        # _url = url if url else self.url
        # _key = key if key else self.key
        # _targetFile = targetFile if targetFile else self.targetFile
        # # _options = options if options else self.options

        # _header = {
        #     'Content-Type': 'application/octet-stream',
        #     'Authorization': _key
        # }
        # ttsResultList = []

        # wav=open(_targetFile, 'rb')
            
        # try:
        #     response = requests.post(url = _url, headers = _header, data = wav)
        # except ConnectionError as ce:
        #     logging.exception(f'[Exception] {__class__.__name__} - {ce}')

        # if response.status_code == 200:
        #     logging.info(f'[info] {__class__.__name__} - {response.text}')

        #     responseText = response.text
        #     finalIndex = responseText.find('{"type":"finalResult"')
        #     finalResult = self._getJsonDataFromIndex(responseText, finalIndex)

        #     if not finalResult or finalIndex == -1:
        #         ttsResultList.append("")
        #         logging.exception(f'[Exception] {__class__.__name__} - json, "finalResult" not found, response = {response}')
        #     else:
        #         ttsResultList.append(json.loads(finalResult)['value'])


        # elif response.status_code == 401:
        #     logging.exception(f'[Exception] {__class__.__name__} - un-registered ips. response = {response}')
        #     return None
        # else:
        #     logging.exception(f'[Exception] {__class__.__name__} - not-expected exception occured. response = {response}')
        #     return None
        # ##### +) Response??? 400 ????????? ???????????? ?????? ????????? ????????? ?????? > ??? ??????
            
        # return ttsResultList
