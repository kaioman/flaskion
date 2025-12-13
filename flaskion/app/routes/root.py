from flask import Blueprint, render_template, jsonify, request
from typing import Any, Optional

root_bp = Blueprint('root', __name__)

@root_bp.route("/")
def index():
    return render_template("index.html")

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
