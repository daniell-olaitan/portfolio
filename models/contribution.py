#!/usr/bin/env python3
"""
Module for open source contribution model
"""
from models import db
from models.base_model import BaseModel
from models.git_ref import GitRef
from models.skill import Skill


class Contribution(BaseModel, db.Model):
    __tablename__ = 'contributions'
    user_id = db.Column(
        db.Text,
        db.ForeignKey('users.id'),
        nullable=False
    )

    name = db.Column(db.String(120), nullable=False)
    repo_url = db.Column(db.String(256), nullable=False)
    contribution_type = db.Column(db.String(60))
    role = db.Column(db.String(60))
    date = db.Column(db.DateTime)
    description = db.Column(
        db.Text, nullable=False
    )  # List of actions separated by '::'

    impact = db.Column(
        db.Text, nullable=False
    )  # List of impacts separated by '::'

    technologies = db.Column(
        db.Text, nullable=False
    )  # List of tools separated by '::'

    skills = db.relationship(
        'Skill',
        backref='contribution',
        lazy='dynamic'
    )

    git_refs = db.relationship(
        'GitRef',
        backref='contribution',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
