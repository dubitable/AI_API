import base64, requests, io
from PIL import Image

images = []
for i in range(16):
    with open(f"/Users/pierrequereuil/Desktop/Projects/ReactNative/heart/prep/{i}.png", "rb") as img_file:
        images.append(str(base64.b64encode(img_file.read())).removeprefix("b'"))

json = {
    "images": images
}

response = requests.post("http://127.0.0.1:5000/combine", json=json)
bin_image = base64.b64decode(response.json()["combined"])
image = Image.open(io.BytesIO(bin_image))

image.save("combined.png")