from flask import Blueprint
from app.core.security import get

bp = Blueprint("settings_api", __name__, url_prefix="/api/v1/settings")

@bp.route("/api-key/regenerate", method=["POST"])
def renegerate_uwgen_api_key():
    """
    ログイン中ユーザーのUwgen APIキーを再発行する
    """
    current_user = ""