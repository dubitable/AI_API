from flask import Flask, request, jsonify
from predictions import load_model, predict
from PIL import Image

models = {
    "fig": load_model("fig")
}
UPLOAD_FOLDER = "/uploads"

app = Flask(__name__, static_url_path = "/static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/figdetector", methods = ["POST"])
def figdetector():
   file = request.files["file"]
   image = Image.open(file.stream)
   prediction = predict(image, models["fig"])
   return jsonify({"prediction": prediction.numpy().tolist()})

if __name__ == "__main__":
    app.run()