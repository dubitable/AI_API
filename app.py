from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/figdetector", methods = ["POST"])
def figdetector():
   request_data = request.get_json()
   return request_data
    

if __name__ == "__main__":
    app.run()