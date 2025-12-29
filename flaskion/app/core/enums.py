from enum import Enum

class EncryptionKeyType(Enum):
    """
    秘密鍵の種類(Fernet)
    """
    
    GEMINI = "gemini"
    """ GEMINI """
    
    UWGEN = "uwgen"
    """ UWGEN """