import os
import requests
from pycorex.gemini_client import GeminiClient

API_KEY = input("Uwgen API Keyを入力してください:").strip()
ENDPOINT = "http://localhost:5100/api/v1/image_analyze"

headers = {
    "Authorization": f"Uwgen {API_KEY}"
}

payload = {
    "prompt":"西暦2200年のイラストレーターになりきって、この画像の説明をしてください。口調は丁寧語。内容は毒舌。文字数はX(Twitter)の1ポスト(140文字以内)に収まるよう作成してください",
    "model": GeminiClient.GeminiModel.GEMINI_3_0_FLASH_PREVIEW.value,
}

base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, "hero_02.png")

files = {
    "sourceImage": open(image_path, "rb")
}

res = requests.post(ENDPOINT, data=payload, files=files, headers=headers)
if res.status_code == 200:
    json_data = res.json()

    image_text = json_data["data"]["generated"]

    print(image_text)
