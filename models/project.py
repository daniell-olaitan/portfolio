#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel
from models.feature import Feature
from sqlalchemy import event
from utils import delete_file


class Project(BaseModel, db.Model):
    __tablename__ = 'projects'
    user_id = db.Column(
        db.String(60),
        db.ForeignKey('users.id'),
        nullable=False
    )

    title = db.Column(db.String(60), nullable=False)
    image_url = db.Column(db.String(256))
    video_url = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=False)
    project_url = db.Column(db.String(256))
    github_url = db.Column(db.String(256))
    skills = db.Column(
        db.Text, nullable=False
    )  # List of skills separated by '::'

    features = db.relationship(
        'Feature',
        backref='project',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def to_json(self):
        obj_dict = super().to_json()

        if obj_dict['skills']:
            obj_dict['skills'] = obj_dict['skills'].split('::')

        return obj_dict


def delete_files(mapper, connection, target):
    if target.image_url:
        delete_file(target.image_url)

    if target.video_url:
        delete_file(target.video_url)


event.listen(Project, 'after_delete', delete_files)
