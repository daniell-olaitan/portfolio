#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel
from models.contact import Contact
from models.service import Service


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
    bio = db.Column(db.Text)
    location = db.Column(db.String(80))
    tagline = db.Column(db.Text)
    project_header = db.Column(db.Text)
    work_header = db.Column(db.Text)
    article_header = db.Column(db.Text)
    contribution_header = db.Column(db.Text)
    resume = db.Column(db.String(256))
    contacts = db.relationship(
        'Contact',
        backref='user_profile',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    services = db.relationship(
        'Service',
        backref='user_profile',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
