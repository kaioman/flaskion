from flask import Blueprint, request, send_file
from http import HTTPStatus
from pathlib import Path
from app.services.image_service import ImageGenService
from app.core.security import get_current_user
from app.core.errors import ImageGenError
from app.core.enums import AuthType
from app.models.response.errors import ErrorResponse
from app.models.response.success import SuccessResponse
from app.services.image_generation.local_storage import LocalStorageStrategy
from app.services.image_generation.memory_storage import MemoryStorageStrategy

bp = Blueprint("image_gen_api", __name__, url_prefix="/api/v1")

@bp.post("/image_gen")
def image_gen():
    """
    画像生成エンドポイント
    """

    # 認証チェック
    auth = get_current_user()
    if auth.error_code:
        return ErrorResponse.from_error(auth.error_code, auth.http_status)
    
    # フォームデータ取得
    param_data: dict = request.get_json() or {}
    
    # クエリパラメーター判定(リクエスト元が外部APIかWebアプリか判定)
    if auth.auth_type == AuthType.API_KEY:
        storage = MemoryStorageStrategy()
    else:
        storage = LocalStorageStrategy(current_user_id=auth.user.id)
    
    # ImageGenServiceで画像生成
    results, status = ImageGenService.generate_image(
        current_user=auth.user,
        param_data=param_data,
        storage_strategy=storage
    )
    if status == HTTPStatus.OK:
        return SuccessResponse.ok(
            data={"generated": results},
            status=status
        )
    else:
        return ErrorResponse.from_error(results, status)

@bp.get("/images/<path_type>/<date_dir>/<image_id>")
def get_image(path_type: str, date_dir: str, image_id: str):
    """
    画像取得API
    """
    
    # 認証チェック
    auth = get_current_user()
    if auth.error_code:
        return ErrorResponse.from_error(auth.error_code, auth.http_status)

    # 保存先ディレクトリ取得
    user_dir = ImageGenService.get_image_path(path_type, date_dir, auth.user.id)

    # ユーザーディレクトリチェック
    if not user_dir.exists():
        return ErrorResponse.from_error(
            ImageGenError.FILE_NOT_FOUND,
            HTTPStatus.NOT_FOUND
        )
    
    # ファイルパス取得(パストラバーサル対策あり)
    try:
        file_path: Path = user_dir / image_id
        if user_dir not in file_path.resolve().parents:
            return ErrorResponse.from_error(
                ImageGenError.PATH_TRAVERSAL_DETECTED,
                HTTPStatus.FORBIDDEN
            )

    except Exception:
        return ErrorResponse.from_error(
            ImageGenError.PATH_TRAVERSAL_DETECTED,
            HTTPStatus.FORBIDDEN
        )
        
    # ファイル存在チェック
    if not file_path.is_file():
        return ErrorResponse.from_error(
            ImageGenError.FILE_NOT_FOUND,
            HTTPStatus.NOT_FOUND
        )
    
    # 画像を返却する
    response = send_file(file_path)
    response.headers["Cache-Control"]  ="public, max-age=3600"
    return response