from sqlalchemy import Column, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from pydbx_hng.models.base.base_model import Base

class User(Base):
    """
    ユーザー情報を管理するモデル
    
    - アプリケーション内でユーザー情報を扱うためのORMモデル
    - DBのテーブル構造をPythonクラスとして定義する
    """
    
    # テーブル名指定
    __tablename__ = "users"
    # スキーマ名指定
    __table_args__ = {"schema": "uwgen"}
    
    # 主キー(UUIDはDB側で自動生成)
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    # ログイン用メールアドレス(ユニーク制約あり)
    email = Column(
        String,
        nullable=False,
        unique=True
    )
    
    # パスワードハッシュ
    password_hash = Column(
        String,
        nullable=False
    )
    
    # アカウント有効フラグ
    is_active = Column(
        Boolean,
        nullable=False,
        server_default="true"
    )
    
    # 作成日時(デフォルトは現在時刻)
    create_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("NOW()")
    )
    
    # 更新日時(デフォルトは現在時刻)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("NOW()")
    )
    
    # 最終ログイン日時
    last_login_at = Column(
        TIMESTAMP(timezone=True)
    )
    
    # 暗号化されたGemini APIキー(任意)
    api_key_encrypted = Column(
        String
    )
    
    # APIキーの最終更新日時
    api_key_updated_at = Column(
        TIMESTAMP(timezone=True)
    )
