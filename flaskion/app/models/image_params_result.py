from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional
from app.models.base_image_params import BaseImageParams

@dataclass
class ImageParamsResult:
    
    params: Optional[BaseImageParams]
    """ 画像生成/編集パラメーターモデル """
    
    decrypted_api_key: Optional[str]
    """ 復号したAPIキー """
    
    error_code: Optional[str]
    """ エラーコード """
    
    http_status: Optional[HTTPStatus]
    """ HTTPステータス """