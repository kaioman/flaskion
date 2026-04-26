import libcore_hng.utils.app_logger as app_logger
from pycorex.gemini_client import GeminiClient
from pycorex.exceptions.no_candidates_error import NoCandidatesError
from app.models.image_gen_params import ImageGenParams

class CoreImageGenerator:
    """
    Gemini画像生成のコア処理を担当する
    """

    def __init__(self, api_key, project_id, location):
        """
        コンストラクタ
        
        Parameters
        ----------
        api_key : str
            外部生成モデルにアクセスするためのAPIキー
        project_id : str
            プロジェクトID(Vertexai)
        location : str
            ロケーション(Vertexai)
        """
        # GeminiClientを初期化
        self.client = GeminiClient(api_key=api_key, project_id=project_id, location=location)
        app_logger.info(f"[CoreImageGenerator] GeminiClient initialized.")
        
    def generate(self, params: ImageGenParams):
        """
        画像生成処理を実行する
        
        Parameters
        ----------
        params : ImageGenParams
            画像生成パラメーターモデル
            
        Returns
        -------
        List[bytes]
            生成された画像データのバイト列リスト
        """
    
        try:
            app_logger.info(f"[CoreImageGenerator] Generating image... ")
            response = self.client.generate_image(
                prompt=params.prompt,
                model=params.model,
                aspect_ratio=params.aspect,
                image_size=params.resolution,
                harm_category = params.safety_filter,
                safety_filter_level = params.safety_level
            )
            app_logger.info(f"[CoreImageGenerator] Image generation completed. result_count={len(response['result'])}")
            return response
        
        except NoCandidatesError as e:
            app_logger.error(e)
            raise e
        except Exception as e:
            app_logger.error(e)
            raise e
