from flask import Flask, render_template
from flask_socketio import SocketIO
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver
import os
import sys
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

class ReloadHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            # 少し待機
            time.sleep(1)
            # コンソールに変更検知を表示
            print(f"🔄 ソースコード変更検知: {event.src_path} | タイプ: {event.event_type}  再起動します...")
            # Flaskアプリケーションを再起動する
            os.execv(sys.executable, ['python'] + sys.argv)
            
# ソースコード変更を監視する
observer = PollingObserver()
observer.schedule(ReloadHandler(), path=".", recursive=True)
observer.start()

@app.route("/")
def index():
    return render_template("index.html")
