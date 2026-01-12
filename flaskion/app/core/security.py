import bcrypt
import jwt
import secrets
from flask import request, session
from http import HTTPStatus
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.errors import UserError
from app.core.enums import AuthType
from app.models.user import User
from app.models.current_user_result import CurrentUserResult
from app.db.session import db
from app.services.hash_service import HashService

def hash_password(password: str) -> str:
    """
    bcryptを使ってパスワードのハッシュを生成する

    Parameters
    ----------
    
    password : str
        平文パスワード
    
    Returns
    -------
    str
        ハッシュ化されたパスワード
    """
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    bcryptを使ってパスワードの検証を行う

    Parameters
    ----------
    
    password : str
        平文パスワード
    
    hashed_password : str
        ハッシュ化されたパスワード
        
    Returns
    -------
    bool
        パスワードが一致する場合はTrue、一致しない場合はFalse
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(payload: dict) -> str:
    """
    JWTアクセストークンを生成する

    - 有効期限(exp)はUTCのUNIXタイムスタンプで付与する
    - payloadは破壊的に変更しない（副作用防止）

    Parameters
    ----------

    payload : dict
        トークンに含めるデータ

    Returns
    -------
    str
        JWTアクセストークン
    """
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 副作用回避のため、新しいdictを作成
    payload = {**payload, "exp": int(expire.timestamp())}
    
    token: str = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token

def generate_api_key_value() -> str:
    """
    暗号学的に安全なAPIキーを生成する
    
    Returns
    -------
    str
        生成されたAPIキー
    """
    return secrets.token_urlsafe(32)

def generate_api_key_hash(api_key) -> str:
    """
    APIキーをハッシュ化する
    
    Parameters
    ----------

    api_key : str
        ハッシュ化するAPIキー

    Returns
    -------
    str
        ハッシュ化されたAPIキー
    """
    return HashService.hash_value(api_key)

def decode_access_token(token: str):
    """
    JWTアクセストークンをデコードしてpayloadを返す
    
    Parameters
    ----------
    
    token : str
        JWTアクセストークン
        
    Returns
    -------
    Any
        Payload
    """
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        # トークン期限切れ
        raise
    except InvalidTokenError:
        # 不正なトークン
        raise
    
def get_current_user():
    """
    AuthorizationヘッダーからJWTを取得し、
    デコードしてユーザー情報を返す
    
    - トークンが無い、無効なトークン、ユーザーが存在しない
    - 上記いずれかの場合はNoneを返す
    """
    
    # 1. セッション認証(HTMLページ用)
    current_user_id = session.get("id")
    if current_user_id:
        user = db.query(User).filter_by(id=current_user_id).first()
        if user:
            return CurrentUserResult(
                user=user,
                auth_type=AuthType.SESSION,
                error_code=None,
                http_status=None
            )
    
    # 2. JWT認証
    # Authorizationヘッダーを取得する
    auth_header = request.headers.get("Authorization")
    # ヘッダーの存在、ヘッダーに"Bearer "を含むか(Bearerは大文字小文字を許容)
    if auth_header and auth_header.lower().startswith("bearer "):
    
        # アクセストークン取得
        parts = auth_header.split()
        if len(parts) == 2:            
            token = parts[1]
            try:
                payload = decode_access_token(token)
                
                # ユーザーID取得
                user_id = payload.get("sub")
                if user_id:
                    return CurrentUserResult(
                        user=db.query(User).filter_by(id=user_id).first(),
                        auth_type=AuthType.JWT,
                        error_code=None,
                        http_status=None
                    )
            
            except Exception as e:
                print(f"[decode_access_token] Invalid token: {e}")
                return CurrentUserResult(
                    user=None, 
                    auth_type=None,
                    error_code=UserError.INVALID_ACCESS_TOKEN, 
                    http_status=HTTPStatus.UNAUTHORIZED
                )
    
    # 3. APIキー認証
    # Authorizationヘッダーを取得する
    auth_header = request.headers.get("Authorization")
    # ヘッダーの存在、ヘッダーに"Uwgen "を含むか(Uwgenは大文字小文字を許容)
    if auth_header and auth_header.lower().startswith("uwgen "):
        
        # APIキー取得
        api_key = auth_header.split()[1]
        hashed_api_key = HashService.hash_value(api_key)
        user = user=db.query(User).filter_by(uwgen_api_key=hashed_api_key).first()
        if user:
            return CurrentUserResult(
                user=user,
                auth_type=AuthType.API_KEY,
                error_code=None,
                http_status=None
            )
    
    # 認証失敗
    return CurrentUserResult(
        user=None, 
        auth_type=None,
        error_code=UserError.AUTH_HEADER_MISSING, 
        http_status=HTTPStatus.UNAUTHORIZED
    )

def get_user_from_session():
    """
    セッションからユーザーIDを取得し、ユーザー情報を返す
    
    Returns
    -------
    User
        ユーザー情報
    """
    
    id = session.get("id")
    if not id:
        return None
    return db.query(User).filter_by(id=id).first()
    
def mask_api_key(key: str | None) -> str:
    """
    指定されたAPIキーをマスクして返す
    
    Parameters
    ----------
    key : str
        マスクするAPIキー
    
    Returns
    -------
    str
        マスクされたAPIキー
    """
    if not key:
        return ""
    return "*" * 40 + key[-4:]
