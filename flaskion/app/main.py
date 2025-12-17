from flask import Flask
from flask_socketio import SocketIO
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver
from .routes import register_routes
import os
import sys
import time

# FlaskアプリケーションとSocketIOの初期化#
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# ルートを登録
register_routes(app)

# class ReloadHandler(FileSystemEventHandler):
#     def on_any_event(self, event):
#         if event.src_path.endswith('.py'):
#             # 少し待機
#             time.sleep(1)
#             # コンソールに変更検知を表示
#             print(f"🔄 ソースコード変更検知: {event.src_path} | タイプ: {event.event_type}  再起動します...")
#             # Flaskアプリケーションを再起動する
#             os.execv(sys.executable, [sys.executable] + sys.argv)
            
# # ソースコード変更を監視する
# observer = PollingObserver()
# observer.schedule(ReloadHandler(), path="./app", recursive=True)
# observer.start()
