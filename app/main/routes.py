from datetime import datetime
from app import db
from flask import render_template, url_for, redirect, flash, request, jsonify, current_app
from flask_login import current_user, login_required
from app.main import bp
from app.models import User, Location, Artist, Show, Porch, Porchfest


@bp.route('/reset_db')
def reset_db():
    db.connection.drop_database('porchfest_radio')
    times = [
        datetime(2019, 12, 26, 9, 0, 0),  # start for porchfests
        datetime(2019, 12, 26, 17, 0, 0),  # end for porchfests
        datetime(2019, 12, 26, 12, 0, 0),  # first show end time
        datetime(2019, 12, 26, 15, 0, 0)  # second show end time
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
        Artist(email='artist1@email.com', name='Artist 1', description='artist 1 desc',
               media_links=[], location=Location.objects(city='Ithaca', state='NY').first(),
               image='https://miquon.org/wp-content/uploads/2016/02/GenericUser.png'),
        Artist(email='artist2@email.com', name='Artist 2', description='artist 2 desc',
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
    flash("Database has been reset!")
    return redirect(url_for('main.index'))


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')