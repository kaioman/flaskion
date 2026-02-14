import libcore_hng.utils.app_logger as app_logger
from pycorex.gemini_client import GeminiClient
from app.models.image_analyze_params import ImageAnalyzeParams

class CoreImageAnalyzer:
    """
    画像解析のコア処理を担当する
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
        app_logger.info(f"[CoreImageAnalyzer] GeminiClient initialized.")
        
    def analyze(self, params: ImageAnalyzeParams, image_bytes):
        """
        画像解析処理を実行する
        
        Parameters
        ----------
        params : ImageAnalyzeParams
            画像解析パラメーターモデル
        image_bytes : bytes
            画像ファイル(bytes)
        Returns
        -------
        dict[str, Any]
            画像解析リクエストレスポンス
        """
    
        try:
            # 画像解析を実行する
            app_logger.info(f"[CoreImageAnalyzer] Analyzing image... ")
            response = self.client.analyze_image(
                base_image=image_bytes,
                prompt=params.prompt,
                model=params.model
            )
            app_logger.info(f"[CoreImageAnalyzer] Image analyze completed. result_count={len(response['result'])}")
            return response
        
        except Exception as e:
            app_logger.error(e)
            raise e
