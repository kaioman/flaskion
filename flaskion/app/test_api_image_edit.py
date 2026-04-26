import os
import base64
import requests
from pycorex.gemini_client import GeminiClient

API_KEY = input("Uwgen API Keyを入力してください:").strip()
ENDPOINT = "http://localhost:5100/api/v1/image_edit"

headers = {
    "Authorization": f"Uwgen {API_KEY}"
}

payload = {
    "prompt":"ポーズや構図はそのままで、笑顔にして",
    "model": GeminiClient.GeminiModel.GEMINI_2_5_FLASH_IMAGE.value,
    "resolution": GeminiClient.ImageSize.TWO_K.value,
    "aspect": GeminiClient.AspectRatio.SQUARE.value,
    "safety_filter": GeminiClient.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.value,
    "safety_level": GeminiClient.SafetyFilterLevel.BLOCK_ONLY_HIGH.value
}

base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, "analyze_test_pic.png")

files = {
    "sourceImage": open(image_path, "rb")
}

res = requests.post(ENDPOINT, data=payload, files=files, headers=headers)
json_data = res.json()

if json_data["data"]:

    images = json_data["data"]["generated"]["images"]

    output_dir = os.path.dirname(os.path.abspath(__file__))

    for idx, img_b64 in enumerate(images):
        img_bytes = base64.b64decode(img_b64)
        file_path = os.path.join(output_dir, f"generated_{idx}.png")
        
        with open(file_path, "wb") as f:
            f.write(img_bytes)
        
        print(f"Saved: {file_path}")
else:
    if json_data["errors"]:
        print(f"{json_data["errors"]}")