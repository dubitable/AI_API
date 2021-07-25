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
    return json.loads(os.path.join("static", model_name, "info.json"))

def format_prediction(prediction, model_name):
    info = get_info(model_name)
    {"prediction": prediction.numpy().tolist()}

@app.route("/figdetector", methods = ["GET", "POST"])
def figdetector():
    if request.method == "GET":
        return jsonify(get_info("fig"))
    file = request.files["file"]
    image = Image.open(file.stream)
    prediction = predict(image, models["fig"])
    return jsonify(format_prediction(prediction, "fig"))

if __name__ == "__main__":
    app.run()