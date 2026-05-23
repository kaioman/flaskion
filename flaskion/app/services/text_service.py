import libcore_hng.utils.app_logger as app_logger
from typing import Type, TypeVar
from http import HTTPStatus
from pydantic import ValidationError
from pycorex.gemini_client import GeminiClient
from app.core.enums import EncryptionKeyType
from app.core.errors import TextGenError
from app.models.text_gen_params import TextGenParams
from app.models.service_result import ParamsResult, AIServiceResult
from app.models.base_params import BaseParams
from app.models.user import User
from app.services.encrypt_service import EncryptService
from app.services.text_generation.gemini_generate import GeminiTextGenerator

T = TypeVar('T', bound=BaseParams)

class TextGenService:

    @staticmethod
    def get_params(current_user: User, param_data: dict, param_class: Type[T]):
        """
        パラメーター取得/チェック
        """
        
        try:
            # フォームの入力値をパラメーターモデルクラスに設定する
            params = param_class(**param_data)
            app_logger.info(f"[TextGenService] Parameters validated. prompt_length={len(params.prompt)}")
        except ValidationError:
            app_logger.error(f"[TextGenService] Parameters validation failed. user_id={current_user.id}")
            return ParamsResult(
                params=None,
                decrypted_api_key=None,
                error_code=TextGenError.INVALID_PARAMETER, 
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        # プロンプト入力チェック
        if not params.prompt:
            app_logger.warning(f"[TextGenService] Missing prompt. user_id={current_user.id}")
            return ParamsResult(
                params=None,
                decrypted_api_key=None,
                error_code=TextGenError.MISSING_PROMPT, 
                http_status=HTTPStatus.BAD_REQUEST
            )
        
        # 暗号化されたAPIキーを取得
        ciphertext = current_user.gemini_api_key_encrypted
        
        if not ciphertext:
            app_logger.error(f"[TextGenService] Missing API key. user_id={current_user.id}")
            return ParamsResult(
                params=None,
                decrypted_api_key=None,
                error_code=TextGenError.MISSING_GEMINI_API_KEY, 
                http_status=HTTPStatus.BAD_REQUEST
            )
        
        # APIキーを復号する
        app_logger.info(f"[TextGenService] Encrypted API key found. user_id={current_user.id}")
        api_key = TextGenService.get_api_key(ciphertext)
        app_logger.info(f"[TextGenService] API key decrypted. user_id={current_user.id}")
        
        # パラメーターを返す
        return ParamsResult(
            params=params,
            decrypted_api_key=api_key,
            error_code=None, 
            http_status=None
        )
        
    @staticmethod
    def generate_text(current_user: User, param_data: dict):
        """
        テキスト生成メソッド
        """
        
        # 開始ログ
        app_logger.info(f"[TextGenService] Start text generation. user_id={current_user.id}")

        # パラメーターを取得する
        params_result = TextGenService.get_params(current_user, param_data, TextGenParams)
        if not params_result.params:
            return AIServiceResult(
                result=None,
                error_code=params_result.error_code, 
                http_status=params_result.http_status
            )
        
        # テキスト生成を実行
        try:
            generator = GeminiTextGenerator(api_key=params_result.decrypted_api_key)
            response = generator.generate(params_result.params)
        except Exception as e:
            # エラーログ出力
            app_logger.error(e)
            
            return AIServiceResult(
                result=None,
                error_code=TextGenError.TEXT_GEN_INTERNAL_ERROR, 
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        # 終了ログ
        app_logger.info(f"[TextGenService] Completed successfully. user_id={current_user.id}")

        # 生成した画像のパスを返す
        return AIServiceResult(
            result=response,
            error_code=None, 
            http_status=HTTPStatus.OK
        )
        
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
    def get_text_models():
        return [
            GeminiClient.GeminiModel.GEMINI_2_0_FLASH,
            GeminiClient.GeminiModel.GEMINI_2_0_FLASH_LITE,
            GeminiClient.GeminiModel.GEMINI_2_5_FLASH,
            GeminiClient.GeminiModel.GEMINI_2_5_FLASH_LITE,
            GeminiClient.GeminiModel.GEMINI_3_PRO,
            GeminiClient.GeminiModel.GEMINI_ULTRA,
        ]
