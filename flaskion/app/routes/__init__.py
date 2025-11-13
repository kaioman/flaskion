from flask import Flask
from .root import root_bp

def register_routes(app:Flask):
    """
    ルーティングを登録する
    Args:
        app (Flask): Flaskアプリケーションインスタンス
    """
    app.register_blueprint(root_bp)
