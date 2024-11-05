#!/usr/bin/env python3
from flask import Blueprint

admin = Blueprint(
    'admin', __name__, url_prefix='/me/admin',
    static_folder='static',
    template_folder='templates'
)

from app.admin.views import *
