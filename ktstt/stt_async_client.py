from ktstt.ktAiApiSDK.stt import STT
import time
import json

# def requestKTAPI(file_path=None):
# def __main__(file_path=None):
def requestKtSTT(file_path):
    stt_client = STT()

    client_id = "3fd7261c-7d08-487b-a104-b867919e497b"
    client_key = "d8613f5b-43f1-5a11-b183-35261da543a6"
    client_secret = "693bc75a1bf4f80d2636372c02b64d0c5a636757e1b9ae6ddfd5c209f9d32892"

    stt_client.setAuth(client_key, client_id, client_secret)

    stt_mode = 2
    target_language = "ko"
    encoding = "mp3"
    # encodingOpt
    channel = 1
    sample_rate = 16000
    sample_fmt = "S16LE"

    # file_path = '/mnt/d/Workspace/Python/temp_http/sample/short.mp3'
    file_path = '/mnt/d/Workspace/Python/speechAPI_tester/sample_nodup/S00000001/0001.mp3'
    print(file_path)
    

    with open(file_path, mode='rb') as file:
        audio_data = file.read()
        result_json = stt_client.requestSTT(audio_data, stt_mode, target_language, encoding, channel, sample_rate, sample_fmt)
        print(result_json)

        result_array = result_json.get("result")
        transaction_id = json.loads(result_array[0]).get("transactionId")
        
        time.sleep(5)

        query_result_json = stt_client.querySTT(transaction_id)
        print(query_result_json)

        return query_result_json
