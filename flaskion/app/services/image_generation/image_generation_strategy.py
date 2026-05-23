from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models.image_gen_params import ImageGenParams

class ImageGenerationStrategy(ABC):
    """
    画像生成プロバイダーの抽象インターフェース
    
    異なるAI画像生成サービス（Gemini、ComfyUI等）を統一的に扱うためのStrategyパターン
    """

    @abstractmethod
    def generate(self, params: ImageGenParams, api_key: str) -> Dict[str, Any]:
        """
        画像生成を実行する
        
        Parameters
        ----------
        params : ImageGenParams
            画像生成パラメーター
        api_key : str
            復号化されたAPIキー
            
        Returns
        -------
        Dict[str, Any]
            生成結果を含む辞書
            {
                'result': List[bytes],  # 生成画像のバイト列リスト
                'model': str,  # 使用したモデル情報
            }
        """
        pass
