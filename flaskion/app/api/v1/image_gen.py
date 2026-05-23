import os
import libcore_hng.utils.app_logger as app_logger
from flask import Blueprint, request, send_file
from http import HTTPStatus
from pathlib import Path
from app.services.image_service import ImageGenService
from app.core.security import get_current_user
from app.core.errors import ImageGenError
from app.core.enums import AuthType
from app.models.response.errors import ErrorResponse
from app.models.response.success import SuccessResponse
from app.models.image_gen_params import ImageGenParams
from app.models.comfyui_image_gen_params import ComfyUIImageGenParams
from app.services.image_generation.local_storage import LocalStorageStrategy
from app.services.image_generation.memory_storage import MemoryStorageStrategy
from app.services.image_generation.gemini_strategy import GeminiImageGenerationStrategy
from app.services.image_generation.comfyui_strategy import ComfyUIImageGenerationStrategy

bp = Blueprint("image_gen_api", __name__, url_prefix="/api/v1")

@bp.post("/image_gen")
def image_gen():
    """
    画像生成エンドポイント
    
    リクエストボディに以下を指定：
    - provider: "gemini" または "comfyui" (デフォルト: "gemini")
    - その他の生成パラメーター（providerに応じて異なる）
    
    ComfyUIの例：
    {
        "provider": "comfyui",
        "workflow_json": {...},
        "batch_size": 1,
        "rating_level": 2
    }
    """

    # 認証チェック
    auth = get_current_user()
    if auth.error_code:
        return ErrorResponse.from_error(auth.error_code, auth.http_status)
    
    # フォームデータ取得
    param_data: dict = request.get_json() or {}
    
    # プロバイダー判定
    provider = param_data.pop('provider', 'gemini').lower()
    
    # ストレージストラテジを決定（認証タイプによる）
    if auth.auth_type == AuthType.API_KEY:
        storage = MemoryStorageStrategy()
    else:
        storage = LocalStorageStrategy(current_user_id=auth.user.id)
    
    # プロバイダー別に生成戦略を構築
    try:
        if provider == 'comfyui':
            # ComfyUIストラテジ（APIキー不要）
            param_class = ComfyUIImageGenParams
            generation_strategy = ComfyUIImageGenerationStrategy(
                api_url=os.getenv("COMFYUI_API_URL", "http://host.docker.internal:8188"),
                timeout_seconds=os.getenv("TIMEOUT_SECONDS", 120),
                polling_interval=os.getenv("POLLING_INTERVAL", 1)
            )
        elif provider == 'gemini':
            # Geminiストラテジ（デフォルト）
            param_class = ImageGenParams
            generation_strategy = GeminiImageGenerationStrategy(
                project_id=os.getenv("VERTEXAI_PROJECT_ID"),
                location=os.getenv("VERTEXAI_LOCATION")
            )
        else:
            return ErrorResponse.from_error(
                ImageGenError.INVALID_PARAMETER,
                HTTPStatus.BAD_REQUEST
            )
    except Exception as e:
        app_logger.error(f"[image_gen] Strategy initialization failed: {str(e)}")
        return ErrorResponse.from_error(
            ImageGenError.IMAGE_INTERNAL_ERROR,
            HTTPStatus.INTERNAL_SERVER_ERROR
        )
    
    # ImageGenServiceで画像生成
    response = ImageGenService.generate_image(
        current_user=auth.user,
        param_data=param_data,
        storage_strategy=storage,
        generation_strategy=generation_strategy,
        param_class=param_class
    )
    
    if response.http_status == HTTPStatus.OK:
        return SuccessResponse.ok(
            data={"generated": response.result["save_result"]},
            status=response.http_status
        )
    else:
        return ErrorResponse.from_error(response.error_code, response.http_status)

@bp.get("/images/<path_type>/<date_dir>/<image_id>")
def get_image(path_type: str, date_dir: str, image_id: str):
    """
    画像取得API
    """
    
    # 認証チェック
    auth = get_current_user()
    if auth.error_code:
        return ErrorResponse.from_error(auth.error_code, auth.http_status)

    # 保存先ディレクトリ取得
    user_dir = ImageGenService.get_image_path(path_type, date_dir, auth.user.id)

    # ユーザーディレクトリチェック
    if not user_dir.exists():
        return ErrorResponse.from_error(
            ImageGenError.FILE_NOT_FOUND,
            HTTPStatus.NOT_FOUND
        )
    
    # ファイルパス取得(パストラバーサル対策あり)
    try:
        file_path: Path = user_dir / image_id
        if user_dir not in file_path.resolve().parents:
            return ErrorResponse.from_error(
                ImageGenError.PATH_TRAVERSAL_DETECTED,
                HTTPStatus.FORBIDDEN
            )

    except Exception:
        return ErrorResponse.from_error(
            ImageGenError.PATH_TRAVERSAL_DETECTED,
            HTTPStatus.FORBIDDEN
        )
        
    # ファイル存在チェック
    if not file_path.is_file():
        return ErrorResponse.from_error(
            ImageGenError.FILE_NOT_FOUND,
            HTTPStatus.NOT_FOUND
        )
    
    # 画像を返却する
    response = send_file(file_path)
    response.headers["Cache-Control"]  ="public, max-age=3600"
    return response