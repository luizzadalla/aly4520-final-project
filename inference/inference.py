import json
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_PATH = "models/model.pkl"
model = joblib.load(MODEL_PATH)


@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200


@app.route("/invocations", methods=["POST"])
def invocations():
    try:
        data = request.get_json()

        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            return jsonify({"error": "Input must be a JSON object or list of objects"}), 400

        preds = model.predict(df)
        return jsonify({"prediction": preds.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)