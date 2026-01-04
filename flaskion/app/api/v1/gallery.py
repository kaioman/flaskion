from flask import Blueprint, request
from http import HTTPStatus
from app.core.security import get_current_user
from app.models.response.errors import ErrorResponse
from app.services.gallery_service import GalleryService
from app.models.response.success import SuccessResponse

bp = Blueprint("gallery_api", __name__, url_prefix="/api/v1")

@bp.get("/gallery")
def get_gallery():
    """
    ギャラリー画像一覧取得
    """
    
    # 認証チェック
    current_user, error, status = get_current_user()
    if error:
        return ErrorResponse.from_error(error, status)

    # クエリパラメーター
    filter_type = request.args.get("type", "all")
    sort_order = request.args.get("sort", "newest")
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=20, type=int)
    
    # 画像取得サービス呼び出し
    results = GalleryService.get_user_images(
        current_user_id=current_user.id,
        filter_type=filter_type,
        sort_order=sort_order,
        offset=offset,
        limit=limit
    )
    
    return SuccessResponse.ok(
        data={
            "images": results["images"], 
            "total": results["total"],
        },
        status=HTTPStatus.OK
    )