#! ../env/bin/python
import os

from flask import Flask
from tektonik.models import db
from tektonik.controller import main

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
    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    app = create_app('ark.settings.%sConfig' % env.capitalize(), env=env)

    app.run()
