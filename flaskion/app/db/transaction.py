import functools
from app.db.session import db

def transactional(func):
    """
    サービス層メソッドのトランザクション制御デコレーター
    
    - メソッド内で例外が発生した場合のみrollbackを実行する
    - commitはメソッド内で行う
    - rollbackが失敗しても元の例外を優先して送出する
    """
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 例外発生時はトランザクションを破棄
            try:
                db.rollback()
            except Exception:
                # rollbackが失敗しても例外を上書きしない
                pass
            raise e
    return wrapper