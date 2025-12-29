from enum import Enum
from typing import Protocol

class ErrorEnumProtocol(Protocol):
    """
    エラー用Enumが満たすべきインターフェースを定義するProtocol
    このProtocolはエラーコードを表すEnumが必ず以下2つの属性を
    持つことを保証する
    
    Attributes
    ----------
    value : str
        Enum メンバーの識別子（エラーコード）。通常は文字列
    message : str
        エラーコードに対応するユーザー向けメッセージ
        
    Notes
    -----
    - このProtocolは継承される必要はない
        AuthErrorやRequestErrorはこのProtocolを継承しなくても
        `value`と`message`を持っていれば自動的に適合する
    - これにより、ErrorResponseなどの関数は「valueとmessageを持つもの」
        という契約に基づいて型安全に動作可能
    """
    
    # Enumメンバーの値（エラーコード）
    value: str
    
    # エラーコードに対応するメッセージ
    message: str

class AuthError(Enum):
    """
    認証系で発生するエラーコード一覧
    """
    
    EMAIL_EXISTS = "email_exists"
    """ メールアドレスが既に存在する """

    INVALID_CREDENTIALS = "invalid_credentials"
    """ 認証情報が無効 """
    
    INACTIVE_ACCOUNT = "inactive_account"
    """ アカウントが無効 """

    WEAK_PASSWORD = "weak_password"
    """ パスワードが弱すぎる """
    
class RequestError(Enum):
    """
    リクエスト処理で発生するエラーコード一覧
    """
    
    INVALID_REQUEST = "invalid_request"
    """ リクエスト無効 """
    
class UserError(Enum):
    """
    ユーザー情報登録処理で発生するエラーコード一覧
    """
    
    AUTH_HEADER_MISSING = "auht_header_missing"
    """ Authorizationヘッダーが存在しない/不正 """
    
    INVALID_ACCESS_TOKEN = "invalid_access_token"
    """ アクセストークンが不正 """

    USER_UNAUTHORIZED = "user_unauthorized"
    """ 認証されていないユーザー """
    
    USER_NOT_FOUND = "user_not_found"
    """ ユーザーが見つからない """
    
    INVALID_API_KEY = "invalid_api_key"
    """ APIキーが無効 """
    