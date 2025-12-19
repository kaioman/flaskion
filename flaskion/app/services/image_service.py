from flask import jsonify
from http import HTTPStatus
from pydantic import ValidationError
from pycorex.gemini_client import GeminiClient
from ..models.image_gen_params import ImageGenParams

def generate_image(param_data: dict):
    try:
        # フォームの入力値をパラメーターモデルクラスに設定する
        params = ImageGenParams(**param_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), HTTPStatus.INTERNAL_SERVER_ERROR
    
    # プロンプト入力チェック
    if not params.prompt:
        error_message = "プロンプトを入力してください"
        return jsonify({"error": error_message}), HTTPStatus.BAD_REQUEST
    
    results: list[str] = [
        "static/generated/test004.png",
        "static/generated/test005.png"
    ]
    # GeminiClient
    return jsonify({"generated": results}), HTTPStatus.OK

def get_models():
    return GeminiClient.GeminiModel

def get_resolutions():
    return GeminiClient.ImageSize

def get_aspects():
    return GeminiClient.AspectRatio

def get_safety_filters():
    return GeminiClient.HarmCategory

def get_safety_levels():
    return GeminiClient.SafetyFilterLevel
