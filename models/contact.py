#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel


class Contact(BaseModel, db.Model):
    __tablename__ = 'contacts'
    user_profile_id = db.Column(
        db.String(60),
        db.ForeignKey('user_profiles.id'),
        nullable=False
    )
    name = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(80), nullable=False)
