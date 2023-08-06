from flask import Flask, render_template, jsonify, request
import numpy as np
import pickle

app = Flask(__name__)

outlet_map = {
    'OUT049': 1999,
    'OUT018': 2009,
    'OUT010': 1998,
    'OUT013': 1987,
    'OUT027': 1985,
    'OUT045': 2002,
    'OUT017': 2007,
    'OUT046': 1997,
    'OUT035': 2004,
    'OUT019': 1985
}

outlets = list(outlet_map.keys())
outlets.sort()

model = pickle.load(open('models/model.pkl', 'rb'))


def get_outlet_sales(features):
    arr = np.zeros(25)
    outlet = outlets[int(features[-1])]

    arr[0] = features[0]
    arr[1] = features[1]
    arr[2] = features[2]
    arr[3] = features[1] / 0.7
    arr[4] = 2023 - outlet_map[outlet]
    arr[5 + int(features[3])] = 1
    arr[7 + int(features[4])] = 1
    arr[9 + int(features[3])] = 1
    arr[11 + int(features[3])] = 1
    arr[13 + int(features[4])] = 1
    arr[16 + int(features[5])] = 1

    sales = model.predict(arr.reshape(1, -1))

    return np.round(sales, 2)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        features = np.array([float(x) for x in request.form.values()])
        sales = get_outlet_sales(features)
        return render_template('index.html', sales=sales[0])

    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    features = np.array([float(x) for x in request.form.values()])
    sales = get_outlet_sales(features)

    return render_template('index.html', sales=sales[0])


@app.route('/get-outlets', methods=['POST'])
def get_outlets():
    response = jsonify({
        'outlets': outlets
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True)
