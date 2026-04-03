from orm import db, Model


class User(Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)


class Employee(Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


class Product(Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)