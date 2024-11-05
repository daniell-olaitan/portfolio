#!/usr/bin/env python3
"""
Module for views related to open source article resource
"""
from models.user import User
from utils import APINamespace
from app.api.v1.app_views import app_views
from models.article import Article
from flask.typing import ResponseReturnValue
from flask_jwt_extended import jwt_required

article = APINamespace(Article)


@app_views.route('/users/<string:user_id>/articles', methods=['POST'])
@jwt_required()
@article.verify_resource_ownership(User, 'user_id', 'id')
@article.validate_json_input()
def create_article(user_id: str) -> ResponseReturnValue:
    """
    Create a new article for a user
    """
    return article.create_resource(
        [{
            'id': user_id,
            'name': 'user_id',
            'type': User
        }]
    )


@app_views.route('/articles/<string:article_id>', methods=['GET'])
def read_article(article_id: str) -> ResponseReturnValue:
    """
    Fetch a article
    """
    return article.get_resource(article_id)


@app_views.route('/users/<string:user_id>/articles', methods=['GET'])
def read_articles(user_id: str) -> ResponseReturnValue:
    """
    Fetch all the articles of a user
    """
    return article.get_resources_from_relationship(User, user_id, 'articles')


@app_views.route('/articles/<string:article_id>', methods=['PATCH'])
@jwt_required()
@article.verify_resource_ownership(Article, 'article_id', 'user_id')
@article.validate_json_input()
def update_article(article_id: str) -> ResponseReturnValue:
    """
    Update a user's article
    """
    return article.update_resource(article_id)


@app_views.route('/articles/<string:article_id>', methods=['DELETE'])
@jwt_required()
@article.verify_resource_ownership(Article, 'article_id', 'user_id')
def delete_article(article_id: str) -> ResponseReturnValue:
    """
    Delete a user's article
    """
    return article.delete_resource(article_id)
