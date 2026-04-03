from Database.database import db

class Model(db.Model):

    __abstract__ = True
    _allowed_operators = {"=", ">", "<", ">=", "<=", "!="}

    def __init__(self):
        self._conditions = []
        self._model_cls = self.__class__

    def where(self, column, value, operator="="):

        if operator not in self._allowed_operators:
            raise ValueError(f"Invalid operator: {operator}")

        if isinstance(self, type):
            instance = self()
            instance._model_cls = self
            instance._conditions.append((column, operator, value))
            return instance

        self._conditions.append((column, operator, value))
        return self


    def _build_query(self):
        query = db.session.query(self._model_cls)

        for column, operator, value in self._conditions:
            column_attr = getattr(self._model_cls, column)

            if operator == "=":
                query = query.filter(column_attr == value)

            elif operator == ">":
                query = query.filter(column_attr > value)

            elif operator == "<":
                query = query.filter(column_attr < value)

            elif operator == ">=":
                query = query.filter(column_attr >= value)

            elif operator == "<=":
                query = query.filter(column_attr <= value)

            elif operator == "!=":
                query = query.filter(column_attr != value)

        return query


    def get(self):
        if not self._conditions:
            raise Exception("get() must be used after where()")

        return self._build_query().all()


    def first(self):
        if self._conditions:
            return self._build_query().first()

        return db.session.query(self._model_cls).first()


    @classmethod
    def all(cls):
        return db.session.query(cls).all()