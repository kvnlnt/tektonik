#! ../env/bin/python
# -*- coding: utf-8 -*-
from tektonik import create_app
from tektonik.models import db, Property


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
        record = Property(property="test property")
        db.session.add(record)
        db.session.commit()

    def teardown(self):

        # destroy session and tables
        db.session.remove()
        db.drop_all()

    def test_properties_create(self):

        headers = [('Content-Type', 'application/json')]
        data = '{"property":"testing.com"}'
        response = self.app.post('/properties', data=data, headers=headers)
        assert response.status_code == 200

    def test_properties_read(self):

        response = self.app.get('/properties')
        assert response.status_code == 200

    def test_properties_update(self):

        headers = [('Content-Type', 'application/json')]
        data = '{"id":1, "property":"updated"}'
        response = self.app.put('/properties', data=data, headers=headers)
        assert response.status_code == 200

    def test_properties_delete(self):

        headers = [('Content-Type', 'application/json')]
        data = '{"id":1}'
        response = self.app.delete('/properties', data=data, headers=headers)
        assert response.status_code == 200

    def test_property_read(self):

        response = self.app.get('/properties/1')
        assert response.status_code == 200

    def test_property_update(self):

        headers = [('Content-Type', 'application/json')]
        data = '{"property":"updated"}'
        response = self.app.put('/properties/1', data=data, headers=headers)
        assert response.status_code == 200

    def test_property_delete(self):

        headers = [('Content-Type', 'application/json')]
        response = self.app.delete('/properties/1', headers=headers)
        assert response.status_code == 200
