from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional
from app.models.base_params import BaseParams

@dataclass
class BaseParamsResult:
    
    params: Optional[BaseParams]
    """ パラメーターモデル """

    decrypted_api_key: Optional[str]
    """ 復号したAPIキー """
    
    error_code: Optional[str]
    """ エラーコード """
    
    http_status: Optional[HTTPStatus]
    """ HTTPステータス """