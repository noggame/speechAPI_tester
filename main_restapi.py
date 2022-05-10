
import json
from flask import Flask, request
from modules.Controller.VisionTestController import FaceTestController
from modules.Controller.VoiceTestController import STTTestController
# from waitress import serve

app = Flask(__name__)
base_url = ''

@app.route(f"{base_url}/")
def hello_world():
    return "<p>HWorld!</p>"

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

    if not result:
        return "empty"

    return str(result)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=9090)
    # app.run(debug=False, host='127.0.0.1', port=9090)

