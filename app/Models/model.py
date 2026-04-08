from database.database import db
from sqlalchemy.orm import Query
from sqlalchemy import or_, and_


class Model(db.Model):
    __abstract__ = True

    def __init__(self):
        self._query: Query | None = None

    @classmethod
    def _base_query(cls):
        return db.session.query(cls)

    @classmethod
    def _new_instance_with_query(cls):
        obj = cls()
        obj._query = cls._base_query()
        return obj

    def _resolve_target(self_or_cls):
        if isinstance(self_or_cls, type):
            return self_or_cls._new_instance_with_query()
        return self_or_cls

    def _build_condition(self, column, value, operator):
        operators = {
            "=": column == value,
            "!=": column != value,
            ">": column > value,
            "<": column < value,
            ">=": column >= value,
            "<=": column <= value,
        }

        if operator not in operators:
            raise ValueError(f"Invalid operator: {operator}")

        return operators[operator]

    def where(self_or_cls, column: str, value, operator: str = "="):
        obj = self_or_cls._resolve_target() if isinstance(self_or_cls, type) else self_or_cls

        column_attr = getattr(obj.__class__, column, None)
        if column_attr is None:
            raise AttributeError(f"{column} is not a valid column")

        if obj._query is None:
            obj._query = obj.__class__._base_query()

        condition = obj._build_condition(column_attr, value, operator)
        obj._query = obj._query.filter(condition)
        return obj

    def get(self):
        if self._query is None:
            raise Exception("Use where() before get()")
        return self._query.all()

    def first(self_or_cls):
        if isinstance(self_or_cls, type):
            return self_or_cls._base_query().first()

        if self_or_cls._query is None:
            raise Exception("Use where() before first()")

        return self_or_cls._query.first()

    @classmethod
    def all(cls):
        return cls._base_query().all()