from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.core.config import settings

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
