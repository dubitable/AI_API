import requests

local = "http://127.0.0.1:5000/figdetector"
api = "https://detectors.herokuapp.com/figdetector"
img_path = "/Users/pierrequereuil/Desktop/head.jpg"

files = {
    "file": open(img_path, "rb")
}


response = requests.post(local, files=files)
print(response.json())