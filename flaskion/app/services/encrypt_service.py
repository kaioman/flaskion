import os
from cryptography.fernet import Fernet
from app.core.enums import EncryptionKeyType

class EncryptService:
    """
    カラムごとに異なる暗号鍵を使い分ける暗号化サービス
    """
    
    _ciphers = {
        EncryptionKeyType.GEMINI: Fernet(os.environ["GEMINI_KEY_SECRET"]),
        EncryptionKeyType.UWGEN: Fernet(os.environ["UWGEN_KEY_SECRET"]),
    }
    
    @classmethod
    def encrypt(cls, plaintext: str, key_type: EncryptionKeyType) -> str:
        """
        指定されたkey_typeの値で暗号化する
        
        Parameters
        ----------
        plaintext : str
            暗号化する対象文字列(平文)
        key_type : str
            暗号鍵タイプ
        
        Returns
        -------
        str
            暗号化された文字列
        """
        
        cipher = cls._ciphers[key_type]
        return cipher.encrypt(plaintext.encode()).decode()
    
    @classmethod
    def decrypt(cls, ciphertext: str, key_type: EncryptionKeyType) -> str:
        """
        指定されたkey_typeの値で復号する
        
        Parameters
        ----------
        ciphertext : str
            暗号化された文字列
        key_type : str
            暗号鍵タイプ
        
        Returns
        -------
        str
            復号化された暗号化文字列
        """

        cipher = cls._ciphers[key_type]
        return cipher.decrypt(ciphertext.encode()).decode()