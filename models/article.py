#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel
from datetime import datetime


class Article(BaseModel, db.Model):
    __tablename__ = 'articles'
    user_id = db.Column(
        db.String(60),
        db.ForeignKey('users.id'),
        nullable=False
    )

    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
