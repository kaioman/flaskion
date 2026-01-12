import libcore_hng.utils.app_logger as app_logger
from PIL import Image as PIL_image
from pycorex.gemini_client import GeminiClient
from pycorex.exceptions.no_candidates_error import NoCandidatesError
from app.models.image_edit_params import ImageEditParams

class CoreImageEditor:
    """
    画像編集のコア処理を担当する
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
        app_logger.info(f"[CoreImageEditor] GeminiClient initialized.")
        
    def edit(self, params: ImageEditParams, stream):
        """
        画像編集処理を実行する
        
        Parameters
        ----------
        params : ImageEditParams
            画像編集パラメーターモデル
        stream : IO[bytes]
            ファイルストリーム
        Returns
        -------
        List[bytes]
            生成された画像データのバイト列リスト
        """
    
        try:
            # 元画像のバイナリデータを取得する
            base_image = PIL_image.open(stream)

            # 画像編集を実行する
            app_logger.info(f"[CoreImageEditor] Editing image... ")
            response = self.client.edit_image(
                prompt=params.prompt,
                model=params.model,
                base_image=base_image,
                aspect_ratio=params.aspect,
                image_size=params.resolution,
                harm_category = params.safety_filter,
                safety_filter_level = params.safety_level
            )
            app_logger.info(f"[CoreImageEditor] Image edit completed. result_count={len(response['result'])}")
            return response["result"]
        
        except NoCandidatesError as e:
            app_logger.error(e)
            raise e
        except Exception as e:
            app_logger.error(e)
            raise e
