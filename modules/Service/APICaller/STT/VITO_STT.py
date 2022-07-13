import requests
from modules.Service.APICaller.BaseAPICaller import BaseAPICaller
import logging
import time
import json

class VITO_STT(BaseAPICaller):

    def __init__(self, url, key, targetFile=None, options=None) -> None:
        super().__init__(url, key, targetFile, options)

    def request(self, url=None, key=None, targetFile=None, options=None) -> list:
        # update params.
        _url = url if url else self.url
        _key = key if key else self.key
        _targetFile = targetFile if targetFile else self.targetFile
        _options = options if options else self.options

        resultList = []

        try:

            payload = {
                'key': {
                    'client_id': _key['vito_id_sdh'],
                    'client_secret': _key['vito_secret_sdh']
                },
                'config' : {
                    "use_multi_channel": False,
                    "diarization": {
                        "use_ars": False,
                        "use_verification": False
                    }
                }
            }

            ### Access Token
            response = requests.post(url='https://openapi.vito.ai/v1/authenticate', data=payload.get("key"))
            response.raise_for_status()
            access_token = str(response.json()['access_token'])
            header = {
                'Authorization': 'bearer ' + access_token
            }

            ### Transaction
            try:
                file = {'file': open(_targetFile, 'rb')}
            except FileNotFoundError as fe:
                logging.warning("[WARNING] file not found :: VITO_STT - {}".format(_targetFile))
                return None
            
            response = requests.post('https://openapi.vito.ai/v1/transcribe', headers=header, data={'config': json.dumps(payload.get("config"))}, files=file)
            response.raise_for_status()
            transactionId = str(response.json()['id'])
            

            ### Message
            response = requests.get('https://openapi.vito.ai/v1/transcribe/'+transactionId, headers=header)
            response.raise_for_status()
            status = response.json()['status']

            while(status == 'transcribing'):
                response = requests.get('https://openapi.vito.ai/v1/transcribe/'+transactionId, headers=header)
                response.raise_for_status()
                status = response.json()['status']

            try:
                combined_result = ""
                for result in response.json()['results']['utterances']:
                    combined_result += result['msg']
                resultList.append("\"{}\"".format(combined_result))
            except Exception as e:
                logging.warning("[WARNING] unrecognized message :: VITO_STT - {}".format(e))
                return None

        except Exception as e:
            logging.warning("[WARNING] exception occured :: VITO_STT - {}".format(e))
            return None
        
        return resultList

