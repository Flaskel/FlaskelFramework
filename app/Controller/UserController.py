from app.Models.User import User
from flask import jsonify, request, render_template
from app.Database.database import db

class UserController:
    def index():
        return render_template('users/index.html',users =User.query.all())

    def create():
        return render_template('users/create.html')

    def store():
        User().create(request.form)
        return jsonify({'Message':f'User has been created'})


    def show(id):
        return render_template('users/show.html',user =User.query.get(id))

    def edit(id):
        return render_template('users/edit.html',user =User.query.get(id))

    def update(id):
        User.query.get(id).update(request.form)
        return jsonify({'Message':f'User has been updated with id {id}'})
    
    def delete(id):
        User.query.get(id).delete()
        return jsonify({'Message':f'User has been deleted with id {id}'})
