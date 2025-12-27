from flask import Flask
from flask_login import LoginManager
from config import Config
from .models import db, User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    return app

