import requests

api = "http://127.0.0.1:5000/figdetector"
img_path = "/Users/pierrequereuil/Desktop/head.jpg"

files = {
    "file": open(img_path, "rb")
}

response = requests.post(api, files=files)
print(response.json())