#!/usr/bin/env python3
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/v1')

from app.api.v1.app_views.user import *
from app.api.v1.app_views.profile import *
from app.api.v1.app_views.project import *
from app.api.v1.app_views.contact import *
from app.api.v1.app_views.feature import *
from app.api.v1.app_views.work import *
from app.api.v1.app_views.experience import *
from app.api.v1.app_views.article import *
from app.api.v1.app_views.contribution import *
from app.api.v1.app_views.git_ref import *
from app.api.v1.app_views.service import *
