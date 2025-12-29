from libcore_hng.core.base_api_model import BaseApiModel
from typing import Optional

class ImageGenParams(BaseApiModel):
    """
    画像生成パラメーターモデルクラス
    
    画像生成処理に必要なパラメーターを保持するためのデータモデル
    
    Attributes
    ----------
    prompt : str
        生成する画像の内容を記述するプロンプト（必須）
    model : Optional[str]
        使用する生成モデル
    resolution : Optional[str]
        出力画像の解像度
    aspect : Optional[str]
        出力画像のアスペクト比
    safety_filter : Optional[str]
        適用する安全フィルターの種類
    safety_level : Optional[str]
        安全フィルターの強度レベル
    """
    
    prompt: str = ''
    """ プロンプト """
    
    model: Optional[str] = None
    """ モデル """
    
    resolution: Optional[str] = None
    """ 解像度 """
    
    ascpect: Optional[str] = None
    """ アスペクト比 """
    
    safety_filter: Optional[str] = None
    """ 安全フィルター """
    
    safety_level: Optional[str] = None
    """ 安全フィルターレベル """
