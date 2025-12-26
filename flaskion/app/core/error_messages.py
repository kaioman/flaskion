from .errors import AuthError, RequestError

AUTH_ERROR_MESSAGES = {
    AuthError.EMAIL_EXISTS: "This email is already registered.",
    AuthError.INVALID_CREDENTIALS: "Invalid email or password.",
    AuthError.INACTIVE_ACCOUNT: "Account is inactive.",
    AuthError.WEAK_PASSWORD: "The provided password is too weak.",
}

REQUEST_ERROR_MESSAGE = {
    RequestError.INVALID_REQUEST: "The request payload is invalid.",
}

def get_error_message(err):

    # AuthErrorの場合
    if isinstance(err, AuthError):
        return AUTH_ERROR_MESSAGES.get(err, "Unknown authentication error")
    
    # RequestErrorの場合
    if isinstance(err, RequestError):
        return REQUEST_ERROR_MESSAGE.get(err, "Unknown request error")
    
    # その他エラー
    return "Unknown error"