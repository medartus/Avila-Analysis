import flask
import collections
from flask import request, jsonify
import pickle
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

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
FINAl_COLUMNS = DATASET_COLUMNS + ['spacing_ratio', 'mrg_ratio']

with open('./api/model.pickle', 'rb') as handle:
    model = pickle.load(handle)


def CreateArray(args, columns):
    dic = collections.OrderedDict()
    for index, columnName in enumerate(columns):
        value = request.args.get(f'F{index}')
        if not value:
            value = request.args.get(columnName)
        if value:
            dic[columnName] = float(value)
        else:
            return (False, {"code": 400, "description": f"You need to specify a value for F{index} or {columnName}"})

    dic['spacing_ratio'] = dic['intercolumnar_dist'] / \
        (dic['upper_mrg'] + dic['lower_mrg'])
    dic['mrg_ratio'] = dic['upper_mrg'] / dic['lower_mrg']

    npArr = np.array(list(dic.values()))
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


@app.route('/', methods=['GET'])
def root():
    return CreateResponse(False, {"code": 404, "description": "Please use GET /predict with parameters to predict the classification"})


@app.route('/predict', methods=['GET'])
def predict():
    try:
        hasAllParameters, result = CreateArray(request.args, DATASET_COLUMNS)
        if not hasAllParameters:
            return CreateResponse(False, result)
        responseContent = {}
        responseContent["class"] = model.predict(result)[0]
        for index, columnName in enumerate(FINAl_COLUMNS):
            responseContent[columnName] = result[0][index]

        return CreateResponse(True, responseContent)
    except:
        return CreateResponse(
            False, {"code": 500, "description": "Internal Server Error"})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return CreateResponse(False, {"code": 404, "description": "Only GET /predict is available"})


if __name__ == '__main__':
    app.run()
