import libcore_hng.utils.app_logger as app_logger
from typing import Dict, Any
from app.models.image_gen_params import ImageGenParams
from app.services.image_generation.image_generation_strategy import ImageGenerationStrategy
from app.services.image_generation.core_generate import CoreImageGenerator

class GeminiImageGenerationStrategy(ImageGenerationStrategy):
    """
    Gemini API を使用した画像生成ストラテジ
    
    既存の CoreImageGenerator をラップし、ImageGenerationStrategy インターフェースを実装
    """

    def __init__(self, project_id: str, location: str):
        """
        コンストラクタ
        
        Parameters
        ----------
        project_id : str
            VertexAI プロジェクトID
        location : str
            VertexAI ロケーション
        """
        self.project_id = project_id
        self.location = location
        app_logger.info("[GeminiImageGenerationStrategy] Initialized.")

    def generate(self, params: ImageGenParams, api_key: str) -> Dict[str, Any]:
        """
        Gemini API で画像生成を実行する
        
        Parameters
        ----------
        params : ImageGenParams
            画像生成パラメーター
        api_key : str
            復号化されたGemini APIキー
            
        Returns
        -------
        Dict[str, Any]
            生成結果
        """
        app_logger.info("[GeminiImageGenerationStrategy] Starting generation...")
        
        # CoreImageGenerator を初期化
        generator = CoreImageGenerator(
            api_key=api_key,
            project_id=self.project_id,
            location=self.location
        )
        
        response = generator.generate(params)
        app_logger.info("[GeminiImageGenerationStrategy] Generation completed.")
        return response
