import requests
from pycorex.gemini_client import GeminiClient

API_KEY = input("Uwgen API Keyを入力してください:").strip()
ENDPOINT = "http://localhost:5100/api/v1/text_gen"

headers = {
    "Authorization": f"Uwgen {API_KEY}"
}

payload = {
    "prompt":"三権分立について教えてください",
    "model": GeminiClient.GeminiModel.GEMINI_2_5_FLASH_LITE.value,
}

res = requests.post(ENDPOINT, json=payload, headers=headers)
if res.status_code == 200:
    json_data = res.json()

    gen_text = json_data["data"]["generated"]["result"]

    print(gen_text)
