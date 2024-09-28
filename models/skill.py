#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel


class Skill(BaseModel, db.Model):
    __tablename__ = 'skills'
    project_id = db.Column(db.String(60), db.ForeignKey('projects.id'))
    work_id = db.Column(db.String(60), db.ForeignKey('works.id'))
    name = db.Column(db.String(60), nullable=False)
