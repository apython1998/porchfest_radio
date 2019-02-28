import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGODB_SETTINGS = {
        'db': 'porchfest_radio',
        'host': 'mongodb://localhost/porchfest_radio'
    }
    ADMINS = os.environ.get('ADMINS') or 'your.email@example.com'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads/'
    S3_BUCKET = os.environ.get('S3_BUCKET_NAME') or None
    S3_KEY = os.environ.get('S3_KEY') or None
    S3_SECRET = os.environ.get('S3_SECRET_ACCESS_KEY') or None