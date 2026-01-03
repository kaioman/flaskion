from enum import Enum

class EncryptionKeyType(Enum):
    """
    秘密鍵の種類(Fernet)
    """
    
    GEMINI = "gemini"
    """ GEMINI """
    
    UWGEN = "uwgen"
    """ UWGEN """
    
class ImagePathType(Enum):
    """
    画像出力先パス種類
    """
    
    GENERATED = "gen"
    """ 画像生成 """
    
    EDITED = "edit"
    """ 画像編集 """