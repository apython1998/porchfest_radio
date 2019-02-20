from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, SelectField, SelectMultipleField
from wtforms.fields.html5 import DateTimeField, DateField, DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, length, URL, Optional
from app.models import User, Artist, Location, Porch, Porchfest
from bson.objectid import ObjectId
from datetime import datetime


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None and current_user.email != user.email:
            raise ValidationError('Email already being used!')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None and current_user.username != user.username:
            raise ValidationError('Username is already being used!')