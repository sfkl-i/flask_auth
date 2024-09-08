import binascii
import os
from flask import Flask, render_template
from flask_login import LoginManager
from .models.base import create_db
from .models.user import User
from .routes.auth import auth_bp
from .models.base import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24)).decode()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

create_db()
app.register_blueprint(auth_bp)


@login_manager.user_loader
def load_user(user_id):
    with Session() as session:
        return session.query(User).get(user_id)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
