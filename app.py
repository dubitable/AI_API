from flask import Flask, request, jsonify, Response
from predictions import load_model, predict
from PIL import Image
import json, os, sys

models = {
    "fig": load_model("fig")
}

with open("headers.json", "r") as file:
    headers = json.loads(file.read())

print(headers)

UPLOAD_FOLDER = "/uploads"

app = Flask(__name__, static_url_path = "/static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_info(model_name):
    filename = os.path.join("static", model_name, "info.json")
    with open(filename, "r") as file:
        return json.loads(file.read())

def format_predictions(predictions, model_name):
    predictions = predictions.numpy().tolist()
    info = get_info(model_name)
    return {class_name : str(prediction) for class_name, prediction in zip(info["class_names"], predictions)}

def make_response(dictionary):
    response = Response(json.dumps(dictionary))
    for key, value in headers.items():
        response.headers[key] = value
    return response

@app.route("/figdetector", methods = ["GET", "POST", "OPTIONS"])
def figdetector():     
    if request.method == "POST":
        file = request.files["file"]
        image = Image.open(file.stream)
        print(image.size, file=sys.stdout)
        predictions = predict(image, models["fig"])
        formatted_predictions = format_predictions(predictions, "fig")
        return make_response(formatted_predictions)
    return make_response(get_info("fig"))

if __name__ == "__main__":
    app.run()