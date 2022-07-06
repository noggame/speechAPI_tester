# from modules.Controller.VisionTestController import FaceTestController
# from trash.VoiceTestController import STTTestController
# from waitress import serve

import json
import logging
from flask import Flask, request
from modules.Controller.TestController import TestController
from modules.Service.Type import SERVICE_TYPE
from modules.DesignPattern.Factory import DataParserFactory as df, ServiceFactory as sf, AnlalyzerFactory as af




app = Flask(__name__)
base_url = ''

@app.route(f"{base_url}/")
def hello_world():
    return "<p>HWorld!</p>"


@app.route(f"{base_url}/test/stt", methods=['Post'])
def test_accuracy():

    ### Get request_data
    try:
        params = json.loads(request.get_data(as_text=True))

        # testdata = {
        #     'data' : params['data_name'],
        #     'api' : params['api_name'],
        #     'number' : 2
        # }

        test_option = {
            'data_limit' : params['data_limit'],
            'update_data' : True
        }

        data_name = params['data_name']
        service_provider = params['service_provider']
        service_type = params['service_type']

    except ValueError as ve:
        print(ve)
        return None


    tc = TestController()

    ########## Face
    # tc = TestController()
    test_option = {
        'data_limit' : 1,
        'update_data' : True
    }

    try:
        testResultList = tc.testWith(testdata = df.DATA_NAME.__getitem__(name=data_name),
                                service_provider = sf.PROVIDER.__getitem__(name=service_provider),
                                service_type = SERVICE_TYPE.__getitem__(name=service_type),
                                option = test_option)
    except:
        logging.error("[ERROR] Fail to test_request on test_accuracy()")
        return str("Test Failed. - Check options or Contact to admin.")

    if not testResultList:
        return "empry"
    return str("샘플수 : {}, 평균_정확도 : {}".format(testResultList[0], testResultList[1]))



@app.route(f"{base_url}/test/stt", methods=['Post'])
def accuracy_stt():
    try:
        params = json.loads(request.get_data(as_text=True))
    except ValueError as ve:
        print(ve)
        return None
    
    ### Input
    testdata = {
        'data' : params['data_name'],
        'api' : params['api_name'],
        'number' : 2
    }

    stc = STTTestController()
    result = stc.startTestAndAnalysis(data_name=testdata["data"], api_name=testdata["api"], number=testdata["number"])
    print(result)

    if not result:
        return "empty"

    return str(result)


@app.route(f"{base_url}/test/faceDetection", methods=['Post'])
def accuracy_face():
    try:
        params = json.loads(request.get_data(as_text=True))
    except ValueError as ve:
        print(ve)
        return None
    
    ### Input
    testdata = {
        'data' : params['data_name'],
        'api' : params['api_name'],
        'number' : 2
    }

    ftc = FaceTestController()
    result = ftc.startTestAndAnalysis(data_name=testdata["data"], api_name=testdata["api"], number=testdata["number"])
    print(result)

    if not result:
        return "empty"

    return str(result)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=9090)
    # app.run(debug=False, host='127.0.0.1', port=9090)

