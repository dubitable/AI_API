import requests

api = "http://127.0.0.1:5000/figdetector"

response = requests.post(api, json={"text":"Testing Message"})
print(response.json())