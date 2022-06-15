from sre_compile import isstring
# from urllib import response
from modules.Service.API.BaseAPICaller import BaseAPICaller
from modules.Service.API.APICaller.STT.ktAiApiSDK.stt import STT as KT_STT_SDK
import modules.SoundConverter as sc
import logging
import time
import json

class KT_STT(BaseAPICaller):

    def __init__(self, url, key, targetFile=None, options=None) -> None:
        super().__init__(url, key, targetFile, options)

    def request(self, url=None, key=None, targetFile=None, options=None) -> list:
        # update params.
        _url = url if url else self.url
        _key = key if key else self.key
        _targetFile = targetFile if targetFile else self.targetFile
        _options = options if options else self.options

        # try:
        #     if options:
        #         _options['client_id'] = options['client_id']
        #         _options['client_key'] = options['client_key']
        #         _options['client_secret'] = options['client_secret']
        #     else:
        #         _options['client_id'] = self.options['client_id']
        #         _options['client_key'] = self.options['client_key']
        #         _options['client_secret'] = self.options['client_secret']
        # except TypeError:
        #     logging.error(f'[ERR] {__class__.__name__} - wrong options input in {__name__}')

        # convert soundFile.format to mp3
        if not str(_targetFile).endswith('.mp3'):
            sc.convertWAVtoMP3(_targetFile)
            _targetFile = f'{_targetFile[:-4]}.mp3'

        # set - KT STT Client
        kt_sttClient = KT_STT_SDK()
        kt_sttClient.setAuth(clientKey=_key['client_key'],
                            clientId=_key['client_id'],
                            clientSecret=_key['client_secret'])

        # request options
        stt_mode = 2
        target_language = "ko"
        encoding = "mp3"        # raw, wav, mp3, vor, aac, fla
        # encodingOpt
        channel = 1             # 1:mono, 2:streo
        sample_rate = 16000     # 16000, 44100, 48000
        sample_fmt = "S16LE"    # Signed 16-bit Little Endian : "S16LE", Float 32-bit Little Endian : "F32LE"

        sttResult = []
        with open(_targetFile, mode='rb') as file:
            audio_data = file.read()
            result_json:dict = kt_sttClient.requestSTT(audio_data, stt_mode, target_language, encoding, channel, sample_rate, sample_fmt)
            logging.info(f'response of kt_stt = {result_json}')


            if isstring(result_json):
                result_json = json.loads(result_json)
            
            if not result_json or result_json.get('statusCode') != 200:
                logging.exception(f'[Exception] {__class__.__name__} - None Transaction id')
                logging.exception(result_json)
                return sttResult


            # request transaction_id
            result_array = result_json.get("result")
            transaction_id = json.loads(result_array[0]).get("transactionId")
            logging.info(f'transaction_id = {transaction_id}')


            # request stt_data from transaction_id
            query_result_json = kt_sttClient.querySTT(transaction_id)
            logging.info(f'query_result_json = {query_result_json}')


            # waiting for request
            timeout = 10
            while not query_result_json or query_result_json.get('sttStatus') == 'processing':
                query_result_json = kt_sttClient.querySTT(transaction_id)
                logging.info(f'waiting,,, query_result_json = {query_result_json}')
                if timeout > 0:
                    timeout -= 1
                    time.sleep(1)
                else:
                    logging.exception(f'[Exception] {__class__.__name__} - timeout - response = {query_result_json}')
                    return sttResult

            # parse stt_data
            if query_result_json.get('statusCode') == 200 and query_result_json.get('sttStatus') == 'completed':
                jsonResult = query_result_json.get('sttResults')
                if jsonResult:
                    for eachResult in jsonResult:
                        sttResult.append(f"\"{eachResult['text']}\"")
                else:
                    logging.exception(f'[Exception] {__class__.__name__} - response = {query_result_json}')
            else:
                logging.exception(f'[Exception] {__class__.__name__} - response = {query_result_json}')

        return sttResult
