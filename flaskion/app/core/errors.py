from enum import Enum
from typing import Dict, TypeVar, Generic

# Generic 型変数
#E = TypeVar("E", bound="BaseErrorEnum")

class BaseErrorEnum(str, Enum):
    """
    エラーコードとメッセージを一元管理するための基底クラス
    各派生クラスは messages 辞書を定義すること
    """

    # 派生クラス側で上書きされる
    messages: Dict["BaseErrorEnum", str] = {}
    
    @property
    def message(self) -> str:
        """
        Enum メンバーに対応するメッセージを返す
        派生クラス側で messages 辞書を定義する必要がある
        """
        return self.messages[self]
    
class AuthError(BaseErrorEnum):
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
    
    messages = {
        EMAIL_EXISTS: "This email is already registered.",
        INVALID_CREDENTIALS: "Invalid email or password.",
        INACTIVE_ACCOUNT: "Account is inactive.",
        WEAK_PASSWORD: "The provided password is too weak.",    
    }
    """ メッセージ定義 """

class RequestError(BaseErrorEnum):
    """
    リクエスト処理で発生するエラーコード一覧
    """
    
    INVALID_REQUEST = "invalid_request"
    """ リクエスト無効 """
    
    messages = {
        INVALID_REQUEST: "The request payload is invalid.",
    }
    """ メッセージ定義 """