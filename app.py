from flask import Flask, request, jsonify
from predictions import load_model, predict
from PIL import Image
import json, os

models = {
    "fig": load_model("fig")
}

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

@app.route("/figdetector", methods = ["GET", "POST"])
def figdetector():
    if request.method == "GET":
        return jsonify(get_info("fig"))
    file = request.files["file"]
    image = Image.open(file.stream)
    predictions = predict(image, models["fig"])
    formatted_predictions = format_predictions(predictions, "fig")
    return jsonify(formatted_predictions)

if __name__ == "__main__":
    app.run()