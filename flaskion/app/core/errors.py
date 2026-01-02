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
    
    AUTH_HEADER_MISSING = "auth_header_missing"
    """ Authorizationヘッダーが存在しない/不正 """
    
    INVALID_ACCESS_TOKEN = "invalid_access_token"
    """ アクセストークンが不正 """

    USER_UNAUTHORIZED = "user_unauthorized"
    """ 認証されていないユーザー """
    
    USER_NOT_FOUND = "user_not_found"
    """ ユーザーが見つからない """
    
    INVALID_API_KEY = "invalid_api_key"
    """ APIキーが無効 """

class ImageGenError(Enum):
    """
    画像生成処理で発生するエラーコード一覧
    """
    
    MISSING_PROMPT = "missing_prompt"
    """ プロンプトが指定されていない """
    
    INVALID_PARAMETER = "invalid_parameter"
    """ パラメーター不正 """
    
    MISSING_GEMINI_API_KEY = "missing_gemini_api_key"
    """ GeminiAPIキーが未設定 """
    
    FILE_NOT_FOUND = "file_not_found"
    """ 画像ファイルが見つからない """
    
    PATH_TRAVERSAL_DETECTED = "path_traversal_detected"
    """ パストラバーサル対策が検出された """
    
    IMAGE_NO_CANDIDATES = "image_no_candidates"
    """ 画像を生成できませんでした。プロンプトを変えて再度実行してください """
    
    IMAGE_INTERNAL_ERROR = "image_internal_error"
    """ 画像生成中に予期しないエラーが発生しました。時間をおいて再度実行してください """
    
class ImageEditError(Enum):
    """
    画像編集処理で発生するエラーコード一覧
    """
    
    MISSING_SOURCE_IMAGE_NOT_FOUND = "missing_source_image_not_found"
    """ 元画像ファイルが指定されていない """
    