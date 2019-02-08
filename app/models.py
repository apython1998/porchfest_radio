from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from app.auth.models import User


class Location(db.Document):
    city = db.StringField()
    state = db.StringField()
    zip_code = db.StringField(max_length=5)
    meta = {
        'indexes': [
            {'fields': ('city', 'state', 'zip_code'), 'unique': True}
        ]
    }

    def __repr__(self):
        return '<Location {}, {}>'.format(self.city, self.state)


class Artist(db.Document):
    name = db.StringField(unique=True)
    description = db.StringField()
    media_links = db.ListField(db.StringField())
    location = db.ReferenceField(Location)
    image = db.StringField()
    genre = db.StringField()
    members = db.ListField(db.ReferenceField(User))

    def __repr__(self):
        return '<Artist {}>'.format(self.name)


class Porch(db.Document):
    name = db.StringField()
    email = db.StringField(unique=True)
    address = db.StringField()
    location = db.ReferenceField(Location)
    time_available_start = db.DateTimeField(default=datetime.utcnow)
    time_available_end = db.DateTimeField(default=datetime.utcnow)
    time_slots = db.ListField(db.DateTimeField())
    meta = {
        'indexes': [
            {'fields': ('address', 'location'), 'unique': True}
        ]
    }

    def __repr__(self):
        return '<Porch {}>'.format(self.name)


class Show(db.Document):
    artist = db.ReferenceField(Artist)
    porch = db.ReferenceField(Porch)
    start_time = db.DateTimeField(default=datetime.utcnow)
    end_time = db.DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': [
            {'fields': ('artist', 'start_time'), 'unique': True}
        ]
    }

    def __repr__(self):
        return '<Show {} playing @ {}>'.format(self.artist.name, self.porch.address)


class Porchfest(db.Document):
    location = db.ReferenceField(Location)
    start_time = db.DateTimeField(default=datetime.utcnow)
    end_time = db.DateTimeField(default=datetime.utcnow)
    porches = db.ListField(db.ReferenceField(Porch, reverse_delete_rule=db.CASCADE))
    shows = db.ListField(db.ReferenceField(Show, reverse_delete_rule=db.CASCADE))
    lat = db.StringField()
    long = db.StringField()
    meta = {
        'indexes': [
            {'fields': ('location', 'start_time'), 'unique': True}
        ]
    }

    def __repr__(self):
        return '<Porchfest in {}, {}>'.format(self.location.city, self.location.state)