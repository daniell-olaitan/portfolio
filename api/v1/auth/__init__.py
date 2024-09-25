#!/usr/bin/python3
from flask import Blueprint
from os import getenv

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

from api.v1.auth.views import *
