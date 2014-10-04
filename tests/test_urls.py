#! ../env/bin/python
# -*- coding: utf-8 -*-
import json
import unittest
from tektonik import create_app
from tektonik.models import db, Property


class TestURLs:
    def setup(self):
        app = create_app('tektonik.settings.TestConfig', env='dev')
        self.app = app.test_client()
        db.app = app
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_properties_post(self):
        headers = [('Content-Type', 'application/json')]
        data = '{"property":"testing.com"}'
        response = self.app.post('/properties', data=data, headers=headers)
        assert response.status_code == 200

    def test_properties_get(self):

        record = Property(property="test property")
        db.session.add(record)
        db.session.commit()
        response = self.app.get('/properties')
        data = json.loads(response.data)
        assert data.get('data') != None
        assert response.status_code == 200
