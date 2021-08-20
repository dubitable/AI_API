import base64, json, os, io, sys

from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image

import numpy as np

from predictions import load_model, predict

models = {
    "fig": load_model("fig")
}

UPLOAD_FOLDER = "/uploads"

app = Flask(__name__, static_url_path = "/static")
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_info(model_name):
    filename = os.path.join("static", model_name, "info.json")
    with open(filename, "r") as file:
        return json.loads(file.read())

def format_predictions(predictions, model_name):
    predictions = predictions.numpy().tolist()
    info = get_info(model_name)
    confidences = {class_name : str(prediction) for class_name, prediction in zip(info["class_names"], predictions)}
    return {
        "confidences": confidences,
        "class_name": info["class_names"][np.argmax(predictions)],
        "value": np.max(predictions)
    }


@app.route("/figdetector", methods = ["GET", "POST", "OPTIONS"])
def figdetector():     
    if request.method == "POST":
        file = request.files["file"]
        image = Image.open(file.stream)
        predictions = predict(image, models["fig"])
        formatted_predictions = format_predictions(predictions, "fig")
        return formatted_predictions
    return get_info("fig")

@app.route("/figdetectorjs", methods = ["GET", "POST", "OPTIONS"])
def figdetectorjs():     
    if request.method == "POST":
        content = request.get_json()
        b64_image = content["image"]["uri"].replace("data:image/png;base64,", "")
        print(content["image"].keys(), file=sys.stdout)
        print(len(b64_image), len(b64_image) % 4)
        bin_image = base64.b64decode(b64_image)
        image = Image.open(io.BytesIO(bin_image))
        predictions = predict(image, models["fig"])
        formatted_predictions = format_predictions(predictions, "fig")
        return formatted_predictions
    return get_info("fig")

if __name__ == "__main__":
    app.run()