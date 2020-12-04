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
    arr = []
    for index, columnName in enumerate(columns):
        value = request.args.get(f'F{index}')
        if not value:
            value = request.args.get(columns[index])
        if value:
            arr.append(value)
        else:
            return (False, {"code": 400, "description": f"You need to specify a value for F{index} or {columnName}"})

    # NE PAS OUBLIER DE CREER LES NOUVELLES COLONNES (Nico doit le faire)
    # df['spacing_ratio'] = df['intercolumnar_dist'] / \(df['upper_mrg'] + df['lower_mrg'])
    # df['mrg_ratio'] = df['upper_mrg'] / df['lower_mrg']

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
        for index, columnName in enumerate(DATASET_COLUMNS):
            responseContent[columnName] = result[0][index]

        return CreateResponse(True, responseContent)
    except:
        return CreateResponse(
            False, {"code": 500, "description": "Internal Server Error"})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return CreateResponse(False, {"code": 404, "description": "Only /predict is available"})


if __name__ == '__main__':
    app.run()
