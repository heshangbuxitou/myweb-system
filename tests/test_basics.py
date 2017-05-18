import unittest
from flask import current_app
from app import create_app, db, models

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)
        
    def test_app_is_testing(self):
        self.assertFalse(current_app.config['TESTING'])