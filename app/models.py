from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Document):
    username = db.StringField(unique=True)
    email = db.StringField(unique=True)
    password_hash = db.StringField()
    name = db.StringField()
    member_of = db.ListField(db.ReferenceField('Artist'))
    follows = db.ListField(db.ReferenceField('Artist'))

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.objects(id=id).first()


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


class Genre(db.Document):
    name = db.StringField(unique=True)


class Track(db.Document):
    artist = db.ReferenceField('Artist')
    title = db.StringField()
    duration = db.IntField()
    filepath = db.StringField(unique=True)


class Artist(db.Document):
    name = db.StringField(unique=True)
    description = db.StringField()
    location = db.ReferenceField(Location)
    genre = db.ListField(db.ReferenceField(Genre))
    members = db.ListField(db.ReferenceField(User))
    followers = db.ListField(db.ReferenceField(User))
    tracks = db.ListField(db.ReferenceField(Track))

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
