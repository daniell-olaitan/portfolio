#!/usr/bin/env python3
from flask import Blueprint

frontend = Blueprint(
    'frontend',
    __name__,
    url_prefix='/me',
    static_folder='static',
    template_folder='templates'
)

from app.frontend.views import *
