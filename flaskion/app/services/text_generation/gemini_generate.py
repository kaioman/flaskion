import libcore_hng.utils.app_logger as app_logger
from pycorex.gemini_client import GeminiClient
from app.models.text_gen_params import TextGenParams

class GeminiTextGenerator:
    """
    テキスト生成のコア処理を担当する
    """

    def __init__(self, api_key):
        """
        コンストラクタ
        
        Parameters
        ----------
        api_key : str
            外部生成モデルにアクセスするためのAPIキー
        """
        # GeminiClientを初期化
        self.client = GeminiClient(api_key=api_key)
        app_logger.info(f"[GeminiTextGenerator] GeminiClient initialized.")
        
    def generate(self, params: TextGenParams):
        """
        テキスト生成処理を実行する
        
        Parameters
        ----------
        params : TextGenParams
            テキスト生成パラメーターモデル
            
        Returns
        -------
        dict[str, Any]
            テキスト生成リクエストレスポンス
        """
    
        try:
            app_logger.info(f"[GeminiTextGenerator] Generating text... ")
            response = self.client.generate_text(
                prompt=params.prompt,
                model=params.model,
            )
            app_logger.info(f"[GeminiTextGenerator] Text generation completed. result_count={len(response['result'])}")
            return response
        
        except Exception as e:
            app_logger.error(e)
            raise e
