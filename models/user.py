#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel
from models.user_profile import UserProfile
from models.article import Article
from models.project import Project
from models.work import Work
from models.contribution import Contribution
from flask_login import UserMixin
from hashlib import md5
import typing as t
from sqlalchemy import desc


class User(UserMixin, BaseModel, db.Model):
    """
    Implement user model
    """
    __tablename__ = 'users'
    name = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    articles = db.relationship(
        'Article',
        backref='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    projects = db.relationship(
        'Project',
        backref='user',
        cascade='all, delete-orphan',
        lazy='dynamic',
        order_by=desc(Project.created_at)
    )

    works = db.relationship(
        'Work',
        backref='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    contributions = db.relationship(
        'Contribution',
        backref='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    profile = db.relationship(
        'UserProfile',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan',
    )

    def __init__(self, **kwargs: t.Mapping) -> None:
        super().__init__(**kwargs)
        if kwargs and kwargs.get('password', None):
            password_hash = md5(kwargs['password'].encode('utf-8'))
            self.password = password_hash.hexdigest()

    @classmethod
    def validate_user_details(cls, **kwargs: t.Mapping) -> t.List[str]:
        """
        Check if user details are valid
        """
        errors = []
        for field, value in kwargs.items():
            if not value:
                errors.append({field: f"{field} is required"})

        return errors

    def to_json(self):
        obj_dict = super().to_json()
        if self.profile:
            obj_dict['profile_id'] = self.profile.id
        else:
            obj_dict['profile_id'] = None

        return obj_dict
