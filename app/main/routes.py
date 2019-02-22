from datetime import datetime
from app import db
from flask import render_template, url_for, redirect, flash, request, jsonify, current_app
from flask_login import current_user, login_required
from app.main import bp
from app.models import User, Location, Artist, Show, Porch, Porchfest, Genre
from app.main.forms import EditProfileForm, CreateArtistForm, EditArtistForm
from selenium import webdriver


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
        User(username='ithaca1', email='ithaca1@email.com', name='Ithaca One', member_of=[], follows=[]),
        User(username='ithaca2', email='ithaca2@email.com', name='Ithaca Two', member_of=[], follows=[]),
        User(username='ithaca3', email='ithaca3@email.com', name='Ithaca Three', member_of=[], follows=[]),
    ]
    for user in default_users:
        user.set_password('default')
        user.save(cascade=True)
    default_locations = [
        Location(city='Ithaca', state='NY', zip_code='14850'),
        Location(city='Albany', state='NY', zip_code='12203'),
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
               location=Location.objects(city='Ithaca', state='NY').first()),
        Artist(name='Artist 2', description='artist 2 desc',
               location=Location.objects(city='Ithaca', state='NY').first())
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


def scrape_genres(url):
    browser = webdriver.Chrome()
    browser.get(url)
    genres = []
    genres_divs = browser.find_elements_by_class_name('hFvVJe')
    for column in genres_divs:
        genre_links = column.find_elements_by_tag_name('a')
        for genre_link in genre_links:
            genres.append(genre_link.text)
    print(len(genres))
    return genres


def get_genres():  # Used in reset_db() to get genres using a google search
    genre_list = scrape_genres('https://www.google.com/search?q=music+genres&rlz=1C5CHFA_enUS738US738&oq=music+genres&aqs=chrome..69i57j69i60j0l4.1688j0j7&sourceid=chrome&ie=UTF-8')
    for genre in genre_list:
        new_genre = Genre(name=genre)
        new_genre.save(cascade=True)


@bp.route('/reset_db')
def reset_db():
    db.connection.drop_database('porchfest_radio')
    get_genres() # Reset the genres for the system
    add_objects() # Add default objects
    make_default_user_connections() # Add connections between Users and Artists
    flash("Database has been reset!")
    return redirect(url_for('main.index'))


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Porchfest')


@bp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.objects(username=username).first_or_404()
    return render_template('user.html',  user=user, title='{} Page'.format(username))


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.save()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/artist/<artist_name>')
def artist(artist_name):
    artist = Artist.objects(name=artist_name).first_or_404()
    shows_for_artist = Show.objects(artist=artist, start_time__gt=datetime.utcnow)
    return render_template('artist.html', artist=artist, shows=shows_for_artist, title='{} Info'.format(artist.name))


@bp.route('/create_artist', methods=['GET', 'POST'])
@login_required
def create_artist():
    form = CreateArtistForm()
    form.location.choices = [(location.id, location.city + ', ' + location.state) for location in Location.objects()]
    form.genre.choices = [(genre.id, genre.name) for genre in Genre.objects.order_by('name')]
    if form.validate_on_submit():
        user = User.objects(username=current_user.username).first()
        location = Location.objects(id=form.location.data).first()
        genres = []
        for genre_id in form.genre.data:
            genres.append(Genre.objects(id=genre_id).first())
        artist = Artist(name=form.name.data, description=form.description.data, location=location,
                        genre=genres)
        artist.save(cascade=True)
        add_member(user, artist)
        flash('Artist {} was created'.format(artist.name))
        return redirect(url_for('main.artist', artist_name=artist.name))
    return render_template('create_artist.html', form=form, title='Create Artist')


@bp.route('/edit_artist/<artist_name>', methods=['GET', 'POST'])
@login_required
def edit_artist(artist_name):
    artist = Artist.objects(name=artist_name).first_or_404()
    if current_user not in artist.members:
        flash('You are not authorized to edit {}\'s information'.format(artist.name))
        return redirect(url_for('main.artist', artist_name=artist.name))
    form = EditArtistForm()
    form.location.choices = [(location.id, location.city + ', ' + location.state) for location in Location.objects()]
    form.genre.choices = [(genre.id, genre.name) for genre in Genre.objects.order_by('name')]
    if form.validate_on_submit():
        artist.name = form.name.data
        artist.description = form.description.data
        artist.location = Location.objects(id=form.location.data).first()
        artist.genre = [Genre.objects(id=genre).first() for genre in form.genre.data]
        artist.save(cascade=True)
        flash('{} Edits Complete'.format(artist.name))
        return redirect(url_for('main.artist', artist_name=artist.name))
    elif request.method == 'GET':
        form.name.data = artist.name
        form.description.data = artist.description
        form.genre.data = [genre.id for genre in artist.genre]
        form.location.data = artist.location.id
    return render_template('edit_artist.html', form=form, title='Edit {}'.format(artist.name))
