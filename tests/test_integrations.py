#! ../env/bin/python
# -*- coding: utf-8 -*-
from tektonik import create_app
from tektonik.models import db
from tektonik.models.persona import betty_crocker
from tektonik.models.property import Property
from tektonik.models.path import Path
from tektonik.models.page import Page
from tektonik.models.path_page import PathPage


class TestIntegration:

    def setup(self):

        # get app test config
        app = create_app('tektonik.settings.TestConfig', env='dev')

        # create test app
        self.app = app.test_client()

        # init SQLAlchemy
        db.app = app

        # create all tables
        db.create_all()

    def teardown(self):

        # destroy session and tables
        db.session.remove()
        db.drop_all()

    def load_persona(self, persona):

        for property in persona:

            # add property
            _property = Property(property=property['property'])
            db.session.add(_property)
            db.session.commit()

            # add paths
            for path in property['paths']:
                _path = Path(path=path['path'], property_id=_property.id)
                db.session.add(_path)
                db.session.commit()

            # get all paths
            paths = Path.query.all()

            # add pages
            for page in property['pages']:
                _page = Page(page=page['page'])
                db.session.add(_page)
                db.session.commit()

            # get all pages
            pages = Page.query.all()

            # connect paths and pages
            for path_page in property['path_pages']:
                path_id = paths[path_page['path']].id
                page_id = pages[path_page['page']].id
                _path_page = PathPage(path_id=path_id, page_id=page_id)
                db.session.add(_path_page)
                db.session.commit()

    def test_betty_crocker(self):
        self.load_persona(betty_crocker)
