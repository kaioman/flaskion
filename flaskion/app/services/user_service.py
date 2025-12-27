from datetime import datetime, timezone
from app.models.user import User
from app.db.session import db
from app.core.security import generate_api_key_value
from app.core.errors import UserError
from app.db.transaction import transactional

class UserService:
    
    @staticmethod
    @transactional
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
        
        # 更新
        user.uwgen_api_key = new_key
        user.uwgen_api_key_updated_at = datetime.now(timezone.utc)
        
        # DB反映
        db.commit()
        db.refresh(user)
        
        return new_key, None
