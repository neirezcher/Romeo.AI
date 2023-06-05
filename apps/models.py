# -*- encoding: utf-8 -*-

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass
from datetime import datetime
from bson import ObjectId

class ModelMetadata(db.Document):
    _id = db.ObjectIdField(required=True, primary_key=True)
    filename = db.StringField(required=True)
    length = db.IntField(required=True)
    chunkSize=db.IntField(required=True)
    uploadDate=db.DateTimeField()
    # Include other metadata fields as needed

    meta = {'collection': 'models.files'}  # Specify the collection name


class ModelChunk(db.Document):
    files_id = db.ObjectIdField(required=True)
    n = db.IntField(required=True)
    data = db.BinaryField(required=True)

    meta = {'collection': 'models.chunks'}  # Specify the collection name
class ReportMetadata(db.Document):
    _id = db.ObjectIdField(required=True, primary_key=True)
    filename = db.StringField(required=True)
    length = db.IntField(required=True)
    chunkSize=db.IntField(required=True)
    uploadDate=db.DateTimeField()
    # Include other metadata fields as needed

    meta = {'collection': 'reports.files'}  # Specify the collection name


class ReportChunk(db.Document):
    files_id = db.ObjectIdField(required=True)
    n = db.IntField(required=True)
    data = db.BinaryField(required=True)

    meta = {'collection': 'reports.chunks'}  # Specify the collection name
class Deepconcorun(db.Document):
    __tablename__ = 'deepconcorun'
    
    _id= db.ObjectIdField(default=ObjectId, primary_key=True)
    general_robustness=db.DecimalField(default=0,precision=4)
    ssc_robustness=db.DecimalField(precision=4)
    nc_robustness=db.DecimalField(precision=4)
    nbc_robustness=db.DecimalField(precision=4)
    class_robustness=db.DictField()
    heatmap_matrix=db.DictField()
    norm = db.StringField(required=True, max_length=50)
    criteria=db.StringField(required=True, max_length=50)
    dataset = db.StringField(required=True, max_length=50)
    modelref = db.ReferenceField('ModelMetadata')
    reportref = db.ReferenceField('ReportMetadata')
    state=db.StringField(max_length=50)

class User(db.Document, UserMixin):

    __tablename__ = 'user'

    #public_id = db.StringField(unique = True)
    username = db.StringField( unique=True, null=False, default=None)
    email = db.EmailField( unique=True, nullable=False, default=None)
    password = db.BinaryField(default=None)
    has_usable_password=db.BooleanField(default=True)

    google_id=db.StringField(unique=True, required=False,sparse=True, index=True)
    github_id=db.StringField(unique=True, required=False,sparse=True, index=True)

    list_run=db.ListField(db.ReferenceField('Deepconcorun'))
    profile_image = db.ImageField(default=None)
    firstname = db.StringField()
    lastname = db.StringField()
    city = db.StringField()
    country = db.StringField()
    about_me = db.StringField()
    role = db.StringField(default='member')
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

class ContactUS(db.Document):
    name = db.StringField(required=True, max_length=100)
    email = db.StringField(required=True, max_length=100)
    message = db.StringField(required=True, max_length=500)
    created_at = db.DateTimeField(default=datetime.now)
    replied = db.BooleanField(default=False)


    

@login_manager.user_loader
def user_loader(id):
    return User.objects(id=id).first()


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = User.objects(email=email).first()
    return user if user else None







