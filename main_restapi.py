
import json
from flask import Flask, request
from modules.Accuracy.STTAccuracyToolForAPI import STTAccuracyTool

app = Flask(__name__)
base_url = ''

@app.route(f"{base_url}/")
def hello_world():
    return "<p>HWorld!</p>"

@app.route(f"{base_url}/test/stt", methods=['Post'])
def accuracy():
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

    sat = STTAccuracyTool()
    result = sat.STTtestWith(data_name=testdata["data"], api_name=testdata["api"], number=testdata["number"])

    if not result:
        return "empty"

    return str(result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5700)

