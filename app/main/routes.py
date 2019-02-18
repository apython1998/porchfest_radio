from datetime import datetime
from app import db
from flask import render_template, url_for, redirect, flash, request, jsonify, current_app
from flask_login import current_user, login_required
from app.main import bp
from app.models import User, Location, Artist, Show, Porch, Porchfest


# Adds a user to a band
# user is of type User
# artist is of type Artist
def add_member(user, artist):
    user.member_of.append(artist)  # Add artist to list of bands that user is part of
    artist.members.append(user)  # Add user to list of members of a band
    user.save(cascade=True)
    artist.save(cascade=True)


# Removes a user from a band
# user is of type User
# artist is of type Artist
def remove_member(user, artist):
    user.member_of.remove(artist)  # Remove artist from list of bands that user is part of
    artist.members.remove(user)  # Remove user from list of members of a band
    user.save(cascade=True)
    artist.save(cascade=True)


# Adds artist to user's follows list
# user is of type User
# artist is of type Artist
def follow_band(user, artist):
    user.follows.append(artist)  # Add artist to list of bands that user follows
    artist.followers.append(user)  # Adds user to artist's list of followers
    user.save(cascade=True)
    artist.save(cascade=True)


# Allows user to unfollow artist
# user is of type User
# artist is of type Artist
def unfollow_band(user, artist):
    user.follows.remove(artist)  # Remove artist from list of bands that user follows
    artist.followers.remove(user)  # Remove user from artist's list of followers
    user.save(cascade=True)
    artist.save(cascade=True)


def add_objects():
    times = [
        datetime(2019, 6, 26, 9, 0, 0),  # start for porchfests
        datetime(2019, 6, 26, 17, 0, 0),  # end for porchfests
        datetime(2019, 6, 26, 12, 0, 0),  # first show end time
        datetime(2019, 6, 26, 15, 0, 0)  # second show end time
    ]
    default_users = [
        User(username='ithaca1', email='ithaca1@email.com', member_of=[], follows=[]),
        User(username='ithaca2', email='ithaca2@email.com', member_of=[], follows=[]),
        User(username='ithaca3', email='ithaca3@email.com', member_of=[], follows=[]),
    ]
    for user in default_users:
        user.set_password('default')
        user.save(cascade=True)
    default_locations = [
        Location(city='Ithaca', state='NY', zip_code='14850'),
    ]
    for location in default_locations:
        location.save(cascade=True)
    default_porches = [
        Porch(name='Ithaca Porch 1', email='ithacaPorch1@email.com', address='953 Danby Rd',
              location=Location.objects(city='Ithaca', state='NY').first(), time_slots=[times[2], times[3]]),
        Porch(name='Ithaca Porch 2', email='ithacaPorch2@email.com', address='123 Ithaca Rd',
              location=Location.objects(city='Ithaca', state='NY').first(), time_slots=[times[0], times[1], times[3]])
    ]
    for porch in default_porches:
        porch.save(cascade=True)
    default_artists = [
        Artist(name='Artist 1', description='artist 1 desc',
               media_links=[], location=Location.objects(city='Ithaca', state='NY').first(),
               image='https://miquon.org/wp-content/uploads/2016/02/GenericUser.png'),
        Artist(name='Artist 2', description='artist 2 desc',
               media_links=[], location=Location.objects(city='Ithaca', state='NY').first(),
               image='https://miquon.org/wp-content/uploads/2016/02/GenericUser.png')
    ]
    for artist in default_artists:
        artist.save(cascade=True)
    default_shows = [
        Show(artist=Artist.objects(name='Artist 1').first(), porch=Porch.objects(name='Ithaca Porch 1').first(),
             start_time=times[0], end_time=times[2]),
        Show(artist=Artist.objects(name='Artist 2').first(), porch=Porch.objects(name='Ithaca Porch 2').first(),
             start_time=times[2], end_time=times[3])
    ]
    for show in default_shows:
        show.save(cascade=True)
    default_porchfests = [
        Porchfest(location=Location.objects(city='Ithaca', state='NY').first(), start_time=times[0], end_time=times[1],
                  porches=[Porch.objects(name='Ithaca Porch 1').first(), Porch.objects(name='Ithaca Porch 2').first()],
                  shows=[Show.objects(artist=Artist.objects(name='Artist 1').first()).first(),
                         Show.objects(porch=Porch.objects(name='Ithaca Porch 2').first()).first()])
    ]
    for porchfest in default_porchfests:
        porchfest.save(cascade=True)


def make_default_user_connections():  # Used in reset_db() MUST CALL ADD_OBJECTS FIRST!!!
    user1 = User.objects(username='ithaca1').first()
    user2 = User.objects(username='ithaca2').first()
    artist1 = Artist.objects(name='Artist 1').first()
    add_member(user1, artist1)
    follow_band(user2, artist1)


@bp.route('/reset_db')
def reset_db():
    db.connection.drop_database('porchfest_radio')
    add_objects() # Add default objects
    make_default_user_connections() # Add connections between Users and Artists
    flash("Database has been reset!")
    return redirect(url_for('main.index'))


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/profile/<username>')
def profile(username):
    user = User.objects(username=username).first_or_404()
    return render_template('user.html',  user=user)


@bp.route('/edit_profile/<username>')
def edit_profile(username):
    pass


@bp.route('/artist/<artist_name>')
def artist(artist_name):
    pass