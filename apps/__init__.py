# -*- encoding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
#from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from mongoengine import connect
from datetime import datetime
#from bson import ObjectId, json_util
from flask.json import JSONEncoder
from importlib import import_module

from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.github import make_github_blueprint


#db = SQLAlchemy()
db = MongoEngine()
login_manager = LoginManager()
app = Flask(__name__)

'''class MongoJsonEncoder(JSONEncoder):
    #adjustments to the flask json encoder for MongoEngine support
    def default(self, obj):
        if isinstance(obj,datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj,ObjectId):
            return str(obj)
        return json_util.default(obj,json_util.CANONICAL_JSON_OPTIONS)'''

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home','welcome'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

'''
def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
'''

def create_app(config):
    
    # we altered the app's json_encoder to properly work with mongoengine objects
    #app.json_encoder=MongoJsonEncoder
    app.config.from_object(config)
    
    google_bp = make_google_blueprint(scope=["profile", "email"])
    app.register_blueprint(google_bp, url_prefix="/login")
    github_bp =  make_github_blueprint()
    app.register_blueprint(github_bp, url_prefix="/login")
    register_extensions(app)
    # we register our blueprints (they acts like mini-flask apps that we can use to organize our app into modules with different functionality)
    register_blueprints(app)
    return app
