from modules.TTS.ktAiApiSDK.stt import STT
import logging
import time
import json

def requestKtSTT(file_path, client_id=None, client_key=None, client_secret=None):
    stt_client = STT()

    client_id = client_id if client_id else "3fd7261c-7d08-487b-a104-b867919e497b"
    client_key = client_key if client_key else "d8613f5b-43f1-5a11-b183-35261da543a6"
    client_secret = client_secret if client_secret else "693bc75a1bf4f80d2636372c02b64d0c5a636757e1b9ae6ddfd5c209f9d32892"

    stt_client.setAuth(client_key, client_id, client_secret)

    stt_mode = 2
    target_language = "ko"
    encoding = "mp3"        # raw, wav, mp3, vor, aac, fla
    # encodingOpt
    channel = 1             # 1:mono, 2:streo
    sample_rate = 16000     # 16000, 44100, 48000
    sample_fmt = "S16LE"    # Signed 16-bit Little Endian : "S16LE", Float 32-bit Little Endian : "F32LE"

    with open(file_path, mode='rb') as file:
        audio_data = file.read()
        result_json = stt_client.requestSTT(audio_data, stt_mode, target_language, encoding, channel, sample_rate, sample_fmt)

        try:
            # request transaction_id
            result_array = result_json.get("result")
            transaction_id = json.loads(result_array[0]).get("transactionId")
            time.sleep(5)

            # request stt_data from transaction_id
            query_result_json = stt_client.querySTT(transaction_id)
            
            # parse stt_data
            stt_answer = 'empty'

            if query_result_json.get('statusCode') == 200:
                for ktstt in query_result_json['sttResults']:
                    stt_answer = ktstt['text']
                    logging.info(f'[KT_STT] {stt_answer}')

        except Exception:
            logging.exception(f'[Exception] request err - result_array = {result_array}, query_result_json = {query_result_json}')

        return stt_answer
