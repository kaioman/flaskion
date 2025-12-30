from flask import Blueprint, request
from http import HTTPStatus
from app.core.security import get_current_user
from app.core.errors import UserError
from app.services.user_service import UserService
from app.models.response.success import SuccessResponse
from app.models.response.errors import ErrorResponse

bp = Blueprint("settings_api", __name__, url_prefix="/api/v1/settings")

@bp.post("/api-key/regenerate")
def renegerate_uwgen_api_key():
    """
    ログイン中ユーザーのUwgen APIキーを再発行する
    """
    
    # 認証チェック
    current_user, error, status = get_current_user()
    if error:
        return ErrorResponse.from_error(error, status)
    
    # Uwge APIキー発行
    new_key, error = UserService.generate_uwgen_api_key(current_user.id)
    if error == UserError.USER_NOT_FOUND:
        return ErrorResponse.from_error(UserError.USER_NOT_FOUND, HTTPStatus.NOT_FOUND)
    
    # レスポンス返却
    return SuccessResponse.ok(
        new_key,
        HTTPStatus.OK
    )
    
@bp.patch("")
def update_settings():
    """
    設定を保存する
    """
    
    # 認証チェック
    current_user, error, status = get_current_user()
    if error:
        return ErrorResponse.from_error(error, status)
    
    # リクエストデータ検証
    data = request.get_json() or {}
    
    # UserServiceで保存処理を実行
    error = UserService.update_settings(
        user=current_user,
        updates=data
    )
    
    # エラーコード判定
    if error:
        if error == UserError.USER_NOT_FOUND:
            return ErrorResponse.from_error(UserError.USER_NOT_FOUND, HTTPStatus.BAD_REQUEST)
        else:
            return ErrorResponse.from_error(error, HTTPStatus.INTERNAL_SERVER_ERROR)
    
    # レスポンス返却
    return SuccessResponse.ok(
        None,
        HTTPStatus.OK
    )