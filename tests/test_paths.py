#! ../env/bin/python
# -*- coding: utf-8 -*-
from tektonik import create_app
from tektonik.models import db
from tektonik.models import Path
from tektonik.models import Property


class TestURLs:

    def setup(self):

        # get app test config
        app = create_app('tektonik.settings.TestConfig', env='dev')

        # version url prefix
        self.prefix = '/paths'

        # create test app
        self.app = app.test_client()

        # set db app
        db.app = app

        # create all tables
        db.create_all()

        # create test record
        property = Property(property="test property")
        db.session.add(property)
        db.session.commit()
        self.property = property

        record = Path(path="testpath", property_id=property.id)
        db.session.add(record)
        db.session.commit()
        self.record = record

        headers = [('Content-Type', 'application/json')]
        self.headers = headers

    def teardown(self):

        # destroy session and tables
        db.session.remove()
        db.drop_all()

    def test_create_path(self):
        property_id = str(self.property.id)
        data = '{"path":"test.com", "property_id":' + property_id + '}'
        response = self.app.post(self.prefix, data=data, headers=self.headers)
        assert response.status_code == 201

    def test_read_paths(self):
        response = self.app.get(self.prefix)
        assert response.status_code == 200

    def test_read_path(self):
        endpoint = self.prefix + '/' + str(self.record.id)
        response = self.app.get(endpoint, headers=self.headers)
        assert response.status_code == 200

    def test_update_path(self):
        property_id = str(self.property.id)
        endpoint = self.prefix + '/' + str(self.record.id)
        data = '{"path":"changed", "property_id":' + property_id + '}'
        response = self.app.put(endpoint, data=data, headers=self.headers)
        assert response.status_code == 200

    def test_delete_path(self):
        endpoint = self.prefix + '/' + str(self.record.id)
        response = self.app.delete(endpoint, headers=self.headers)
        assert response.status_code == 200
