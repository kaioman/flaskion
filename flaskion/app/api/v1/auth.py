from flask import Blueprint, request, jsonify
from app.schemas.auth import (
    SignupRequestSchema, SignupResponseSchema,
    SigninRequestSchema, SigninResponseSchema
)
from app.services.auth_service import AuthService

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
        return jsonify({"errors": "invalid_request", "message": errors}), 400
    
    # サインアップ処理
    user, err = AuthService.signup(data["email"], data["password"])
    if err == "email_exists":
        return jsonify({"errors": "email_exists", "message": "This email is already registered."}), 409
    
    # レスポンス生成
    response = SignupResponseSchema().dump(user)
    return jsonify(response), 201

@bp.post("/signin")
def signin():
    """
    ユーザーサインインAPI
    """
    
    # リクエストデータ検証
    data = request.get_json()
    errors = SigninRequestSchema().validate(data)
    if errors:
        return jsonify({"errors": "invalid_request", "message": errors}), 400

    # サインイン処理
    token, err = AuthService.signin(data["email"], data["password"])
    if err == "invalid_credentials":
        return jsonify({"errors": "invalid_credentials", "message": "Invalid email or password."}), 401
    if err == "inactive_account":
        return jsonify({"errors": "inactive_account", "message": "Account is inactive."}), 403
    
    # レスポンス生成
    response = SigninResponseSchema().dump({
        "access_token": token,
        "token_type": "Bearer"
    })
    return jsonify(response), 200