import flask
from flask import request, jsonify
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DATASET_COLUMNS = [
    'intercolumnar_dist',
    'upper_mrg',
    'lower_mrg',
    'exploit',
    'row_num',
    'modular_ratio',
    'spacing',
    'weight',
    'peak_num',
    'modular/spacing'
]

with open('model.pickle', 'rb') as handle:
    model = pickle.load(handle)


def CreateArray(args, columns):
    # arr = np.array([0.364825, -0.189174, 0.502357, 0.223290, -
    #                 1.168333, -3.837595, 0.069175, 0.534971, -2.149801, -3.417834])
    # return (True, arr.reshape(1, -1))
    arr = []
    for index, columnName in enumerate(columns):
        value = 'plop'
        value = request.args.get(f'F{index}')
        if not value:
            value = request.args.get(columns[index])
        if value:
            arr.append(value)
        else:
            return (False, {"code": 400, "description": f"You need to specify a value for F{index} or {columnName}"})
    npArr = np.array(arr)
    return (True, npArr.reshape(1, -1))


def CreateResponse(isSuccess, content):
    if isSuccess:
        return jsonify({
            "status": "OK",
            "data": content
        })
    return jsonify({
        "status": "Error",
        "data": None,
        "error":  {
            "errorCode": content['code'],
            "description": content['description']
        }
    })


@app.route('/predict', methods=['GET'])
def predict():
    try:
        hasAllParameters, result = CreateArray(request.args, DATASET_COLUMNS)
        if not hasAllParameters:
            return CreateResponse(False, result)
        responseContent = {}
        responseContent["class"] = model.predict(result)[0]
        for index, columnName in enumerate(DATASET_COLUMNS):
            responseContent[columnName] = result[0][index]

        return CreateResponse(True, responseContent)
    except:
        return CreateResponse(
            False, {"code": 500, "description": "Internal Server Error"})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path


if __name__ == '__main__':
    app.run()
