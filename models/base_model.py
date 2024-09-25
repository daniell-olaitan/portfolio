#!/usr/bin/env python3
from models import db
import uuid
from datetime import datetime
from typing import Dict, Any


class BaseModel:
    id = db.Column(
        db.String(60),
        primary_key=True,
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid.uuid4())

    def to_json(self) -> Dict[str, Any]:
        obj = vars(self)
        obj['created_at'] = self.created_at.isoformat()
        obj['updated_at'] = self.updated_at.isoformat()
        del obj['_sa_instance_state']
        del obj['password']

        return obj
