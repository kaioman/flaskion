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
payload = {
    "prompt":"20代OLが電車の長いすに座っている",
    "model": GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value,
    "resolution": GeminiClient.ImageSize.ONE_K.value,
    "aspect": GeminiClient.AspectRatio.SQUARE.value,
    "safety_filter": GeminiClient.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.value,
    "safety_level": GeminiClient.SafetyFilterLevel.BLOCK_ONLY_HIGH.value
}

res = requests.post(ENDPOINT, json=payload, headers=headers)

print(res)