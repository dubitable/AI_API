from flask import Flask, request, url_for, redirect, jsonify
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = "/uploads"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/figdetector", methods = ["POST"])
def figdetector():
   file = request.files["file"]
   img = Image.open(file.stream)
   return jsonify({"Size": img.size})

if __name__ == "__main__":
    app.run()