#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel


class Feature(BaseModel, db.Model):
    __tablename__ = 'features'
    project_id = db.Column(
        db.String(60),
        db.ForeignKey('projects.id'),
        nullable=False
    )

    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(2048), nullable=False)
