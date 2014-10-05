#! ../env/bin/python
import os

from flask import Flask
from tektonik.models import db
from tektonik.property import controller as property
from tektonik.path import controller as path
from tektonik.page import controller as page

def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. ark.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    #init SQLAlchemy
    db.init_app(app)

    # register our blueprints
    app.register_blueprint(property)
    app.register_blueprint(path)
    app.register_blueprint(page)

    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    app = create_app('ark.settings.%sConfig' % env.capitalize(), env=env)

    app.run()
