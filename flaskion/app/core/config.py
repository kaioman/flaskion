import os
from dotenv import load_dotenv
from dataclasses import dataclass

# .envファイルの内容を環境変数にロードする
load_dotenv()

@dataclass
class Settings:
    """
    設定クラス
    -  追加のアプリケーション設定はここに定義する
    -  このクラスは環境変数べースの設定値を一元管理する    
    """
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://uwgen:uwgen@uwgen_db:5432/uwgen_pg12")
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change_this_secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # デバッグモード
    DEBUG: bool = os.getenv("DEBUGPY", "false").lower() == "true"

# インスタンス生成
settings = Settings()
