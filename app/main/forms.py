from flask_wtf import FlaskForm
from flask_login import current_user
from flask import current_app
from wtforms import StringField, TextAreaField, SubmitField, SelectField, SelectMultipleField, MultipleFileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, length, URL, Optional, Regexp
from flask_wtf.file import FileRequired, FileAllowed, FileField
from app.models import User, Artist, Location, Porch, Porchfest, Track
from bson.objectid import ObjectId
from datetime import datetime
import os


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


class CreateArtistForm(FlaskForm):
    name = StringField('Band Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    genre = SelectMultipleField('Pick 3 Genres', validators=[DataRequired()], coerce=ObjectId)
    location = SelectField('Location', validators=[DataRequired()], coerce=ObjectId)
    submit = SubmitField('Register')

    def validate_zip(self, zip):
        for c in zip.data:
            if c.isalpha():
                raise ValidationError('Zip code must consist of only integers')

    def validate_genre(self, genre):
        if len(genre.data) > 3:
            raise ValidationError('You can only select 3 genres for your band')


class EditArtistForm(FlaskForm):
    name = StringField('Band Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    genre = SelectMultipleField('Pick 3 Genres', validators=[DataRequired()], coerce=ObjectId)
    location = SelectField('Location', validators=[DataRequired()], coerce=ObjectId)
    submit = SubmitField('Submit')

    def validate_zip(self, zip):
        for c in zip.data:
            if c.isalpha():
                raise ValidationError('Zip code must consist of only integers')

    def validate_genre(self, genre):
        if len(genre.data) > 3:
            raise ValidationError('You can only select 3 genres for your band')


class UploadTrackForm(FlaskForm):
    track_name = StringField('Track Name', validators=[DataRequired()])
    genre = SelectMultipleField('Pick 3 Genres', validators=[DataRequired()], coerce=ObjectId)
    track = FileField('Upload a Track', validators=[FileRequired(), FileAllowed(['mp3', 'wav'], 'Only Music Files')])
    upload = SubmitField('Upload')

    def validate_track(self, track):
        if Track.objects(filepath=os.path.join(current_app.config['UPLOAD_FOLDER'], track.data.filename)).first() is not None:
            raise ValidationError('That file already exists')

    def validate_track_name(self, track_name):
        if Track.objects(track_name=track_name.data).first() is not None:
            raise ValidationError('Track with that name already exists')

    def validate_genre(self, genre):
        if len(genre.data) > 3:
            raise ValidationError('You can only select 3 genres for your band')
