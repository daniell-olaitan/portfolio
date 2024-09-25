#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

from config import config
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from helpers import get_provider_cfg

jwt = JWTManager()
migrate = Migrate()
google_document_cfg = get_provider_cfg()


def create_app(config_type: str) -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[config_type])
    from api.v1.auth import auth

    app.register_blueprint(auth)
    CORS(app, resources={
        r'/api/*': {
            'origins': '*'
        }
    })

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    return app
