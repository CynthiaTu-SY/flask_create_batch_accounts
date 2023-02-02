from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['UPLOAD_FOLDER'] = 'static/files'
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
    app.config['UPLOAD_EXTENSIONS'] = ['.TXT']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .upload import upload
    from .result import result

    app.register_blueprint(upload, url_prefix='/')
    app.register_blueprint(result, url_prefix='/')

    from .models import Group, Account

    with app.app_context():
        db.create_all()
        
    return app