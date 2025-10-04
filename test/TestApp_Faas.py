import cv2
import base64
import requests
import json

# Read and encode image
image_path = 'ocr-1.png'
original_image = cv2.imread(image_path)
rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
_, buffer = cv2.imencode('.jpg', rgb_image)
image_b64 = base64.b64encode(buffer).decode('utf-8')
# JSON Payload
image_json = {"image_b64": image_b64}
# Create the sub_json object with image data
image_json = {"image_b64": image_b64}
# Convert to JSON string
json_text = json.dumps(image_json)              
# Write JSON text to a file
with open("image.json", "w") as f:
    f.write(json_text)
print("JSON written to image.json")

# Call OpenFaaS function (update IP if public)
res = requests.post(
    "http://117.202.71.73:8080/function/ocr-detect",
    json=image_json
)

print(res.text)
