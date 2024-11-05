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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.id = str(uuid.uuid4())

    def to_json(self) -> Dict[str, Any]:
        obj_dict = {}
        obj = vars(self)
        for key, value in obj.items():
            if key == 'created_at':
                obj_dict['created_at'] = self.created_at.isoformat()
            elif key == 'updated_at':
                obj_dict['updated_at'] = self.updated_at.isoformat()
            elif key == '_sa_instance_state' or key == 'password':
                continue
            elif 'date' in key:
                obj_dict[key] = value.strftime('%Y-%m-%d')
            else:
                obj_dict[key] = value

        return obj_dict
