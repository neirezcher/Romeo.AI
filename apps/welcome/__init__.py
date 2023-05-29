from flask import Blueprint

blueprint = Blueprint(
    'welcome_blueprint',
    __name__,
    url_prefix=''
)