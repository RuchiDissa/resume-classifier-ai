import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = '5e36tk37'

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes)
    app.register_blueprint(auth)

    return app
