import hashlib

class HashService:
    """
    文字列をハッシュ化・検証するサービス(SHA-256)
    """
    
    @staticmethod
    def hash_value(value: str) -> str:
        """
        値をSHA-256でハッシュ化して返す

        Parameters
        ----------
        value : str
            ハッシュ化する文字列

        Returns
        -------
        str
            ハッシュ化した値

        """
        
        if not isinstance(value, str):
            raise ValueError("value must be a string")
        
        return hashlib.sha256(value.encode("utf-8")).hexdigest()
    
    def verify(value: str, hashed_value: str) -> bool:
        """
        入力値がハッシュと一致するか検証する
        
        Parameters
        ----------
        value : str
            ハッシュ化する前の値
        value : str
            ハッシュ化した値
        
        Returns
        -------
        bool
            検証結果(True:一致,False:不一致)

        """
        
        # 検証値の型チェック
        if not isinstance(value, str) or not isinstance(hashed_value, str):
            return False
        
        # 検証結果を返す
        try:
            return hashlib.sha256(value.encode("utf-8")).hexdigest() == hashed_value
        except Exception:
            return False