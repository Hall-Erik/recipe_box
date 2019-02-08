import unittest
from unittest import TestCase
from recipebox import app, db
from recipebox.models import User

class UserModelTestCase(TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hash(self):
        user = User(username='Steve')
        user.set_password('blah')
        self.assertTrue(user.check_password('blah'))
        self.assertFalse(user.check_password('derp'))


if __name__ == '__main__':
    unittest.main(verbosity=2)