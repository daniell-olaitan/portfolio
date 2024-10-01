#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel
from models.skill import Skill
from models.experience import Experience


class Work(BaseModel, db.Model):
    __tablename__ = 'works'
    user_id = db.Column(
        db.String(60),
        db.ForeignKey('users.id'),
        nullable=False
    )

    title = db.Column(db.String(60), nullable=False)
    image_url = db.Column(db.String(256))
    description = db.Column(db.String(2048), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    skills = db.relationship(
        'Skill',
        backref='work',
        lazy='dynamic'
    )

    experiences = db.relationship(
        'Experience',
        backref='user_profile',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
