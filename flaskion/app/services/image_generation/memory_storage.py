import base64
from app.services.image_generation.base import StorageStrategy
from app.core.enums import ImagePathType

class MemoryStorageStrategy(StorageStrategy):
    def save(self, image_bytes_list, path_type: ImagePathType):
        
        base64_images = [
            base64.b64encode(img_bytes).decode("utf-8")
            for img_bytes in image_bytes_list
        ]
        
        return {
            "type": "memory",
            "images": base64_images
        }