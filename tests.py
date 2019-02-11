from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Artist, Show, Porch, Porchfest, Location
from config import Config
from app.main.routes import add_objects, make_default_user_connections, reset_db


class TestConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
            'db': 'porchfest_radio_test',
            'host': 'mongodb://localhost/porchfest_radio_test'
        }


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='ab', email='a@b.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))


class ResetDBCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_add_objects(self):
        db.connection.drop_database('porchfest_radio_test')
        add_objects()
        u1 = User.objects(username='ithaca1').first()
        self.assertIsNotNone(u1) # default user added
        a1 = Artist.objects(name='Artist 1').first()
        self.assertIsNotNone(a1)  # default artist added

    def test_make_user_connections(self):
        db.connection.drop_database('porchfest_radio_test')
        add_objects()
        make_default_user_connections()
        u1 = User.objects(username='ithaca1').first()
        u2 = User.objects(username='ithaca2').first()
        a1 = Artist.objects(name='Artist 1').first()
        # u1 is in band a1
        self.assertTrue(u1 in a1.members)
        self.assertTrue(a1 in u1.member_of)
        # u2 is NOT in band a1
        self.assertFalse(u2 in a1.members)
        self.assertFalse(a1 in u2.member_of)
        # u2 follows band a1
        self.assertTrue(u2 in a1.followers)
        self.assertTrue(a1 in u2.follows)
        # u1 does not follow band a1
        self.assertFalse(u1 in a1.followers)
        self.assertFalse(a1 in u1.follows)


if __name__ == '__main__':
    unittest.main(verbosity=2)