from flask import Blueprint, request, session
from http import HTTPStatus
from app.schemas.auth import (
    SignupRequestSchema, SignupResponseSchema,
    SigninRequestSchema, SigninResponseSchema
)
from app.services.auth_service import AuthService
from app.core.security import get_current_user
from app.core.errors import AuthError, RequestError
from app.models.response.errors import ErrorResponse
from app.models.response.success import SuccessResponse

# Blueprintの作成
bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@bp.post("/signup")
def signup():
    """
    ユーザーサインアップAPI
    """
    
    # リクエストデータ検証
    data = request.get_json()
    errors = SignupRequestSchema().validate(data)
    if errors:
        return ErrorResponse.from_error(RequestError.INVALID_REQUEST, HTTPStatus.BAD_REQUEST, details=errors)

    # サインアップ処理
    user, err = AuthService.signup(data["email"], data["password"])
    if err == AuthError.EMAIL_EXISTS:
        return ErrorResponse.from_error(AuthError.EMAIL_EXISTS, HTTPStatus.CONFLICT)

    # レスポンス生成
    return SuccessResponse.ok(
        SignupResponseSchema().dump(user),
        status=HTTPStatus.CREATED
    )
    
@bp.post("/signin")
def signin():
    """
    ユーザーサインインAPI
    """
    
    # リクエストデータ検証
    data = request.get_json() or {}
    errors = SigninRequestSchema().validate(data)
    if errors:
        return ErrorResponse.from_error(RequestError.INVALID_REQUEST, HTTPStatus.BAD_REQUEST, details=errors)

    # サインイン処理
    user ,token, err = AuthService.signin(data["email"], data["password"])
    if err == AuthError.INVALID_CREDENTIALS:
        return ErrorResponse.from_error(AuthError.INVALID_CREDENTIALS, HTTPStatus.UNAUTHORIZED)
    if err == AuthError.INACTIVE_ACCOUNT:
        return ErrorResponse.from_error(AuthError.INACTIVE_ACCOUNT, HTTPStatus.FORBIDDEN)

    # セッションにidとEmailアドレスをセットする
    session["id"] = user.id
    session["email"] = user.email
    
    # レスポンス生成
    return SuccessResponse.ok(
        SigninResponseSchema().dump({
            "access_token": token,
            "token_type": "Bearer"
        })
    )
    
@bp.get("/me")
def get_me():
    """
    カレントユーザーを返すエンドポイント
    - 認証済み -> 200 + ユーザー情報
    - 未認証 -> 400
    """
    
    # 認証チェック
    current_user, error, status = get_current_user()
    if error:
        return ErrorResponse.from_error(error, status)
    
    # 認証済み
    return SuccessResponse.ok(
        data = {
            "id": current_user.id,
            "email": current_user.email
        },
        status=HTTPStatus.OK
    )