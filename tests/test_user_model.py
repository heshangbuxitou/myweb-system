import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User, Post, Comment


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        User.generate_fake()
        Post.generate_fake(10)
        Comment.generate_fake()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)
