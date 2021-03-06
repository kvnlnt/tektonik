#! ../env/bin/python
import os

from flask import Flask
from flask.ext.cors import CORS
from tektonik.controllers.pages import blueprint as pages_blueprint
from tektonik.controllers.paths import blueprint as paths_blueprint
from tektonik.controllers.path_pages import blueprint as path_pages_blueprint
from tektonik.controllers.properties import blueprint as properties_blueprint
from tektonik.models import db


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
    app.register_blueprint(properties_blueprint, url_prefix='/properties')
    app.register_blueprint(paths_blueprint, url_prefix='/paths')
    app.register_blueprint(pages_blueprint, url_prefix='/pages')
    app.register_blueprint(path_pages_blueprint, url_prefix='/path_pages')

    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    app = create_app('tektonik.settings.%sConfig' % env.capitalize(), env=env)

    app.run()
