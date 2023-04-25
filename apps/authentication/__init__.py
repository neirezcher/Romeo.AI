# -*- encoding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)
googleAuth = Blueprint('google_auth', __name__)
