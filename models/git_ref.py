#!/usr/bin/env python3
"""
Module for git reference model
"""
from models import db
from models.base_model import BaseModel


class GitRef(BaseModel, db.Model):
    __tablename__ = 'git_refs'
    open_source_contribution_id = db.Column(
        db.String(60),
        db.ForeignKey('contributions.id')
    )

    status = db.Column(db.String(60), nullable=False)
    commit_id = db.Column(db.String(256), nullable=False)
    pull_request_url = db.Column(db.String(256), nullable=False)
    issue_url = db.Column(db.String(256))
