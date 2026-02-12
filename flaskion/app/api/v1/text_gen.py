from flask import Blueprint, request
from http import HTTPStatus
from app.services.text_service import TextGenService
from app.core.security import get_current_user
from app.models.response.errors import ErrorResponse
from app.models.response.success import SuccessResponse

bp = Blueprint("text_gen_api", __name__, url_prefix="/api/v1")

@bp.post("/text_gen")
def text_gen():
    """
    テキスト生成エンドポイント
    """

    # 認証チェック
    auth = get_current_user()
    if auth.error_code:
        return ErrorResponse.from_error(auth.error_code, auth.http_status)
    
    # jsonデータ取得
    param_data: dict = request.get_json() or {}
    
    # TextGenServiceでテキスト生成
    response = TextGenService.generate_text(
        current_user=auth.user,
        param_data=param_data
    )
    if response.http_status == HTTPStatus.OK:
        return SuccessResponse.ok(
            data={"generated": response.result},
            status=response.http_status
        )
    else:
        return ErrorResponse.from_error(response.error_code, response.http_status)
