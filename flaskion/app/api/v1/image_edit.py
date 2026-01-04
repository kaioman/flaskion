
from flask import Blueprint, request
from http import HTTPStatus
from app.services.image_service import ImageGenService
from app.core.security import get_current_user
from app.models.response.errors import ErrorResponse
from app.models.response.success import SuccessResponse

bp = Blueprint("image_edit_api", __name__, url_prefix="/api/v1")

@bp.post("/image_edit")
def image_edit():
    """
    画像編集エンドポイント
    """
    
    # 認証チェック
    current_user, error, status = get_current_user()
    if error:
        return ErrorResponse.from_error(error, status)
    
    # フォームデータ取得
    param_data: dict = request.form.to_dict()

    # 元画像を取得
    source_image = request.files.get("sourceImage")
    
    # ImageGenServiceで画像編集
    results, status = ImageGenService.edit_image(
        current_user=current_user,
        param_data=param_data,
        source_image=source_image
    )
    if status == HTTPStatus.OK:
        return SuccessResponse.ok(
            data={"generated": results},
            status=status
        )
    else:
        return ErrorResponse.from_error(results, status)
