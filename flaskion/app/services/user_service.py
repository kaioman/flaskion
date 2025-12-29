from datetime import datetime, timezone
from app.models.user import User
from app.db.session import db
from app.core.security import generate_api_key_value
from app.core.errors import UserError
from app.db.transaction import transactional

class UserService:
    
    @staticmethod
    def generate_uwgen_api_key(email: str):
        """
        Uwgen独自のAPIキーを生成し、ユーザーに紐づけて保存する
        emailはunique前提
        
        Parameters
        ----------
        email : str
            Emailアドレス
            
        Returns
        -------
        tuple[str | None, UserError | None]
            (生成されたAPIキー、エラーコード)
        """

        # ユーザー情報取得
        user = db.query(User).filter_by(email=email).first()
        if not user:
            return None, UserError.USER_NOT_FOUND
        
        # APIキー生成
        new_key = generate_api_key_value()
        
        return new_key, None

    @staticmethod
    @transactional
    def update_settings(user: User, updates: dict):
        """
        ユーザー情報の部分更新を行う
        
        Parameters
        ----------
        user : User
            ユーザー情報
        updates : dict 
            更新対象dict
            
        Returns
        -------
        str 
            エラーコード(成功時はNone)
            
        Notes
        -----
        - updates: {"uwgen_api_key": "...", "gemini_api_key": "..."}
        """
        
        # ユーザー情報チェック
        if not user:
            return UserError.USER_NOT_FOUND
        
        # モデルから更新可能フィールド取得
        updatable_fields = {
            col.key
            for col in User.__table__.columns
            if col.info.get("updatable")
        }
        
        # updatesのキーと照合して更新
        for key, value in updates.items():
            if key in updatable_fields and value is not None:
                setattr(user, key, value)
        
        # Uwgen APIキーに変更があれば変更日時を更新する
        if updates.get("uwgen_api_key_changed"):
            user.uwgen_api_key_updated_at = datetime.now(timezone.utc)

        # Gemini APIキーに変更があれば変更日時を更新する
        if updates.get("gemini_api_key_changed"):
            user.gemini_api_key_updated_at = datetime.now(timezone.utc)
        
        # DBに反映
        db.commit()
        db.refresh(user)
        
        return None