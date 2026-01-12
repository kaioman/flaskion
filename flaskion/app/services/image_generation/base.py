from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.core.enums import ImagePathType

class StorageStrategy(ABC):
    
    @abstractmethod
    def save(self, image_bytes_liset: List[bytes], path_type: ImagePathType) -> Dict[str, Any]:
        pass