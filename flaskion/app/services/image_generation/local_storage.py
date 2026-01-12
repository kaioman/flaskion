import uuid
import libcore_hng.utils.app_logger as app_logger
from flask import url_for
from datetime import date, datetime, timezone
from app.core.config import settings
from app.core.enums import ImagePathType
from app.services.image_generation.base import StorageStrategy

class LocalStorageStrategy(StorageStrategy):
    
    def __init__(self, current_user_id):
        """
        コンストラクタ
        """
        
        self.current_user_id = current_user_id
    
    def save(self, image_bytes_list, path_type: ImagePathType):
        """
        Uwgenに画像ファイルを保存する
        """
        
        # 日付フォルダ名取得
        date_dir = date.today().isoformat()

        # 出力先パス取得・作成
        MEDIA_DIR = self.get_image_path(path_type, date_dir, self.current_user_id)
        MEDIA_DIR.mkdir(parents=True, exist_ok=True)
        app_logger.info(f"[LocalStorageStrategy] Output directory prepared: {MEDIA_DIR}")

        # 画像ファイルを出力する
        filenames: list[str] = []
        for _, image_bytes in enumerate(image_bytes_list):
            filename = self.get_gen_filename()
            output_path = MEDIA_DIR / filename
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            filenames.append(filename)
            app_logger.info(f"[LocalStorageStrategy] Saved image: {filename}")

        # public URLに変換してリスト化する
        public_urls = [
            url_for("image_gen_api.get_image", path_type=path_type.value, date_dir=date_dir, image_id=image_id, _external=True)
            for image_id in filenames
        ]
        
        return {
            "type": "local",
            "filenames": public_urls
        }
        
    def get_gen_filename(self):
        """
        生成画像のファイル名を取得する
        """
        
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        unique = uuid.uuid4().hex
        return f"{timestamp}_{unique}.png"
    
    def get_image_path(self, path_type: ImagePathType, date_str: str, current_user_id):
        """
        画像ファイルパスを取得する
        """
        
        # ルートパス
        root_path = self.get_root_image_path(current_user_id)
        # 出力先パス構成
        if path_type == ImagePathType.GENERATED:
            return root_path / settings.GEN_IMAGE_DIR / date_str
        elif path_type == ImagePathType.EDITED:
            return root_path / settings.EDIT_IMAGE_DIR / date_str
        return root_path
    
    def get_root_image_path(self, current_user_id):
        """
        画像ファイルのルートパスを取得する
        """
        
        return settings.MEDIA_ROOT / str(current_user_id)
