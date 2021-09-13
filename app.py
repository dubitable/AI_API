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

def clearfacts():
    with open("facts.txt", "w") as file: pass

clearfacts()

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
        b64_image = request.get_json()["base64"]
        bin_image = base64.b64decode(b64_image)
        image = Image.open(io.BytesIO(bin_image))
        print(image.size)
        predictions = predict(image, models["fig"])
        formatted_predictions = format_predictions(predictions, "fig")
        print(formatted_predictions)
        return formatted_predictions
    return get_info("fig")

@app.route("/figfacts", methods = ["GET", "POST", "OPTIONS"])
def figfacts():
    if request.method == "POST":
        json = request.get_json()
        if "clear" in json.keys():
            clearfacts()
        else:
            fact = json["fact"]
            with open("facts.txt", "a") as file:
                file.write(f"{fact}\n")

    with open("facts.txt", "r") as file:
        facts = [fact for fact in file.read().split("\n") if fact != ""]
        return jsonify(facts)

@app.route("/combine", methods = ["GET", "POST", "OPTIONS"])
def combine():
    if request.method == "POST":
        json = request.get_json()
        images = []
        for b64 in json["images"]:
            bin_image = base64.b64decode(b64)
            images.append(Image.open(io.BytesIO(bin_image)))
        side, _ = images[0].size
        image = Image.new("RGB", (side * 4, side * 4))
        elem = 0
        for i in range(4):
            for j in range(4):
                image.paste(images[elem], (j * side, i * side))
                elem += 1
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return jsonify({"combined": str(img_str).removeprefix("b'")})

if __name__ == "__main__":
    app.run()