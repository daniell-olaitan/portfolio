#!/usr/bin/env python3
from models import db
from models.base_model import BaseModel


class InvalidToken(BaseModel, db.Model):
    __tablename__ = 'invalid_tokens'
    jti = db.Column(db.String(36), nullable=False, index=True)

    @classmethod
    def verify_jti(cls, jti: str) -> bool:
        """
        Verify the JWT identity
        """
        return bool(db.fetch_object_by(cls, jti=jti))
