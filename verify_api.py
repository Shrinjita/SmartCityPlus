import requests

# API Details
API_KEY = "Kp1AqMurWRBXStFinPNM"
MODEL_ID = "waste-classification-uwqfy/1"
API_URL = f"https://detect.roboflow.com/{MODEL_ID}"

# Use local image file
local_image_path = "istockphoto-927987734-612x612.jpg"

# Make an inference request
with open(local_image_path, "rb") as image_file:
    response = requests.post(
        API_URL,
        params={"api_key": API_KEY, "confidence": 20},
        files={"file": image_file}
    )

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
