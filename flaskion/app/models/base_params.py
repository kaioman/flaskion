from libcore_hng.core.base_api_model import BaseApiModel
from typing import Optional
from pycorex.gemini_client import GeminiClient

class BaseParams(BaseApiModel):
    """
    パラメーターモデル基底
    """
    
    prompt: str
    """ プロンプト """
    
    model: Optional[GeminiClient.GeminiModel] = None
    """ モデル """
