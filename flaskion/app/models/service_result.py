from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional, Any
from app.models.base_params import BaseParams

@dataclass
class ParamsResult:
    
    params: Optional[BaseParams]
    """ パラメーターモデル """

    decrypted_api_key: Optional[str]
    """ 復号したAPIキー """
    
    error_code: Optional[str]
    """ エラーコード """
    
    http_status: Optional[HTTPStatus]
    """ HTTPステータス """

@dataclass
class AIServiceResult:
    
    result: Optional[Any]
    """ 処理結果 """

    error_code: Optional[str]
    """ エラーコード """
    
    http_status: Optional[HTTPStatus]
    """ HTTPステータス """