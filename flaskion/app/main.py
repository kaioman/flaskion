import os
import sys
import time
from flask import Flask, g, session
from flask_socketio import SocketIO
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver
from app.routes import register_routes
from app.core.config import settings
from app.core.logging import init_logging
from app.models.user import User
from app.db.session import db

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
    email = session.get("email")
    g.current_user = db.query(User).filter_by(email=email).first() if email else None

@app.context_processor
def inject_user():
    """
    テンプレートに current_userを注入
    """
    return dict(current_user=g.get("current_user"))

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
