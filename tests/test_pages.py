#! ../env/bin/python
# -*- coding: utf-8 -*-
from tektonik import create_app
from tektonik.models import db, Page


class TestURLs:

    def setup(self):

        # get app test config
        app = create_app('tektonik.settings.TestConfig', env='dev')

        # create test app
        self.app = app.test_client()

        # set db app
        db.app = app

        # create all tables
        db.create_all()

        # create test record
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

    def test_pages_post(self):
        data = '{"page":"/testpage"}'
        endpoint = '/pages'
        response = self.app.post(endpoint, data=data, headers=self.headers)
        assert response.status_code == 201

    def test_pages_get(self):
        endpoint = '/pages'
        response = self.app.get(endpoint)
        assert response.status_code == 200

    def test_page_get(self):
        endpoint = '/pages/' + str(self.record.id)
        response = self.app.get(endpoint, headers=self.headers)
        assert response.status_code == 200

    def test_page_put(self):
        endpoint = '/pages/' + str(self.record.id)
        data = '{"page":"/changed"}'
        response = self.app.put(endpoint, data=data, headers=self.headers)
        assert response.status_code == 200

    def test_page_delete(self):
        endpoint = '/pages/' + str(self.record.id)
        response = self.app.delete(endpoint, headers=self.headers)
        assert response.status_code == 204
