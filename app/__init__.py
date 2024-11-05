#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

from config import config
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from flask_mail import Mail

jwt = JWTManager()
mail = Mail()
migrate = Migrate()


def create_app(config_type: str) -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[config_type])
    from app.api.v1.auth import auth
    from app.api.v1.app_views import app_views
    from app.frontend import frontend
    from app.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(app_views)
    app.register_blueprint(frontend)
    app.register_blueprint(admin)
    CORS(app, resources={
        r'/v1*': {
            'origins': '*'
        }
    })

    jwt.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    return app
