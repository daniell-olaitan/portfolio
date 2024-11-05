#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
import typing as t
from sqlalchemy.exc import IntegrityError

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
        for field in kwargs.keys():
            if field not in cls.__table__.columns.keys():
                raise ValueError(
                    f"{field} field does not exist in {cls.__name__} Model"
                )

        try:
            obj = cls(**kwargs)
            self.session.add(obj)
            self.session.commit()

            return self.session.get(cls, obj.id)
        except IntegrityError as err:
            self.session.rollback()
            raise ValueError(f"Database error: {err}")

    def remove_object(self, cls: t.Type[ModelType], id: str) -> None:
        try:
            obj = self.session.get(cls, id)
            if not obj:
                raise ValueError('id does not exist')

            self.session.delete(obj)
            self.session.commit()
        except IntegrityError as err:
            self.session.rollback()
            raise ValueError(f"Database error: {err}")

    def fetch_object(
        self,
        cls: t.Type[ModelType],
        **kwargs: t.Mapping
    ) -> ModelType:
        """
        Fetch an object from the database using attributes
        """
        return self.session.query(cls).filter_by(**kwargs).first()

    def fetch_objects(
        self,
        cls: t.Type[ModelType],
        **kwargs: t.Mapping
    ) -> t.List[ModelType]:
        """
        Fetch object(s) from the database using attributes
        """
        return self.session.query(cls).filter_by(**kwargs).all()

    def fetch_all(self, cls: t.Type[ModelType]) -> t.List[ModelType]:
        """
        Fetch all the objects of type cls from the database
        """
        return self.session.query(cls).all()

    def update_object(
        self,
        cls: t.Type[ModelType],
        id: str,
        **kwargs:t.Mapping
    ) -> ModelType:
        """
        Update a given model object
        """
        from datetime import datetime
        from hashlib import md5

        obj = self.session.get(cls, id)
        if not obj:
            raise ValueError('id does not exist')

        for key, value in kwargs.items():
            if key not in obj.__table__.columns.keys():
                raise ValueError(
                    f"{key} field does not exist in {cls.__name__} Model"
                )

            if key == 'password':
                password_hash = md5(value.encode('utf-8'))
                value = password_hash.hexdigest()

            setattr(obj, key, value)
            obj.updated_at = datetime.now()

        try:
            self.session.add(obj)
            self.session.commit()

            return self.session.get(cls, id)
        except IntegrityError as err:
            self.session.rollback()
            raise ValueError(f"Database error: {err}")
