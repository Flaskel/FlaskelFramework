from database.database import db
import os
import importlib.util


class Model(db.Model):
    __abstract__ = True

    _allowed_operators = {"=", ">", "<", ">=", "<=", "!="}

    # ---------------- INIT ----------------
    def __init__(self):
        self._conditions = []
        self._model_cls = self.__class__

    # ---------------- QUERY BUILDER ----------------
    @classmethod
    def where(cls, column, value, operator="="):
        if operator not in cls._allowed_operators:
            raise ValueError(f"Invalid operator: {operator}")

        if not hasattr(cls, column):
            raise ValueError(f"Invalid column: {column}")

        instance = cls()
        instance._conditions.append((column, operator, value))
        return instance

    def and_where(self, column, value, operator="="):
        if operator not in self._allowed_operators:
            raise ValueError(f"Invalid operator: {operator}")

        if not hasattr(self._model_cls, column):
            raise ValueError(f"Invalid column: {column}")

        self._conditions.append((column, operator, value))
        return self

    # ---------------- INTERNAL QUERY ----------------
    def _build_query(self):
        query = db.session.query(self._model_cls)

        operators = {
            "=": lambda c, v: c == v,
            ">": lambda c, v: c > v,
            "<": lambda c, v: c < v,
            ">=": lambda c, v: c >= v,
            "<=": lambda c, v: c <= v,
            "!=": lambda c, v: c != v,
        }

        for column, operator, value in self._conditions:
            column_attr = getattr(self._model_cls, column)
            query = query.filter(operators[operator](column_attr, value))

        return query

    # ---------------- EXECUTION METHODS ----------------
    def get(self):
        if not self._conditions:
            raise Exception("get() must be used after where()")

        result = self._build_query().all()
        self._reset()
        return result

    def first(self):
        result = self._build_query().first()
        self._reset()
        return result

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    # ---------------- UTILITIES ----------------
    def _reset(self):
        self._conditions = []

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    # ---------------- MIGRATION RUNNER ----------------
    @staticmethod
    def run_migrations():
        migration_path = "app/Database/Migrations"

        if not os.path.exists(migration_path):
            print("No migrations found")
            return

        files = sorted(os.listdir(migration_path))

        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(migration_path, file)

                try:
                    spec = importlib.util.spec_from_file_location(file, full_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, "upgrade") and callable(module.upgrade):
                        print(f"Running migration: {file}")
                        module.upgrade()
                    else:
                        print(f"Skipping {file} (no upgrade function)")

                except Exception as e:
                    print(f"Error in migration {file}: {e}")

        print("Migrations completed!")