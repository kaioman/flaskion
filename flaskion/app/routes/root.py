from flask import Blueprint, render_template, jsonify, request
from typing import Any, Optional
from pycorex.gemini_client import GeminiClient
from app.services.image_service import ImageGenService
from app.core.security import get_user_from_session, mask_api_key

# Blueprint定義
root_bp = Blueprint('root', __name__)

@root_bp.get("/")
def index():
    """
    インデックスページを表示するルート 
    
    Returns
    -------
    str
        index.html テンプレートをレンダリングした HTML
    """
    return render_template("index.html")

@root_bp.get("/signin")
def signin():
    return render_template("signin.html", hide_nav_items=True)

@root_bp.get("/signup")
def signup():
    return render_template("signup.html", hide_nav_items=True)

@root_bp.get("/gallery")
def gallery():
    return render_template("gallery.html")

@root_bp.get("/settings")
def settings():
    
    # ログインユーザーを取得
    user = get_user_from_session()

    # uwgen APIキーをマスクする
    if user.uwgen_api_key:
        masked_uwgen_api_key = mask_api_key(user.uwgen_api_key)
    else:
        masked_uwgen_api_key = "[未発行]"
    
    # gemini APIキーをマスクする
    if user.gemini_api_key_encrypted:
        masked_gemini_api_key = mask_api_key(user.gemini_api_key_encrypted)
    else:
        masked_gemini_api_key = '[未設定]'

    # gemini(VertexAI) APIキーをマスクする
    if user.gemini_api_key_vertexai_encrypted:
        masked_gemini_api_key_vertexai = mask_api_key(user.gemini_api_key_vertexai_encrypted)
    else:
        masked_gemini_api_key_vertexai = '[未設定]'

    return render_template(
        "settings.html",
        user=user,
        masked_uwgen_api_key=masked_uwgen_api_key,
        masked_gemini_api_key=masked_gemini_api_key,
        masked_gemini_api_key_vertexai=masked_gemini_api_key_vertexai
    )

@root_bp.get("/image_gen")
def image_gen():
    """
    画像生成ページを表示するルート
    
    - GET: Geminiモデル一覧を取得し、フォームを表示する

    Returns
    -------
    str
        imaeg_gen.html テンプレートをレンダリングした HTML
        生成画像のパス、生成条件を含む
    """
    
    # 各種列挙体を取得
    gemini_models = ImageGenService.get_image_models()
    image_sizes = ImageGenService.get_resolutions()
    image_aspects = ImageGenService.get_aspects()
    image_safety_filters = ImageGenService.get_safety_filters()
    image_safety_levels = ImageGenService.get_safety_levels()
    
    # 変数初期化
    generated_paths: Optional[list[str]] = None
    error: Optional[str] = None
    
    return render_template(
        "image_gen.html", 
        generated=generated_paths, 
        models=gemini_models,
        resolutions=image_sizes,
        aspects=image_aspects,
        safety_filters=image_safety_filters,
        safety_levels=image_safety_levels,
        selected_model=GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value,
        selected_resolution=GeminiClient.ImageSize.ONE_K.value,
        selected_aspect=GeminiClient.AspectRatio.SQUARE.value,
        selected_safety_filter=GeminiClient.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.value,
        selected_safety_level=GeminiClient.SafetyFilterLevel.BLOCK_ONLY_HIGH.value,
        error=error
    )

@root_bp.get("/image_edit")
def image_edit():
    """
    画像編集ページを表示するルート
    
    - GET: Geminiモデル一覧を取得し、フォームを表示する

    Returns
    -------
    str
        imaeg_edit.html テンプレートをレンダリングした HTML
        編集画像のパス、生成条件を含む
    """
    
    # 各種列挙体を取得
    gemini_models = ImageGenService.get_image_models()
    image_sizes = ImageGenService.get_resolutions()
    image_aspects = ImageGenService.get_aspects()
    image_safety_filters = ImageGenService.get_safety_filters()
    image_safety_levels = ImageGenService.get_safety_levels()
    
    # 変数初期化
    error: Optional[str] = None
    
    return render_template(
        "image_edit.html", 
        models=gemini_models,
        resolutions=image_sizes,
        aspects=image_aspects,
        safety_filters=image_safety_filters,
        safety_levels=image_safety_levels,
        selected_model=GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value,
        selected_resolution=GeminiClient.ImageSize.ONE_K.value,
        selected_aspect=GeminiClient.AspectRatio.SQUARE.value,
        selected_safety_filter=GeminiClient.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.value,
        selected_safety_level=GeminiClient.SafetyFilterLevel.BLOCK_ONLY_HIGH.value,
        error=error
    )
    
@root_bp.route("/test", methods=["GET", "POST"])
def test():
    
    prompt:str = ""
    if request.method == "POST":
        data: Optional[dict[str, Any]] = request.json
        prompt = data.get("prompt", "Hello from Flask!") if data else ""
    else:
        prompt = "Hello from Flask!"
    
    return jsonify({
        "key1": "value1",
        "key2": "value2",
        "prompt": prompt
    })
