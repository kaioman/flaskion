from flask import Blueprint, render_template, jsonify, request
from typing import Any, Optional
from pydantic import ValidationError
from ..services import image_service as img_srv

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

@root_bp.get("/image_gen")
def image_gen():
    """
    画像生成ページを表示するルート
    
    - GET: Geminiモデル一覧を取得し、フォームを表示する
    - POST: フォームから送信された生成条件に基づき、画像生成処理を行い結果を表示する

    Returns
    -------
    str
        imaeg_gen.html テンプレートをレンダリングした HTML
        生成画像のパス、生成条件を含む
    """
    
    # 各種列挙体を取得
    gemini_models = img_srv.get_image_models()
    image_sizes = img_srv.get_resolutions()
    image_aspects = img_srv.get_aspects()
    image_safety_filters = img_srv.get_safety_filters()
    image_safety_levels = img_srv.get_safety_levels()
    
    # 変数初期化
    model: Optional[str] = None
    resolution: Optional[str] = None
    aspect: Optional[str] = None
    safety_filter: Optional[str] = None
    safety_level: Optional[str] = None
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
        selected_model=model,
        selected_resolution=resolution,
        selected_aspect=aspect,
        selected_safety_filter=safety_filter,
        selected_safety_level=safety_level,
        error=error
    )

@root_bp.route("/get_gen_image", methods=["POST"])
def get_gen_image():
    """
    画像生成エンドポイント
    """
    if request.method == "POST":
        
        try:

            # フォームの入力値をパラメーターモデルクラスに設定する
            param_data: dict = request.get_json()
            
        except ValidationError as e:
            return jsonify({"error": e.errors() }), img_srv.HTTPStatus.BAD_REQUEST
        
        # 生成結果(画像パス)をJSONで返す
        return img_srv.generate_image(param_data)

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
