#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel
from models.contact import Contact


class UserProfile(BaseModel, db.Model):
    """
    User Profile class
    """
    __tablename__ = 'user_profiles'
    user_id = db.Column(
        db.String(60),
        db.ForeignKey('users.id'),
        nullable=False
    )

    image_url = db.Column(db.String(256))
    bio = db.Column(db.String(2048))
    location = db.Column(db.String(80))
    project_header = db.Column(db.String(2048))
    work_header = db.Column(db.String(2048))
    article_header = db.Column(db.String(2048))
    resume = db.Column(db.String(256))
    contacts = db.relationship(
        'Contact',
        backref='user_profile',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
