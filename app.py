import os
import pandas as pd
import numpy as np
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)
MODEL_PATH = 'superkart_model.joblib'
model = joblib.load(MODEL_PATH)

@app.route('/v1/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)[0]
        return jsonify({'prediction': float(prediction), 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part', 'status': 'error'}), 400
        file = request.files['file']
        input_df = pd.read_csv(file)
        predictions = model.predict(input_df)
        predictions_dict = {str(i): float(pred) for i, pred in enumerate(predictions)}
        return jsonify(predictions_dict), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=False)
