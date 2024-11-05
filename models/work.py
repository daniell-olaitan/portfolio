#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel
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
    company = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    skills = db.Column(
        db.Text, nullable=False
    )  # List of skills separated by '::'

    experiences = db.relationship(
        'Experience',
        backref='work',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def to_json(self):
        obj_dict = super().to_json()

        if obj_dict['skills']:
            obj_dict['skills'] = obj_dict['skills'].split('::')

        return obj_dict
