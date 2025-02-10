from flask import Flask
from config import Config
from app.extentions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.cantor import bp as cantor_bp
    app.register_blueprint(cantor_bp, url_prefix='/cantor')
    
    from app.models import exchange

    @app.route('/test/')
    def test_page():
        return "<h1>Test page</h1>"

    return app
