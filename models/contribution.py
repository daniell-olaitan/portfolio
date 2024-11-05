#!/usr/bin/env python3
"""
Module for open source contribution model
"""
from models import db
from models.base_model import BaseModel
from models.git_ref import GitRef


class Contribution(BaseModel, db.Model):
    __tablename__ = 'contributions'
    user_id = db.Column(
        db.String(60),
        db.ForeignKey('users.id'),
        nullable=False
    )

    name = db.Column(db.String(120), nullable=False)
    repo_url = db.Column(db.String(256), nullable=False)
    contribution_type = db.Column(db.String(60))
    role = db.Column(db.String(60))
    date = db.Column(db.DateTime)
    descriptions = db.Column(
        db.Text, nullable=False
    )  # List of actions separated by '::'

    impacts = db.Column(
        db.Text, nullable=False
    )  # List of impacts separated by '::'

    technologies = db.Column(
        db.Text, nullable=False
    )  # List of tools separated by '::'

    skills = db.Column(
        db.Text, nullable=False
    )  # List of skills separated by '::'

    git_refs = db.relationship(
        'GitRef',
        backref='contribution',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def to_json(self):
        obj_dict = super().to_json()
        if obj_dict['skills']:
            obj_dict['skills'] = obj_dict['skills'].split('::')

        if obj_dict['technologies']:
            obj_dict['technologies'] = obj_dict['technologies'].split('::')

        if obj_dict['impacts']:
            obj_dict['impacts'] = obj_dict['impacts'].split('::')

        if obj_dict['descriptions']:
            obj_dict['descriptions'] = obj_dict['descriptions'].split('::')

        return obj_dict
