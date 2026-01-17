import uuid
import libcore_hng.utils.app_logger as app_logger
from typing import Type, TypeVar
from datetime import datetime, timezone
from http import HTTPStatus
from pydantic import ValidationError
from werkzeug.datastructures import FileStorage
from pycorex.gemini_client import GeminiClient
from pycorex.exceptions.no_candidates_error import NoCandidatesError
from app.core.config import settings
from app.core.enums import EncryptionKeyType, ImagePathType
from app.core.errors import ImageGenError, ImageEditError, ImageAnalyzeError
from app.models.image_gen_params import ImageGenParams
from app.models.image_edit_params import ImageEditParams
from app.models.image_analyze_params import ImageAnalyzeParams
from app.models.service_result import ParamsResult, AIServiceResult
from app.models.base_params import BaseParams
from app.models.base_image_params import BaseImageParams
from app.models.user import User
from app.services.encrypt_service import EncryptService
from app.services.image_generation.core_generate import CoreImageGenerator
from app.services.image_generation.core_edit import CoreImageEditor
from app.services.image_generation.core_analyze import CoreImageAnalyzer
from app.services.image_generation.base import StorageStrategy

T = TypeVar('T', bound=BaseParams)

class ImageGenService:

    @staticmethod
    def get_params(current_user: User, param_data: dict, param_class: Type[T]):
        """
        パラメーター取得/チェック
        """
        
        try:
            # フォームの入力値をパラメーターモデルクラスに設定する
            params = param_class(**param_data)
            app_logger.info(f"[ImageGenService] Parameters validated. prompt_length={len(params.prompt)}")
        except ValidationError:
            app_logger.error(f"[ImageGenService] Parameters validation failed. user_id={current_user.id}")
            return ParamsResult(
                params=None,
                decrypted_api_key=None,
                error_code=ImageGenError.INVALID_PARAMETER, 
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        # プロンプト入力チェック
        if not params.prompt:
            app_logger.warning(f"[ImageGenService] Missing prompt. user_id={current_user.id}")
            return ParamsResult(
                params=None,
                decrypted_api_key=None,
                error_code=ImageGenError.MISSING_PROMPT, 
                http_status=HTTPStatus.BAD_REQUEST
            )
        
        # 暗号化されたAPIキーを取得
        ciphertext = ""
        if isinstance(params, BaseImageParams):
            ciphertext = current_user.gemini_api_key_vertexai_encrypted
        else:
            ciphertext = current_user.gemini_api_key_encrypted
        
        if not ciphertext:
            app_logger.error(f"[ImageGenService] Missing API key. user_id={current_user.id}")
            return ParamsResult(
                params=None,
                decrypted_api_key=None,
                error_code=ImageGenError.MISSING_GEMINI_API_KEY, 
                http_status=HTTPStatus.BAD_REQUEST
            )
        
        # APIキーを復号する
        app_logger.info(f"[ImageGenService] Encrypted API key found. user_id={current_user.id}")
        api_key = ImageGenService.get_api_key(ciphertext)
        app_logger.info(f"[ImageGenService] API key decrypted. user_id={current_user.id}")
        
        # パラメーターを返す
        return ParamsResult(
            params=params,
            decrypted_api_key=api_key,
            error_code=None, 
            http_status=None
        )
        
    @staticmethod
    def generate_image(current_user: User, param_data: dict, storage_strategy: StorageStrategy):
        """
        画像生成メソッド
        """
        
        # 開始ログ
        app_logger.info(f"[ImageGenService] Start image generation. user_id={current_user.id}")

        # パラメーターを取得する
        params_result = ImageGenService.get_params(current_user, param_data, ImageGenParams)
        if not params_result.params:
            return params_result.error_code, params_result.http_status
        
        # 画像生成を実行
        try:
            generator = CoreImageGenerator(api_key=params_result.decrypted_api_key)
            image_bytes_list = generator.generate(params_result.params)
        except NoCandidatesError:
            return ImageGenError.IMAGE_NO_CANDIDATES, HTTPStatus.BAD_REQUEST
        except Exception:
            return ImageGenError.IMAGE_INTERNAL_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR
        
        # 生成結果を保存/取得
        save_result = storage_strategy.save(image_bytes_list, ImagePathType.GENERATED)
        app_logger.info(f"[ImageGenService] save_result generated. count={len(save_result)}")

        # 終了ログ
        app_logger.info(f"[ImageGenService] Completed successfully. user_id={current_user.id}")

        # 生成した画像のパスを返す
        return save_result, HTTPStatus.OK
    
    @staticmethod
    def edit_image(current_user: User, param_data: dict, source_image: FileStorage, storage_strategy: StorageStrategy):
        """
        画像編集メソッド
        """
        
        # 開始ログ
        app_logger.info(f"[ImageGenService] Start image edit. user_id={current_user.id}")

        # パラメーターを取得する
        params_result = ImageGenService.get_params(current_user, param_data, ImageEditParams)
        if not params_result.params:
            return params_result.error_code, params_result.http_status

        # 元画像入力チェック
        if not source_image:
            app_logger.warning(f"[ImageGenService] Missing source image file. user_id={current_user.id}")
            return ImageEditError.MISSING_SOURCE_IMAGE_NOT_FOUND, HTTPStatus.BAD_REQUEST
        
        # 画像編集を実行
        try:
            editor = CoreImageEditor(api_key=params_result.decrypted_api_key)
            image_bytes_list = editor.edit(params_result.params, source_image.stream)
        except NoCandidatesError:
            return ImageEditError.IMAGE_NO_CANDIDATES, HTTPStatus.BAD_REQUEST
        except Exception:
            return ImageEditError.EDIT_INTERNAL_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR
        
        # 生成結果を保存/取得
        save_result = storage_strategy.save(image_bytes_list, ImagePathType.EDITED)
        app_logger.info(f"[ImageGenService] save_result generated. count={len(save_result)}")
        
        # 終了ログ
        app_logger.info(f"[ImageGenService] Completed successfully. user_id={current_user.id}")

        # 生成した画像のパスを返す
        return save_result, HTTPStatus.OK
    
    @staticmethod
    def analyze_image(current_user: User, param_data: dict, source_image: FileStorage | bytes):
        """
        画像解析メソッド
        """
        
        # 開始ログ
        app_logger.info(f"[ImageGenService] Start image analyze. user_id={current_user.id}")

        # パラメーターを取得する
        params_result = ImageGenService.get_params(current_user, param_data, ImageAnalyzeParams)
        if not params_result.params:
            return AIServiceResult(
                result=None, 
                error_code=params_result.error_code,
                http_status=params_result.http_status
            )

        # 解析画像入力チェック
        if not source_image:
            app_logger.warning(f"[ImageGenService] Missing source image file. user_id={current_user.id}")
            return AIServiceResult(
                result=None, 
                error_code=ImageAnalyzeError.MISSING_SOURCE_IMAGE_NOT_FOUND, 
                http_status=HTTPStatus.BAD_REQUEST
            )
        
        # 画像解析を実行
        try:
            raw_bytes = source_image if isinstance(source_image, bytes) else source_image.stream.read()
            analyzer = CoreImageAnalyzer(api_key=params_result.decrypted_api_key)
            response = analyzer.analyze(params_result.params, raw_bytes)
        except Exception:
            return AIServiceResult(
                result=None, 
                error_code=ImageAnalyzeError.ANALYZE_INTERNAL_ERROR, 
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        
        # 終了ログ
        app_logger.info(f"[ImageGenService] Completed successfully. user_id={current_user.id}")

        # 画像解析リクエストのレスポンスを返す
        return AIServiceResult(
            result=response, 
            error_code=None, 
            http_status=HTTPStatus.OK
        )
    
    @staticmethod
    def get_gen_filename():
        """
        生成画像のファイル名を取得する
        """
        
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        unique = uuid.uuid4().hex
        return f"{timestamp}_{unique}.png"

    @staticmethod
    def get_root_image_path(current_user_id):
        """
        画像格納先ルートパスを取得する
        """
        
        return settings.MEDIA_ROOT / str(current_user_id)
    
    @staticmethod
    def get_image_path(path_type: str, date_str: str, current_user_id):
        """
        画像格納先パスを取得する
        """

        # ルートパス
        root_path = ImageGenService.get_root_image_path(current_user_id)
        # 出力先パス構成
        if path_type == ImagePathType.GENERATED.value:
            return root_path / settings.GEN_IMAGE_DIR / date_str
        elif path_type == ImagePathType.EDITED.value:
            return root_path / settings.EDIT_IMAGE_DIR / date_str
        return root_path
    
    @staticmethod
    def get_api_key(ciphertext):
        """
        暗号化されたキーを復号して取得する
        """
        
        return EncryptService.decrypt(
            ciphertext=ciphertext,
            key_type=EncryptionKeyType.GEMINI
        )
    
    @staticmethod
    def get_all_models():
        return GeminiClient.GeminiModel

    @staticmethod
    def get_image_models():
        return [
            GeminiClient.GeminiModel.GEMINI_PRO_VISION,
            GeminiClient.GeminiModel.GEMINI_2_5_FLASH_IMAGE,
            GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW
        ]

    @staticmethod
    def get_text_models():
        return [
            GeminiClient.GeminiModel.GEMINI_2_0_FLASH,
            GeminiClient.GeminiModel.GEMINI_2_0_FLASH_LITE,
            GeminiClient.GeminiModel.GEMINI_2_5_FLASH,
            GeminiClient.GeminiModel.GEMINI_2_5_FLASH_LITE,
            GeminiClient.GeminiModel.GEMINI_3_PRO,
            GeminiClient.GeminiModel.GEMINI_ULTRA,
        ]

    @staticmethod
    def get_resolutions():
        return GeminiClient.ImageSize

    @staticmethod
    def get_aspects():
        return GeminiClient.AspectRatio

    @staticmethod
    def get_safety_filters():
        return GeminiClient.HarmCategory

    @staticmethod
    def get_safety_levels():
        return GeminiClient.SafetyFilterLevel
