import os

# デバッグモード判定
if os.getenv("DEBUGPY", "false").lower() == "true":
    # 二重listen防止対策
    if not os.getenv("DEBUGPY_STARTED"):
        os.environ["DEBUGPY_STARTED"] = "true"
        import debugpy
        
        # デバッグポート取得
        debug_port = int(os.getenv("DEBUG_PORT", "5150"))
        print(f"🚀[debugpy] Preparing to open listner on port {debug_port}")
        # デバッグポートlisten
        debugpy.listen(("0.0.0.0", debug_port))
        print(f"🔧[debugpy] Waiting for client connection on port {debug_port}")
        # クライアントからの接続待機
        debugpy.wait_for_client()
        print(f"✅[debugpy] Client connected. Continuing execution.")

from app.main import app # noqa: F401

# NOTE:
# Do not remove 'app'. Although it looks unused in this file,
# Flask (`flask run`) and Gunicorn (`server:app`) rely on it as the entrypoint.
# It is required for the application to start correctly.

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5100)