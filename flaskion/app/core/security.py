import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

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