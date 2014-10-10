#! ../env/bin/python
# -*- coding: utf-8 -*-
from tektonik import create_app
from tektonik.models import db, Path


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
        record = Path(path="test path")
        db.session.add(record)
        db.session.commit()
        self.record = record

        headers = [('Content-Type', 'application/json')]
        self.headers = headers

    def teardown(self):

        # destroy session and tables
        db.session.remove()
        db.drop_all()

    def test_paths_post(self):
        data = '{"path":"/testpath", "pages":[]}'
        endpoint = '/paths'
        response = self.app.post(endpoint, data=data, headers=self.headers)
        assert response.status_code == 201

    def test_paths_get(self):
        endpoint = '/paths'
        response = self.app.get(endpoint)
        assert response.status_code == 200

    def test_path_get(self):
        endpoint = '/paths/' + str(self.record.id)
        response = self.app.get(endpoint, headers=self.headers)
        assert response.status_code == 200

    def test_path_put(self):
        endpoint = '/paths/' + str(self.record.id)
        data = '{"path":"/changed", "property_id":1}'
        response = self.app.put(endpoint, data=data, headers=self.headers)
        assert response.status_code == 200

    def test_path_delete(self):
        endpoint = '/paths/' + str(self.record.id)
        response = self.app.delete(endpoint, headers=self.headers)
        assert response.status_code == 204
