#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel
from models.article import Article

tags_articles = db.Table(
    'tags_articles',
    db.Column(
        'tag_id',
        db.String(60),
        db.ForeignKey('tags.id'),
        primary_key=True
    ),
    db.Column(
        'article_id',
        db.String(60),
        db.ForeignKey('articles.id'),
        primary_key=True
    )
)


class Tag(BaseModel, db.Model):
    __tablename__ = 'tags'
    article_id = db.Column(db.String(60), db.ForeignKey('articles.id'))
    name = db.Column(db.String(60), nullable=False)
    articles = db.relationship(
        'Article',
        secondary=tags_articles,
        backref=db.backref('tags', lazy='dynamic'),
        cascade='save-update, merge, delete-orphan'
    )
