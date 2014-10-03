#! ../env/bin/python
# -*- coding: utf-8 -*-
import json
from tektonik import create_app
from tektonik.models import db



class TestURLs:
    def setup(self):
        app = create_app('tektonik.settings.TestConfig', env='dev')
        self.app = app.test_client()
        db.app = app
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_properties(self):
        response = self.app.get('/properties')
        data = json.loads(response.data)
        assert data.get('data') != None
        assert response.status_code == 200
