from .errors import AuthError, RequestError, UserError, ImageGenError

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

IMAGE_GEN_ERROR_MESSAGE = {
    ImageGenError.MISSING_PROMPT: "プロンプトが指定されていません",
    ImageGenError.INVALID_PARAMETER: "パラメーターが不正です",
    ImageGenError.MISSING_GEMINI_API_KEY: "Gemini(VertexAI) APIキーが未設定です",
    ImageGenError.FILE_NOT_FOUND: "画像ファイルが見つかりません",
    ImageGenError.PATH_TRAVERSAL_DETECTED: "不正なパスが指定されました",
    ImageGenError.IMAGE_NO_CANDIDATES: "画像を生成できませんでした。プロンプトを変えて再度実行してください",
    ImageGenError.IMAGE_INTERNAL_ERROR: "画像生成中に予期しないエラーが発生しました。時間をおいて再度実行してください"
}
""" 画像生成処理系エラーメッセージ """

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

    # ImageGenErrorの場合
    if isinstance(err, ImageGenError):
        return IMAGE_GEN_ERROR_MESSAGE.get(err, "Unknown user error")
    
    # その他エラー
    return "Unknown error"