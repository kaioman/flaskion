from typing import Optional
from pycorex.gemini_client import GeminiClient
from app.models.base_params import BaseParams

class BaseImageParams(BaseParams):
    """
    画像生成/編集パラメーターモデル基底
    """
    
    resolution: Optional[GeminiClient.ImageSize] = GeminiClient.ImageSize.ONE_K
    """ 解像度 """
    
    aspect: Optional[GeminiClient.AspectRatio] = GeminiClient.AspectRatio.SQUARE
    """ アスペクト比 """
    
    safety_filter: Optional[GeminiClient.HarmCategory] = GeminiClient.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT
    """ 安全フィルター """
    
    safety_level: Optional[GeminiClient.SafetyFilterLevel] = GeminiClient.SafetyFilterLevel.BLOCK_ONLY_HIGH
    """ 安全フィルターレベル """