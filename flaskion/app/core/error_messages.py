from .errors import AuthError, RequestError, UserError

AUTH_ERROR_MESSAGES = {
    AuthError.EMAIL_EXISTS: "入力されたEmailアドレスは既に登録されています",
    AuthError.INVALID_CREDENTIALS: "Emailアドレスまたはパスワードが間違っています",
    AuthError.INACTIVE_ACCOUNT: "このアカウントは無効です",
    AuthError.WEAK_PASSWORD: "パスワード強度が低すぎます",
}
""" 認証系レスポンスエラーメッセージ """

REQUEST_ERROR_MESSAGE = {
    RequestError.INVALID_REQUEST: "リクエストの内容が不正です",
}
""" リクエスト系エラーメッセージ """

USER_ERROR_MESSAGE = {
    UserError.AUTH_HEADER_MISSING: "Authorizationヘッダーが存在しない、または不正です",
    UserError.INVALID_ACCESS_TOKEN: "アクセストークンが不正です",
    UserError.USER_UNAUTHORIZED: "ユーザーが認証されていません",
    UserError.USER_NOT_FOUND: "ユーザーが見つかりません",
    UserError.INVALID_API_KEY: "APIキーが無効です",
}
""" ユーザー情報登録系エラーメッセージ """

def get_error_message(err) -> str:
    """
    エラーレスポンスクラスごとにメッセージを取得する
    
    Parameters
    ----------
    err : Enum
        エラーレスポンスEnum
    
    Returns
    -------
    str
        エラーメッセージ
    """
    
    # AuthErrorの場合
    if isinstance(err, AuthError):
        return AUTH_ERROR_MESSAGES.get(err, "Unknown authentication error")
    
    # RequestErrorの場合
    if isinstance(err, RequestError):
        return REQUEST_ERROR_MESSAGE.get(err, "Unknown request error")

    # UserErrorの場合
    if isinstance(err, UserError):
        return USER_ERROR_MESSAGE.get(err, "Unknown user error")
    
    # その他エラー
    return "Unknown error"