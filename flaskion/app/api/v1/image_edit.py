
from flask import Blueprint, request
from http import HTTPStatus
from app.services.image_service import ImageGenService
from app.core.security import get_current_user
from app.core.enums import AuthType
from app.models.response.errors import ErrorResponse
from app.models.response.success import SuccessResponse
from app.services.image_generation.local_storage import LocalStorageStrategy
from app.services.image_generation.memory_storage import MemoryStorageStrategy

bp = Blueprint("image_edit_api", __name__, url_prefix="/api/v1")

@bp.post("/image_edit")
def image_edit():
    """
    画像編集エンドポイント
    """
    
    # 認証チェック
    auth = get_current_user()
    if auth.error_code:
        return ErrorResponse.from_error(auth.error_code, auth.http_status)
    
    # フォームデータ取得
    param_data: dict = request.form.to_dict()

    # クエリパラメーター判定(リクエスト元が外部APIかWebアプリか判定)
    if auth.auth_type == AuthType.API_KEY:
        storage = MemoryStorageStrategy()
    else:
        storage = LocalStorageStrategy(current_user_id=auth.user.id)
    
    # 元画像を取得
    source_image = request.files.get("sourceImage")
    
    # ImageGenServiceで画像編集
    response = ImageGenService.edit_image(
        current_user=auth.user,
        param_data=param_data,
        source_image=source_image,
        storage_strategy=storage
    )
    if response.http_status == HTTPStatus.OK:
        return SuccessResponse.ok(
            data={"generated": response.result["save_result"]},
            status=response.http_status
        )
    else:
        return ErrorResponse.from_error(response.error_code, response.http_status)
