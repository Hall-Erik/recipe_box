import unittest
from unittest import TestCase
from recipebox import create_app, db
from recipebox.models import User
from recipebox.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'splite://'

class UserModelTestCase(TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hash(self):
        user = User(username='Steve')
        user.set_password('blah')
        self.assertTrue(user.check_password('blah'))
        self.assertFalse(user.check_password('derp'))

    def test_password_reset_token(self):
        user = User(username='Steve', email='s@s.com')
        user2 = User(username='NotSteve', email='ns@ns.com')
        user.set_password('blah')
        user2.set_password('notblah')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

        token = user.get_reset_token()
        self.assertEqual(type(token), str)
        self.assertEqual(User.verify_reset_token(token), user)
        self.assertNotEqual(User.verify_reset_token(token), user2)

if __name__ == '__main__':
    unittest.main(verbosity=2)