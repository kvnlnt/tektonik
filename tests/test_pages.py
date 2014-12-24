#! ../env/bin/python
# -*- coding: utf-8 -*-
from tektonik import create_app
from tektonik.models import db
from tektonik.models.page import Page


class TestURLs:

    def setup(self):

        # get app test config
        app = create_app('tektonik.settings.TestConfig', env='dev')

        # version url prefix
        self.prefix = '/pages'

        # create test app
        self.app = app.test_client()

        # init SQLAlchemy
        db.app = app

        # create all tables
        db.create_all()

        record = Page(page="test page")
        db.session.add(record)
        db.session.commit()
        self.record = record

        headers = [('Content-Type', 'application/json')]
        self.headers = headers

    def teardown(self):

        # destroy session and tables
        db.session.remove()
        db.drop_all()

    def test_list_pages(self):
        response = self.app.get(self.prefix)
        assert response.status_code == 200

    def test_create_page(self):
        data = '{"page":"test page"}'
        response = self.app.post(self.prefix, data=data, headers=self.headers)
        assert response.status_code == 201

    def test_read_page(self):
        endpoint = self.prefix + '/' + str(self.record.id)
        response = self.app.get(endpoint, headers=self.headers)
        assert response.status_code == 200

    def test_update_page(self):
        endpoint = self.prefix + '/' + str(self.record.id)
        data = '{"page":"changed"}'
        response = self.app.put(endpoint, data=data, headers=self.headers)
        assert response.status_code == 200

    def test_delete_page(self):
        endpoint = self.prefix + '/' + str(self.record.id)
        response = self.app.delete(endpoint, headers=self.headers)
        assert response.status_code == 200
