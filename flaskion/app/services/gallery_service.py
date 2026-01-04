from flask import url_for
from app.core.config import settings
from app.core.enums import ImagePathType
from app.services.image_service import ImageGenService

class GalleryService:
    
    @staticmethod
    def get_user_images(current_user_id, filter_type, sort_order, offset=0, limit=20):
        
        # 画像保存ルートパス取得
        root_path = ImageGenService.get_root_image_path(current_user_id)
        
        targets = []
        if filter_type in ("all", ImagePathType.GENERATED.value):
            targets.append((ImagePathType.GENERATED.value, settings.GEN_IMAGE_DIR))
        if filter_type in ("all", ImagePathType.EDITED.value):
            targets.append((ImagePathType.EDITED.value, settings.EDIT_IMAGE_DIR))
            
        results = []
        
        for img_type, dir_name in targets:
            img_dir = root_path / str(dir_name)
            if not img_dir.exists():
                continue
            
            # 日付フォルダを走査
            for date_dir in sorted(img_dir.iterdir()):
                if not date_dir.is_dir():
                    continue
                
                for img_file in date_dir.iterdir():
                    if img_file.is_file():
                        public_url = url_for(
                            "image_gen_api.get_image",
                            path_type=img_type,
                            date_dir=date_dir.name,
                            image_id=img_file.name,
                            _external=False
                        )
                        results.append({
                            "path": public_url,
                            "type": img_type,
                            "date": date_dir.name,
                            "mtime": img_file.stat().st_mtime
                        })
        
        # ソート
        reverse = (sort_order == "newest")
        results.sort(
            key=lambda x: (x["date"], x["mtime"]), 
            reverse=reverse
        )
        
        # ページング
        paged = results[offset: offset + limit]
        
        return {
            "images": paged,
            "total": len(results)
        }