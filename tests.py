from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Artist, Show, Porch, Porchfest, Location
from config import Config


class TestConfig(Config):
    TESTING = True
    # MONGODB_SETTINGS = {
    #         'db': 'porchfest_radio_test',
    #         'host': 'mongodb://localhost/porchfest_radio_test'
    #     }


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


if __name__ == '__main__':
    unittest.main(verbosity=2)