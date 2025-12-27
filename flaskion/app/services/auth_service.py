from datetime import datetime, timezone
from app.models.user import User
from app.db.session import db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import AuthError

class AuthService:
    
    @staticmethod
    def signup(email: str, password: str):
        """
        ユーザーのサインアップ処理
        
        Parameters
        ----------
    
        email : str
            ユーザーのメールアドレス
        password : str
            ユーザーのパスワード
        """
        
        # email重複チェック
        existing = db.query(User).filter_by(email=email).first()
        
        if existing:
            return None, AuthError.EMAIL_EXISTS
        
        # ハッシュパスワード生成
        password_hashed = hash_password(password)
        
        # ユーザー作成
        now = datetime.now(timezone.utc)
        user = User(
            email=email,
            password_hash=password_hashed,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user, None
    
    @staticmethod
    def signin(email: str, password: str):
        """
        ユーザーのサインイン処理
        
        email : str
            ユーザーのメールアドレス
        password : str
            ユーザーのパスワード
        """
        
        # ユーザー情報取得
        user = db.query(User).filter_by(email=email).first()
        
        # ユーザー存在チェック
        if not user:
            return None, AuthError.INVALID_CREDENTIALS
        
        # パスワード検証
        if not verify_password(password, user.password_hash):
            return None, AuthError.INVALID_CREDENTIALS
        
        # アカウント有効チェック
        if not user.is_active:
            return None, AuthError.INACTIVE_ACCOUNT
        
        # トークン生成
        token = create_access_token({"sub": str(user.id)})
        
        # 最終ログイン日時更新
        user.last_login_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
        
        # ユーザーModel, トークン返却
        return user, token, None