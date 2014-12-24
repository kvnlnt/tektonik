#! ../env/bin/python
# -*- coding: utf-8 -*-
from tektonik import create_app
from tektonik.models import db
from tektonik.models.property import Property


class TestURLs:

    def setup(self):

        # get app test config
        app = create_app('tektonik.settings.TestConfig', env='dev')

        # version url prefix
        self.prefix = '/properties'

        # create test app
        self.app = app.test_client()

        # set db app
        db.app = app

        db.init_app(app)

        # create all tables
        db.create_all()

        # create test record
        record = Property(property="test property")
        db.session.add(record)
        db.session.commit()
        self.record = record

        headers = [('Content-Type', 'application/json')]
        self.headers = headers

    def teardown(self):

        # destroy session and tables
        db.session.remove()
        db.drop_all()

    def test_list_properties(self):
        response = self.app.get(self.prefix)
        assert response.status_code == 200

    def test_create_property(self):
        data = '{"property":"test.com"}'
        response = self.app.post(self.prefix, data=data, headers=self.headers)
        assert response.status_code == 201

    def test_read_property(self):
        endpoint = self.prefix + '/' + str(self.record.id)
        response = self.app.get(endpoint, headers=self.headers)
        assert response.status_code == 200

    def test_update_property(self):
        endpoint = self.prefix + '/' + str(self.record.id)
        data = '{"property":"changed.com"}'
        response = self.app.put(endpoint, data=data, headers=self.headers)
        assert response.status_code == 200

    def test_delete_property(self):
        endpoint = self.prefix + '/' + str(self.record.id)
        response = self.app.delete(endpoint, headers=self.headers)
        assert response.status_code == 200
