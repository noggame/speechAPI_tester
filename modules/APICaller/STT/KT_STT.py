from typing import List
from modules.APICaller.APICaller import APICaller
from modules.APICaller.STT.ktAiApiSDK.stt import STT as KT_STT_SDK
import modules.SoundConverter as sc
import logging
import time
import json

class KT_STT(APICaller):

    def __init__(self, url=None, key=None, targetFile=None, options=None) -> None:
        super().__init__(url, key, targetFile, options)

    def request(self, url=None, key=None, targetFile=None, options=None) -> List:
        # update params.
        _url = url if url else self.url
        _key = key if key else self.key
        _targetFile = targetFile if targetFile else self.targetFile
        _options = {}

        try:
            if options:
                _options['client_id'] = options['client_id']
                _options['client_key'] = options['client_key']
                _options['client_secret'] = options['client_secret']
            else:
                _options['client_id'] = self.options['client_id']            # "3fd7261c-7d08-487b-a104-b867919e497b"
                _options['client_key'] = self.options['client_key']          # "d8613f5b-43f1-5a11-b183-35261da543a6"
                _options['client_secret'] = self.options['client_secret']    # "693bc75a1bf4f80d2636372c02b64d0c5a636757e1b9ae6ddfd5c209f9d32892"
        except TypeError:
            logging.error(f'[ERR] {__class__.__name__} - wrong options input in {__name__}')

        # convert soundFile.format to mp3
        if not str(_targetFile).endswith('.mp3'):
            sc.convertWAVtoMP3(_targetFile)
            _targetFile = f'{_targetFile[:-4]}.mp3'

        # set - KT STT Client
        kt_sttClient = KT_STT_SDK()
        kt_sttClient.setAuth(clientKey=_options['client_key'],
                            clientId=_options['client_id'],
                            clientSecret=_options['client_secret'])

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
            result_json = kt_sttClient.requestSTT(audio_data, stt_mode, target_language, encoding, channel, sample_rate, sample_fmt)
            
            if not result_json or result_json.get('statusCode') != 200:
                logging.exception(f'[Exception] {__class__.__name__} - None Transaction id')
                return

            try:
                # request transaction_id
                result_array = result_json.get("result")
                transaction_id = json.loads(result_array[0]).get("transactionId")
                time.sleep(3)

                # request stt_data from transaction_id
                query_result_json = kt_sttClient.querySTT(transaction_id)

                # parse stt_data
                if query_result_json.get('statusCode') == 200 and query_result_json.get('sttStatus') == 'completed':
                    jsonResult = query_result_json.get('sttResults')
                    if jsonResult:
                        for eachResult in jsonResult:
                            sttResult.append(eachResult['text'])
                            logging.info(f'[KT_STT] {sttResult}')
                    else:
                        logging.exception(f'[Exception] {__class__.__name__} - response = {query_result_json}')

            except SyntaxError as se:
                logging.exception(f'[Exception] {__class__.__name__} - parsing exception : {se}')

        return sttResult
