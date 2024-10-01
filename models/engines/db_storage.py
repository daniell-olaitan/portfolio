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

    def fetch_an_object_by(
        self,
        cls: t.Type[ModelType],
        **kwargs: t.Mapping
    ) -> ModelType:
        """
        Fetch an object from the database using attributes
        """
        return self.session.query(cls).filter_by(**kwargs).first()

    def fetch_object_by(
        self,
        cls: t.Type[ModelType],
        **kwargs: t.Mapping
    ) -> t.List[ModelType]:
        """
        Fetch object(s) from the database using attributes
        """
        return self.session.query(cls).filter_by(**kwargs).all()

    def update_object(
        self,
        cls: t.Type[ModelType],
        id: str,
        **kwargs:t.Mapping
    ) -> None:
        """
        Update a given model object
        """
        obj = self.session.get(cls, id)
        for key, value in kwargs.items():
            if key not in obj.__table__.columns.keys():
                raise ValueError(
                    f"{key} field does not exist in {cls.__name__} Model"
                )

            setattr(obj, key, value)

        self.session.add(obj)
        self.session.commit()
