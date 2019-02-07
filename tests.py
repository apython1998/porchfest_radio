from datetime import datetime, timedelta
import unittest
from app import create_app, db
# from app.models import
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

    # test shit here