from database.database import db


class Model(db.Model):
    __abstract__ = True

    def __init__(self):
        self._filters = []

    
    def where(self, column_name=None, value=None, operator="="):
        # If called from class
        if isinstance(self, type):
            obj = self()
        else:
            obj = self

        if column_name is None or value is None:
            raise Exception("Usage: where(column, value, operator='=')")

        obj._filters.append((column_name, value, operator))
        return obj

    
    where = classmethod(where)

    @classmethod
    def all(cls):
        return cls.query.all()

    def _apply_filters(self, query):
        ops = {
            "=": lambda c, v: c == v,
            "!=": lambda c, v: c != v,
            ">": lambda c, v: c > v,
            "<": lambda c, v: c < v,
            ">=": lambda c, v: c >= v,
            "<=": lambda c, v: c <= v,
        }

        for col_name, value, op in self._filters:
            if not hasattr(self.__class__, col_name):
                raise Exception(f"Column '{col_name}' does not exist")

            if op not in ops:
                raise Exception(f"Invalid operator '{op}'")

            column = getattr(self.__class__, col_name)
            query = query.filter(ops[op](column, value))

        return query

    def first(self):
        query = self.__class__.query
        if self._filters:
            query = self._apply_filters(query)

        result = query.first()
        self._filters = []
        return result

    def get(self):
        if not self._filters:
            raise Exception("get() must be used after where()")

        result = self._apply_filters(self.__class__.query).all()
        self._filters = []
        return result