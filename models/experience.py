#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel


class Experience(BaseModel, db.Model):
    __tablename__ = 'experiences'
    work_id = db.Column(
        db.String(60),
        db.ForeignKey('works.id'),
        nullable=False
    )

    result = db.Column(db.Text, nullable=False)
