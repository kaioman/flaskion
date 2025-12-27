import bcrypt
import jwt
import secrets
from flask import request
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.models.user import User
from app.db.session import db

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
    
    # Authorizationヘッダーを取得する
    auth_header = request.headers.get("Authorization")
    # ヘッダーの存在、ヘッダーに"Bearer "を含むか(Bearerは大文字小文字を許容)
    if not auth_header or not auth_header.lower().startswith("bearer "):
        return None
    
    # アクセストークン取得
    parts = auth_header.split()
    if len(parts) != 2:
        return None
    token = parts[1]
    try:
        payload = decode_access_token(token)
    except Exception as e:
        print(f"[decode_access_token] Invalid token: {e}")
        return None
    
    # ユーザーID取得    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    # ユーザー情報を返す
    return db.query(User).filter_by(id=user_id).first()