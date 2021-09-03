import requests

local = "http://127.0.0.1:5000/figfacts"
api = "https://detectors.herokuapp.com/figfacts"

response = requests.post(local, json={"fact": "true"})
response = requests.post(local, json={"fact": "true"})
response = requests.post(local, json={"fact": "true"})
response = requests.post(local, json={"fact": "true"})

response = requests.get(local)
print(response.json())