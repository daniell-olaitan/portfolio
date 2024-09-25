#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
import typing as t

ModelType = t.TypeVar('Model')


class DBStorage(SQLAlchemy):
    def add_object(
        self,
        cls: t.Type[ModelType],
        **kwargs: t.Mapping
    ) -> ModelType:
        """
        Create and add new object to the db
        """
        obj = cls(**kwargs)
        self.session.add(obj)
        self.session.commit()

        return obj

    def remove_object(self, obj: ModelType) -> None:
        self.session.delete(obj)
        self.session.commit()

    def fetch_object_by(
        self,
        cls: t.Type[ModelType],
        **kwargs: t.Mapping
    ) -> ModelType:
        """
        Fetch object(s) from the database using attributes
        """
        return self.session.query(cls).filter_by(**kwargs).all()

    def update_object(
        self,
        id: str,
        cls: t.Type[ModelType],
        **kwargs
    ) -> None:
        """
        Update a given model object
        """
        obj = self.session.query(cls).get(id)
        for key, value in kwargs.items():
            if key not in obj.__table__.columns.keys():
                raise ValueError

            setattr(obj, key, value)

        self.session.add(obj)
        self.session.commit()
