import libcore_hng.utils.app_logger as app_logger
from typing import Dict, Any
from app.models.comfyui_image_gen_params import ComfyUIImageGenParams
from app.services.image_generation.image_generation_strategy import ImageGenerationStrategy
from app.services.image_generation.comfyui_generate import ComfyUIImageGenerator
from pycorex.exceptions.no_candidates_error import NoCandidatesError
from pycorex.exceptions.comfyui_exceptions import ComfyUIAPIError


class ComfyUIImageGenerationStrategy(ImageGenerationStrategy):
    """
    ComfyUI API を使用した画像生成ストラテジ
    
    ComfyUIサーバーのREST APIを叩いて画像生成を実行
    """

    def __init__(self, api_url: str, timeout_seconds: int, polling_interval: int):
        """
        コンストラクタ
        
        Parameters
        ----------
        api_url : str
            ComfyUI APIのベースURL (例: http://localhost:8188)
        timeout_seconds : int
            ComfyUI APIのタイムアウト設定
        polling_interval : int
            ComfyUI APIの生成画像取得間隔
        """
        self.api_url = api_url.rstrip('/')
        self.timeout_seconds = timeout_seconds
        self.polling_interval = polling_interval
        app_logger.info(f"[ComfyUIImageGenerationStrategy] Initialized with URL: {self.api_url}")
        app_logger.info(f"[ComfyUIImageGenerationStrategy] Initialized with Timeout seconds: {self.timeout_seconds}")
        app_logger.info(f"[ComfyUIImageGenerationStrategy] Initialized with Poling interval: {self.polling_interval}")

    def generate(self, params: ComfyUIImageGenParams, _: str) -> Dict[str, Any]:
        """
        ComfyUI API で画像生成を実行する
        
        Parameters
        ----------
        params : ComfyUIImageGenParams
            画像生成パラメーター
        api_key : str
            未使用（ローカルComfyUIはAPIキー不要）
            
        Returns
        -------
        Dict[str, Any]
            生成結果
            {
                'result': List[bytes],  # 生成画像のバイト列リスト
                'model': str,  # 使用したモデル情報
            }
            
        Raises
        ------
        NoCandidatesError
            API呼び出しがエラーの場合（Gemini互換のエラーハンドリング）
        """
        
        try:
            app_logger.info(
                f"[ComfyUIImageGenerationStrategy] Starting generation... "
                f"rating_level={params.rating_level}, batch_size={params.batch_size}"
            )

            # CoreImageGenerator を初期化
            generator = ComfyUIImageGenerator(
                base_url=self.api_url,
                timeout_seconds=self.timeout_seconds,
                polling_interval=self.polling_interval
            )
            
            # 生成処理を実行
            response = generator.generate(params)
            app_logger.info("[ComfyUIImageGenerationStrategy] Generation completed.")
            
            # 実行結果を返す
            return response
        except NoCandidatesError as e:
            error_msg = f"{str(e)}"
            app_logger.error(f"[ComfyUIImageGenerationStrategy] {error_msg}")
            raise NoCandidatesError(error_msg)            
        except ComfyUIAPIError as e:
            error_msg = f"Unexpected error in ComfyUI generation: {str(e)}"
            app_logger.error(f"[ComfyUIImageGenerationStrategy] {error_msg}")
            raise ComfyUIAPIError(error_msg)
