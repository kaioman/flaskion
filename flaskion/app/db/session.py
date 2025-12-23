from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
#from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from app.core.config import settings
#from pydbx_hng.models.base.base_model import BaseModel

# Base class for models
#Base = DeclarativeBase()
#class BaseModel(DeclarativeBase):
#    pass

# データベースエンジン
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# セッションメーカー
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# スレッドローカルなセッション
db = scoped_session(SessionLocal)

# def init_db():
#     """
#     データベース初期化
#     - 必要なテーブルを作成する
#     """
    
#     # モデルをimportしてBaseに登録
#     import app.models.user # noqa: F401
#     BaseModel.metadata.create_all(bind=engine)
    
#     print("Database initialized.")