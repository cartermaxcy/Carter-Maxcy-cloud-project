import logging

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from config import Config
from .models import db, User

login_manager = LoginManager()

limiter = Limiter(get_remote_address)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.info('Initializing DB...')
    db.init_app(app)
    logging.info('DB initialized.')

    logging.info('Initializing login manager...')
    login_manager.init_app(app)
    logging.info('Login manager initialized.')

    logging.info('Initializing limiter...')
    limiter.init_app(app)
    logging.info('Limiter initialized.')

    from .routes.auth import auth
    from .routes.products import products
    app.register_blueprint(auth)
    app.register_blueprint(products)

    with app.app_context():
        db.create_all()

    return app

