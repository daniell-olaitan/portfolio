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
    GOOGLE_REDIRECT_URI = 'https://127.0.0.1:5000/api/v1/auth/login-callback'


class DevelopmentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@localhost/{}".format(
        getenv('DATABASE_USERNAME_DEV'),
        getenv('DATABASE_PASSWORD'),
        getenv('DATABASE_DEV')
    )


class TestingConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DeploymentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=10)
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        getenv('DATABASE_USERNAME'),
        getenv('DATABASE_PASSWORD'),
        getenv('DATABASE_HOST'),
        getenv('DATABASE_PORT'),
        getenv('DATABASE')
    )


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'deployment': DeploymentConfig
}
