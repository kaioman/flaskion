import os
import sys
import time
from flask import Flask, redirect, g
from flask_socketio import SocketIO
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver
from app.routes import register_routes
from app.core.config import settings
from app.core.logging import init_logging
from app.core.security import get_current_user
from app.core.version import APP_VERSION
from app.db.session import db
from app.models.current_user_result import AuthType

# FlaskアプリケーションとSocketIOの初期化
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# Flask Secret-Keyを設定
app.config["SECRET_KEY"] = settings.SECRET_KEY

# ロガーを初期化する
init_logging()

@app.before_request
def load_user():
    """
    リクエストごとにユーザーをロードする
    """
    
    auth = get_current_user()
    g.current_user = auth.user
    g.auth_type = auth.auth_type
    
    # AuthTypeがNoneの場合は終了
    if not auth.auth_type:
        return
    
    # APIはセッション不要
    if auth.auth_type == AuthType.API_KEY:
        return
    
    # JWTはセッション必須
    if auth.auth_type != AuthType.SESSION:
        return redirect("/signin")
    
@app.context_processor
def inject_user():
    """
    テンプレートに current_userを注入
    """
    return dict(current_user=g.get("current_user"), app_version=APP_VERSION)

@app.teardown_request
def shutdown_session(exception=None):
    """
    リクエスト終了時にSQLAlchemyのセッションをクリーンアップする
    
    Parameters
    ----------
    exception : Exception | None
        リクエスト処理中に発生した例外
    """
    db.remove()

# ルートを登録
register_routes(app)

class ReloadHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            # 少し待機
            time.sleep(1)
            # コンソールに変更検知を表示
            print(f"🔄 ソースコード変更検知: {event.src_path} | タイプ: {event.event_type}  再起動します...")
            # Flaskアプリケーションを再起動する
            os.execv(sys.executable, [sys.executable] + sys.argv)
            
# ソースコード変更を監視する
observer = PollingObserver()
observer.schedule(ReloadHandler(), path="./app", recursive=True)
observer.start()
