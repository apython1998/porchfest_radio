from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from app.models import Artist


class User(UserMixin, db.Document):
    username = db.StringField(unique=True)
    email = db.StringField(unique=True)
    password_hash = db.StringField()
    member_of = db.ListField(db.ReferenceField(Artist))
    follows = db.ListField(db.ReferenceField(Artist))

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
