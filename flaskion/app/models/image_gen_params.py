from libcore_hng.core.base_api_model import BaseApiModel
from typing import Optional
from pycorex.gemini_client import GeminiClient

class ImageGenParams(BaseApiModel):
    """
    画像生成パラメーターモデルクラス
    
    - 画像生成処理に必要なパラメーターを保持するためのデータモデル
    
    """
    
    prompt: str
    """ プロンプト """
    
    model: Optional[GeminiClient.GeminiModel] = None
    """ モデル """
    
    resolution: Optional[GeminiClient.ImageSize] = None
    """ 解像度 """
    
    aspect: Optional[GeminiClient.AspectRatio] = None
    """ アスペクト比 """
    
    safety_filter: Optional[GeminiClient.HarmCategory] = None
    """ 安全フィルター """
    
    safety_level: Optional[GeminiClient.SafetyFilterLevel] = None
    """ 安全フィルターレベル """
