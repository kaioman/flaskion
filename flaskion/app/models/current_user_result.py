from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional
from app.core.enums import AuthType
from app.models.user import User

@dataclass
class CurrentUserResult:
    
    user: Optional[User]
    """ ユーザー情報モデル """
    
    auth_type: Optional[AuthType]
    """ 認証方式 """
    
    error_code: Optional[str]
    """ エラーコード """
    
    http_status: Optional[HTTPStatus]
    """ HTTPステータス """