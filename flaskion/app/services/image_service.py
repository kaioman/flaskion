import uuid
import libcore_hng.utils.app_logger as app_logger
from datetime import datetime, timezone
from http import HTTPStatus
from flask import url_for
from pydantic import ValidationError
from PIL import Image as PIL_image
from werkzeug.datastructures import FileStorage
from datetime import date
from pycorex.gemini_client import GeminiClient
from pycorex.exceptions.no_candidates_error import NoCandidatesError
from app.core.config import settings
from app.core.enums import EncryptionKeyType, ImagePathType
from app.core.errors import ImageGenError, ImageEditError
from app.models.image_gen_params import ImageGenParams
from app.models.image_edit_params import ImageEditParams
from app.models.user import User
from app.services.encrypt_service import EncryptService

class ImageGenService:

    @staticmethod
    def generate_image(current_user: User, param_data: dict):
        
        app_logger.info(f"[ImageGenService] Start image generation. user_id={current_user.id}")

        try:
            # フォームの入力値をパラメーターモデルクラスに設定する
            params = ImageGenParams(**param_data)
            app_logger.info(f"[ImageGenService] Parameters validated. prompt_length={len(params.prompt)}")
        except ValidationError:
            app_logger.error(f"[ImageGenService] Parameters validation failed. user_id={current_user.id}")
            return ImageGenError.INVALID_PARAMETER, HTTPStatus.INTERNAL_SERVER_ERROR
        
        # プロンプト入力チェック
        if not params.prompt:
            app_logger.warning(f"[ImageGenService] Missing prompt. user_id={current_user.id}")
            return ImageGenError.MISSING_PROMPT, HTTPStatus.BAD_REQUEST
        
        # 暗号化されたAPIキーを取得
        ciphertext = current_user.gemini_api_key_vertexai_encrypted
        if not ciphertext:
            app_logger.error(f"[ImageGenService] Missing API key. user_id={current_user.id}")
            return ImageGenError.MISSING_GEMINI_API_KEY, HTTPStatus.BAD_REQUEST
        
        # APIキーを復号する
        app_logger.info(f"[ImageGenService] Encrypted API key found. user_id={current_user.id}")
        api_key = ImageGenService.get_api_key(ciphertext)
        app_logger.info(f"[ImageGenService] API key decrypted. user_id={current_user.id}")

        # GeminiClientを初期化
        client = GeminiClient(
            api_key=api_key
        )
        app_logger.info(f"[ImageGenService] GeminiClient initialized.")
        
        # 画像生成を実行
        try:
            app_logger.info(f"[ImageGenService] Generating image... user_id={current_user.id}")
            response = client.generate_image(
                prompt=params.prompt,
                model=params.model,
                aspect_ratio=params.aspect,
                image_size=params.resolution,
                harm_category = params.safety_filter,
                safety_filter_level = params.safety_level
            )
            app_logger.info(f"[ImageGenService] Image generation completed. result_count={len(response['result'])}")
            
        except NoCandidatesError as e:
            app_logger.error(e)
            return ImageGenError.IMAGE_NO_CANDIDATES, HTTPStatus.BAD_REQUEST
        except Exception as e:
            app_logger.error(e)
            return ImageGenError.IMAGE_INTERNAL_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR

        # 出力先パス取得・作成
        MEDIA_DIR = ImageGenService.get_image_path(ImagePathType.GENERATED.value, current_user.id)
        MEDIA_DIR.mkdir(parents=True, exist_ok=True)
        app_logger.info(f"[ImageGenService] Output directory prepared: {MEDIA_DIR}")
        
        # 画像ファイルを出力する
        results: list[str] = []
        for _, image_bytes in enumerate(response["result"]):
            filename = ImageGenService.get_gen_filename()
            output_path = MEDIA_DIR / filename
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            results.append(filename)
            app_logger.info(f"[ImageGenService] Saved image: {filename}")

        # public URLに変換してリスト化する
        public_urls = [
            url_for("image_gen_api.get_image", path_type=ImagePathType.GENERATED.value, image_id=image_id, _external=True)
            for image_id in results
        ]
        app_logger.info(f"[ImageGenService] Public URLs generated. count={len(public_urls)}")
        
        # 生成した画像のパスを返す
        app_logger.info(f"[ImageGenService] Completed successfully. user_id={current_user.id}")
        return public_urls, HTTPStatus.OK
    
    @staticmethod
    def edit_image(current_user: User, param_data: dict, source_image: FileStorage):
        
        app_logger.info(f"[ImageGenService] Start image edit. user_id={current_user.id}")

        try:
            # フォームの入力値をパラメーターモデルクラスに設定する
            params = ImageEditParams(**param_data)
            app_logger.info(f"[ImageGenService] Parameters validated. prompt_length={len(params.prompt)}")
        except ValidationError:
            app_logger.error(f"[ImageGenService] Parameters validation failed. user_id={current_user.id}")
            return ImageGenError.INVALID_PARAMETER, HTTPStatus.INTERNAL_SERVER_ERROR
        
        # プロンプト入力チェック
        if not params.prompt:
            app_logger.warning(f"[ImageGenService] Missing prompt. user_id={current_user.id}")
            return ImageGenError.MISSING_PROMPT, HTTPStatus.BAD_REQUEST
        
        # 元画像入力チェック
        if not source_image:
            app_logger.warning(f"[ImageGenService] Missing source image file. user_id={current_user.id}")
            return ImageEditError.MISSING_SOURCE_IMAGE_NOT_FOUND, HTTPStatus.BAD_REQUEST
        
        # 暗号化されたAPIキーを取得
        ciphertext = current_user.gemini_api_key_vertexai_encrypted
        if not ciphertext:
            app_logger.error(f"[ImageGenService] Missing API key. user_id={current_user.id}")
            return ImageGenError.MISSING_GEMINI_API_KEY, HTTPStatus.BAD_REQUEST
        
        # APIキーを復号する
        app_logger.info(f"[ImageGenService] Encrypted API key found. user_id={current_user.id}")
        api_key = ImageGenService.get_api_key(ciphertext)
        app_logger.info(f"[ImageGenService] API key decrypted. user_id={current_user.id}")

        # 元画像のバイナリデータを取得する
        base_image = PIL_image.open(source_image.stream)
        
        # GeminiClientを初期化
        client = GeminiClient(
            api_key=api_key
        )
        app_logger.info(f"[ImageGenService] GeminiClient initialized.")
        
        # 画像編集を実行
        try:
            app_logger.info(f"[ImageGenService] Editing image... user_id={current_user.id}")
            response = client.edit_image(
                prompt=params.prompt,
                model=params.model,
                base_image=base_image,
                aspect_ratio=params.aspect,
                image_size=params.resolution,
                harm_category = params.safety_filter,
                safety_filter_level = params.safety_level
            )
            app_logger.info(f"[ImageGenService] Image edit completed. result_count={len(response['result'])}")
            
        except NoCandidatesError as e:
            app_logger.error(e)
            return ImageGenError.IMAGE_NO_CANDIDATES, HTTPStatus.BAD_REQUEST
        except Exception as e:
            app_logger.error(e)
            return ImageGenError.IMAGE_INTERNAL_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR

        # 出力先パス取得・作成
        MEDIA_DIR = ImageGenService.get_image_path(ImagePathType.EDITED.value, current_user.id)
        MEDIA_DIR.mkdir(parents=True, exist_ok=True)
        app_logger.info(f"[ImageGenService] Output directory prepared: {MEDIA_DIR}")
        
        # 画像ファイルを出力する
        results: list[str] = []
        for _, image_bytes in enumerate(response["result"]):
            filename = ImageGenService.get_gen_filename()
            output_path = MEDIA_DIR / filename
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            results.append(filename)
            app_logger.info(f"[ImageGenService] Saved image: {filename}")

        # public URLに変換してリスト化する
        public_urls = [
            url_for("image_gen_api.get_image", path_type=ImagePathType.EDITED.value, image_id=image_id, _external=True)
            for image_id in results
        ]
        app_logger.info(f"[ImageGenService] Public URLs generated. count={len(public_urls)}")
        
        # 生成した画像のパスを返す
        app_logger.info(f"[ImageGenService] Completed successfully. user_id={current_user.id}")
        return public_urls, HTTPStatus.OK
    
    @staticmethod
    def get_gen_filename():
        """
        生成画像のファイル名を取得する
        """
        
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        unique = uuid.uuid4().hex
        return f"{timestamp}_{unique}.png"

    @staticmethod
    def get_image_path(path_type: str, current_user_id):
        # 日付フォルダ
        data_str = date.today().isoformat()
        # ルートパス
        root_path = settings.MEDIA_ROOT / str(current_user_id)
        # 出力先パス構成
        if path_type == ImagePathType.GENERATED.value:
            return root_path / settings.GEN_IMAGE_DIR / data_str
        elif path_type == ImagePathType.EDITED.value:
            return root_path / settings.EDIT_IMAGE_DIR / data_str
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
