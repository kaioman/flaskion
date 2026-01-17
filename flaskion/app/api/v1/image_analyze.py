from flask import Blueprint, request
from http import HTTPStatus
from app.services.image_service import ImageGenService
from app.core.security import get_current_user
from app.models.response.errors import ErrorResponse
from app.models.response.success import SuccessResponse

bp = Blueprint("image_analyze_api", __name__, url_prefix="/api/v1")

@bp.post("/image_analyze")
def image_analyze():
    """
    画像解析エンドポイント
    """
    
    # 認証チェック
    auth = get_current_user()
    if auth.error_code:
        return ErrorResponse.from_error(auth.error_code, auth.http_status)
    
    # フォームデータ取得
    param_data: dict = request.form.to_dict()

    # 解析する画像を取得
    source_image = request.files.get("sourceImage")

    # ImageGenServiceで画像解析
    results, error_code, status = ImageGenService.analyze_image(
        current_user=auth.user,
        param_data=param_data,
        source_image=source_image
    )
    if status == HTTPStatus.OK:
        return SuccessResponse.ok(
            data={
                "generated": results["result"],
                "response_detail": results
            },
            status=status
        )
    else:
        return ErrorResponse.from_error(error_code, status)