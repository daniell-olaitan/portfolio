#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel
from models.skill import Skill
from models.feature import Feature


class Project(BaseModel, db.Model):
    __tablename__ = 'projects'
    user_id = db.Column(
        db.String(60),
        db.ForeignKey('users.id'),
        nullable=False
    )

    title = db.Column(db.String(60), nullable=False)
    image_url = db.Column(db.String(256))
    description = db.Column(db.String(2048), nullable=False)
    project_url = db.Column(db.String(256))
    github_url = db.Column(db.String(256))
    skills = db.relationship(
        'Skill',
        backref='project',
        lazy='dynamic'
    )

    features = db.relationship(
        'Feature',
        backref='project',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
