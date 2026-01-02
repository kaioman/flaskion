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

    # image_genルート
    from app.api.v1.image_gen import bp as image_gen_bp
    app.register_blueprint(image_gen_bp)

    # image_editルート
    from app.api.v1.image_edit import bp as image_edit_bp
    app.register_blueprint(image_edit_bp)
