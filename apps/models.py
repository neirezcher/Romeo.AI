# -*- encoding: utf-8 -*-

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass
from datetime import datetime


class User(db.Document, UserMixin):

    __tablename__ = 'user'

    #public_id = db.StringField(unique = True)
    username = db.StringField( unique=True, null=False, default=None)
    email = db.StringField( unique=True, nullable=False, default=None)
    password = db.BinaryField(default=None)
    has_usable_password=db.BooleanField(default=True)

    google_id=db.StringField(unique=True, required=False,sparse=True, index=True)
    github_id=db.StringField(unique=True, required=False,sparse=True, index=True)
   
    '''
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)'''
    def to_json(self):
        return {"id": self.id,
            "name": self.username,
            "email":self.email}

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.objects(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.objects(username=username).first()
    return user if user else None







