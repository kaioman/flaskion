from flask import Blueprint, render_template, jsonify, request
from typing import Any, Optional
from ..services.image_service import generate_image, get_models, get_resolutions, get_aspects, get_safety_filters, get_safety_levels

# Blueprint定義
root_bp = Blueprint('root', __name__)

@root_bp.route("/")
def index():
    """
    インデックスページを表示するルート 
    
    Returns
    -------
    str
        index.html テンプレートをレンダリングした HTML
    """
    return render_template("index.html")

@root_bp.route("/image_gen", methods=["GET", "POST"])
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
    gemini_models = get_models()
    image_sizes = get_resolutions()
    image_aspects = get_aspects()
    image_safety_filters = get_safety_filters()
    image_safety_levels = get_safety_levels()
    
    prompt: str = ""
    model: Optional[str] = None
    resolution: Optional[str] = None
    aspect: Optional[str] = None
    safety_filter: Optional[str] = None
    safety_level: Optional[str] = None
    generated_paths: Optional[list[str]] = None
    error: Optional[str] = None
    
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        model = request.form.get("model")
        resolution = request.form.get("resolution")
        aspect = request.form.get("aspect")
        safety_filter = request.form.get("safety_filter")
        safety_level = request.form.get("safety_level")
        if prompt:
            generated_paths = generate_image(prompt)
        else:
            error = "プロンプトを入力してください"

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
