import os
import base64
import requests
from pycorex.gemini_client import GeminiClient

API_KEY = input("Uwgen API Keyを入力してください:").strip()
ENDPOINT = "http://localhost:5100/api/v1/image_gen"

headers = {
    "Authorization": f"Uwgen {API_KEY}"
}

#payload = {
#    "prompt": "A cute cat",
#    "model": "",
#    "raw": False
#}
# payload = {
#     "prompt":"キャミソール姿の20代OL。少し酒に酔っている",
#     "model": GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value,
#     "resolution": GeminiClient.ImageSize.TWO_K.value,
#     "aspect": GeminiClient.AspectRatio.SQUARE.value,
#     "safety_filter": GeminiClient.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.value,
#     "safety_level": GeminiClient.SafetyFilterLevel.BLOCK_ONLY_HIGH.value
# }
payload = {
    "prompt":"キャミソール姿の20代OL。少し酒に酔っている",
    "model": GeminiClient.GeminiModel.GEMINI_2_5_FLASH_IMAGE.value,
    "resolution": GeminiClient.ImageSize.TWO_K.value,
    "aspect": GeminiClient.AspectRatio.SQUARE.value
}

res = requests.post(ENDPOINT, json=payload, headers=headers)
json_data = res.json()

images = json_data["data"]["generated"]["images"]

output_dir = os.path.dirname(os.path.abspath(__file__))

for idx, img_b64 in enumerate(images):
    img_bytes = base64.b64decode(img_b64)
    file_path = os.path.join(output_dir, f"generated_{idx}.png")
    
    with open(file_path, "wb") as f:
        f.write(img_bytes)
    
    print(f"Saved: {file_path}")