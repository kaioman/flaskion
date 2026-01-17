from typing import Optional
from pycorex.gemini_client import GeminiClient
from app.models.base_params import BaseParams

class BaseImageParams(BaseParams):
    """
    画像生成/編集パラメーターモデル基底
    """
    
    resolution: Optional[GeminiClient.ImageSize] = None
    """ 解像度 """
    
    aspect: Optional[GeminiClient.AspectRatio] = None
    """ アスペクト比 """
    
    safety_filter: Optional[GeminiClient.HarmCategory] = None
    """ 安全フィルター """
    
    safety_level: Optional[GeminiClient.SafetyFilterLevel] = None
    """ 安全フィルターレベル """