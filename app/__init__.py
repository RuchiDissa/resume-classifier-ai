from flask import Flask
from .routes import routes
from .auth import auth

def create_app():
    app = Flask(__name__)
    app.secret_key = '5e36tk37'

    app.register_blueprint(routes)
    app.register_blueprint(auth)

    return app
