from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query, declared_attr

db = SQLAlchemy()


def pluralize(name: str):
    if name.endswith("y"):
        return name[:-1].lower() + "ies"
    elif name.endswith("s"):
        return name.lower() + "es"
    return name.lower() + "s"


class Model(db.Model):
    __abstract__ = True
    _query: Query = None

    # AUTO TABLE NAME
    @declared_attr
    def __tablename__(cls):
        return pluralize(cls.__name__)

    # -----------------------------
    @classmethod
    def _base_query(cls):
        return db.session.query(cls)

    # -----------------------------
    def where(self_or_cls, column: str, value, operator: str = "="):

        if isinstance(self_or_cls, type):
            obj = self_or_cls.__new__(self_or_cls)
            obj._query = self_or_cls._base_query()
        else:
            obj = self_or_cls

        column_attr = getattr(obj.__class__, column, None)

        if column_attr is None:
            raise AttributeError(f"{column} is not a valid column")

        if operator == "=":
            condition = column_attr == value
        elif operator == "!=":
            condition = column_attr != value
        elif operator == ">":
            condition = column_attr > value
        elif operator == "<":
            condition = column_attr < value
        elif operator == ">=":
            condition = column_attr >= value
        elif operator == "<=":
            condition = column_attr <= value
        else:
            raise ValueError(f"Invalid operator: {operator}")

        obj._query = obj._query.filter(condition)
        return obj

    # -----------------------------
    def get(self):
        if self._query is None:
            raise Exception("Use where() before get()")
        return self._query.all()

    # -----------------------------
    def first(self_or_cls):

        if isinstance(self_or_cls, type):
            return self_or_cls._base_query().first()
        else:
            if self_or_cls._query is None:
                raise Exception("Use where() before first()")
            return self_or_cls._query.first()

    # -----------------------------
    @classmethod
    def all(cls):
        return cls._base_query().all()