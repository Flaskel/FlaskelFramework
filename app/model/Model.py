from database.database import db
from sqlalchemy.orm import Query


class Model(db.Model):
    __abstract__ = True

    def __init__(self):
        self._query: Query = None

    # -----------------------------
    # BASE QUERY
    # -----------------------------
    @classmethod
    def _base_query(cls):
        return db.session.query(cls)

    # -----------------------------
    # SMART WHERE (handles both cases)
    # -----------------------------
    def where(self_or_cls, column: str, value, operator: str = "="):
        
        # 🔹 CASE 1: called like User.where(...)
        if isinstance(self_or_cls, type):
            obj = self_or_cls()
            obj._query = self_or_cls._base_query()
        
        # 🔹 CASE 2: called like obj.where(...)
        else:
            obj = self_or_cls

        column_attr = getattr(obj.__class__, column, None)

        if column_attr is None:
            raise AttributeError(f"{column} is not a valid column")

        condition = obj._build_condition(column_attr, value, operator)
        obj._query = obj._query.filter(condition)

        return obj

    # -----------------------------
    # CONDITION BUILDER
    # -----------------------------
    def _build_condition(self, column, value, operator):
        if operator == "=":
            return column == value
        elif operator == "!=":
            return column != value
        elif operator == ">":
            return column > value
        elif operator == "<":
            return column < value
        elif operator == ">=":
            return column >= value
        elif operator == "<=":
            return column <= value
        else:
            raise ValueError(f"Invalid operator: {operator}")

    # -----------------------------
    # GET
    # -----------------------------
    def get(self):
        if self._query is None:
            raise Exception("Use where() before get()")

        return self._query.all()

    # -----------------------------
    # FIRST
    # -----------------------------
    def first(self_or_cls):

        # 🔹 CASE 1: User.first()
        if isinstance(self_or_cls, type):
            return self_or_cls._base_query().first()

        # 🔹 CASE 2: User.where(...).first()
        else:
            if self_or_cls._query is None:
                raise Exception("Use where() before first()")

            return self_or_cls._query.first()

    # -----------------------------
    # ALL
    # -----------------------------
    @classmethod
    def all(cls):
        return cls._base_query().all()
