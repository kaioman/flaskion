import os
import json
import base64
import requests
from http import HTTPStatus

def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
API_KEY = input("Uwgen API Keyを入力してください:").strip()
ENDPOINT = "http://localhost:5100/api/v1/image_gen"

headers = {
    "Authorization": f"Uwgen {API_KEY}"
}

workflow = _load_json("flaskion/configs/comfyui/workflow/aoi-IPAdapter9.json")
persona_conf = _load_json("flaskion/configs/comfyui/prompt/persona/Aoi.json")
camera_conf = _load_json("flaskion/configs/comfyui/prompt/camera_angules.json")
wardrobe_conf = _load_json("flaskion/configs/comfyui/prompt/wardrobe.json")
environment_conf = _load_json("flaskion/configs/comfyui\prompt/environments.json")
workflow_mod_conf = _load_json("flaskion/configs/comfyui/workflow/aoi_workflow_config.json")

payload = {
    "provider": "comfyui",
    "workflow_json": workflow,
    "workflow_mod_json": workflow_mod_conf,
    "prompt_randomize": True,
    "persona_json": persona_conf,
    "camera_angle_json": camera_conf,
    "wardrobe_json": wardrobe_conf,
    "environment_json": environment_conf,
    "batch_size": 1,
    "rating_level": 2
}

res = requests.post(ENDPOINT, json=payload, headers=headers)
json_data = res.json()
if res.status_code == HTTPStatus.OK:
    
    images = json_data["data"]["generated"]["images"]

    output_dir = os.path.dirname(os.path.abspath(__file__))

    for idx, img_b64 in enumerate(images):
        img_bytes = base64.b64decode(img_b64)
        file_path = os.path.join(output_dir, f"generated_{idx}.png")
        
        with open(file_path, "wb") as f:
            f.write(img_bytes)
        
        print(f"Saved: {file_path}")
else:
    print(json_data)