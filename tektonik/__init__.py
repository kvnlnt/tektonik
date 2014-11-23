#! ../env/bin/python
import os

from flask import Flask
from flask.ext.cors import CORS
from tektonik.models import db
from tektonik.v1_0.properties import api


def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. tektonik.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)
    app.config.from_object(object_name)
    app.config['ENV'] = env

    # config cors
    CORS(app, headers='Content-Type')

    #init SQLAlchemy
    db.init_app(app)

    # register blueprints
    app.register_blueprint(api, url_prefix='/v1_0')

    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    app = create_app('tektonik.settings.%sConfig' % env.capitalize(), env=env)

    app.run()
