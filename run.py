# -*- encoding: utf-8 -*-


#from flask_migrate import Migrate
from sys import exit
from decouple import config

from apps.config import config_dict
from apps import create_app

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
#Migrate(app, db)
import base64

def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')
#the b64encode filter is not available in Jinja by default so we can define a custom filter to perform the base64 encoding
app.jinja_env.filters['b64encode'] = b64encode_filter

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.MONGODB_SETTINGS['host'])

if __name__ == "__main__":
    app.run()
