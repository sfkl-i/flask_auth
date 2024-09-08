import binascii
import os
from flask import Flask
from flask_login import LoginManager
from .models.base import create_db
from .models.user import User
from .models.base import Session

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Adjusted to use blueprint 'auth'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24)).decode()

    login_manager.init_app(app)

    # Import blueprints and register them here
    from .routes.auth import auth_bp
    from .routes.default import default_bp
    from .routes.error import error_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(default_bp)
    app.register_blueprint(error_bp)

    # Create the database
    create_db()

    return app


@login_manager.user_loader
def load_user(user_id: int):
    with Session() as session:
        return session.query(User).where(User.id == user_id).first()
