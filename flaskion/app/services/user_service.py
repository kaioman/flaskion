from datetime import datetime, timezone
from app.models.user import User
from app.db.session import db
from app.core.security import generate_api_key_value
from app.core.errors import UserError
from app.db.transaction import transactional
from app.services.encrypt_service import EncryptService

class UserService:
    
    @staticmethod
    def generate_uwgen_api_key(id: str):
        """
        Uwgen独自のAPIキーを生成し、ユーザーに紐づけて保存する
        emailはunique前提
        
        Parameters
        ----------
        id : str
            ユーザーID
            
        Returns
        -------
        tuple[str | None, UserError | None]
            (生成されたAPIキー、エラーコード)
        """

        # ユーザー情報取得
        user = db.query(User).filter_by(id=id).first()
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
                column = User.__table__.columns.get(key)
                if column.info.get("encrypt"):
                    key_type = column.info.get("key")
                    value = EncryptService.encrypt(value, key_type)
                
                setattr(user, key, value)
        
        # Uwgen APIキーに変更があれば変更日時を更新する
        if updates.get("uwgen_api_key_changed"):
            user.uwgen_api_key_updated_at = datetime.now(timezone.utc)

        # Gemini APIキーに変更があれば変更日時を更新する
        if updates.get("gemini_api_key_changed"):
            user.gemini_api_key_updated_at = datetime.now(timezone.utc)

        # Gemini(VertexAI) APIキーに変更があれば変更日時を更新する
        if updates.get("gemini_api_key_vertexai_changed"):
            user.gemini_api_key_vertexai_updated_at = datetime.now(timezone.utc)
        
        # DBに反映
        db.commit()
        db.refresh(user)
        
        return None