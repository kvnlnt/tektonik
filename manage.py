#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from tektonik import create_app
from tektonik.models import db
from tektonik.models.page import Page
from tektonik.models.path import Path
from tektonik.models.path_page import PathPage
from tektonik.models.property import Property
from tektonik.schemas.page import Page as PageSchema
from tektonik.schemas.path import Path as PathSchema
from tektonik.schemas.path_page import PathPage as PathPageSchema
from tektonik.schemas.property import Property as PropertySchema

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('tektonik.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app,
                db=db,
                Property=Property,
                PropertySchema=PropertySchema,
                Path=Path,
                PathSchema=PathSchema,
                PathPage=PathPage,
                PathPageSchema=PathPageSchema,
                Page=Page,
                PageSchema=PageSchema)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your Alchemy models
    """

    db.create_all()


@manager.command
def recreatedb():
    """ Creates a database with all of the tables defined in
        your Alchemy models
    """
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    manager.run()
