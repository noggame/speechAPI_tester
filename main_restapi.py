# from modules.Controller.VisionTestController import FaceTestController
# from trash.VoiceTestController import STTTestController
# from waitress import serve

import json
import logging
from flask import Flask, request
from modules.Controller.TestController import TestController
from modules.Service.Type import SERVICE_TYPE
from modules.DesignPattern.Factory import DataParserFactory as df, ServiceFactory as sf


app = Flask(__name__)
base_url = ''
tc = TestController()
logging.getLogger().setLevel(logging.INFO)
# (format='%(asctime)s %(message)s')

@app.route(f"{base_url}/")
def hello_world():
    return "<p>Homepage!</p>"


@app.route(f"{base_url}/test", methods=['Post'])
def test_accuracy():

    ### Get request_data
    try:
        params:dict = json.loads(request.get_data(as_text=True))

        try:
            # TODO: 데이터 제한개수가 0개일 경우, option으로 전체 테스트 요청이 왔는지 확인. >> 전체요청이 아닌 경우 잘못된 요청으로 처리
            test_option = {
                'data_limit' : int(params['data_limit']),
                'update_data' : True
            }
        except:
            logging.error("[ERROR] Wrong input - not a number (on data limit)")
            return "Wrong Input"

        data_name = params['data_name']
        service_provider = params['service_provider']
        service_type = params['service_type']

    except ValueError as ve:
        logging.error("[ERROR] ValueError occured :: main_restapi - {}".format(ve))
        return None
    except:
        logging.error("[ERROR] unexpected error occured :: main_restapi")
        return None


    try:
        testResultList = tc.testWith(testdata = df.DATA_NAME.__getitem__(name=data_name),
                                service_provider = sf.PROVIDER.__getitem__(name=service_provider),
                                service_type = SERVICE_TYPE.__getitem__(name=service_type),
                                option = test_option)
    except:
        logging.error("[ERROR] Fail to test_request on test_accuracy()")
        return str("Test Failed. - Check options or Contact to admin.")

    if not testResultList:
        return "empty"
    return str("샘플수 : {}, 평균_정확도 : {}".format(testResultList[0], testResultList[1]))


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=9090)
    # app.run(debug=False, host='127.0.0.1', port=9090)

