#!/usr/bin/env python3
from os import getenv
from datetime import timedelta


class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_REDIRECT_URI = 'https://127.0.0.1:5000/v1/auth/login-callback'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_SENDER = getenv('MAIL_SENDER')
    REDIS_URI = 'redis://localhost:6379/0'


class DevelopmentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@localhost/{}".format(
        getenv('DATABASE_USERNAME'),
        getenv('DATABASE_PASSWORD'),
        getenv('DATABASE')
    )


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DeploymentConfig(DevelopmentConfig):
    DEBUG = False


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'deployment': DeploymentConfig
}
