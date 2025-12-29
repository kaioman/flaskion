from flask import Flask

def register_routes(app:Flask):
    """
    ルーティングを登録する
    Args:
        app (Flask): Flaskアプリケーションインスタンス
    """
    
    # rootルート
    from .root import root_bp
    app.register_blueprint(root_bp)

    # authルート
    from app.api.v1.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # settingsルート
    from app.api.v1.settings import bp as settings_bp
    app.register_blueprint(settings_bp)
