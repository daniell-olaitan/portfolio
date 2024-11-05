#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel


class Service(BaseModel, db.Model):
    __tablename__ = 'services'
    user_profile_id = db.Column(
        db.String(60),
        db.ForeignKey('user_profiles.id'),
        nullable=False
    )
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
