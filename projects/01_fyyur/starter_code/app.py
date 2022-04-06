#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI
from models import Venue, Artist, Show, db
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# available in models.py
  
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Endpoint to retrieve all the venues
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  locations = db.session.query(Venue.city, Venue.state).all()
  
  data = []
  for location in locations :
    venues = db.session.query(Venue.id, Venue.name, Venue.upcoming_shows_count).filter(Venue.city==location[0], Venue.state==location[1]).all()
    data.append({
      "city": location[0],
      "state": location[1],
      "venues": []
    })

    for venue in venues :
      data[-1]["venues"].append({
        "id":venue[0],
        "name": venue[1],
        "num_upcoming_shows": venue[2]
      })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # End point to serach venues. This returns the result with case-insensitive.
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form['search_term']
  search_results = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  response = {
    "count": len(search_results),
    "data" :[]
  }
  for venue in search_results:
    response["data"].append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": venue.upcoming_shows_count
    })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # Endpoint for displaying venue details based on venue id
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  shows = venue.shows
  past_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
  upcoming_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()
  
  past_shows_data = []
  upcoming_shows_data = []
  for show in upcoming_shows:
    artist_details = {
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    upcoming_shows_data.append(artist_details)
  for show in past_shows:
    artist_details = {
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    past_shows_data.append(artist_details)
  data={
    "id": venue.id,
    "name":venue.name,
    "genres":venue.genres,
    "address":venue.address,
    "city":venue.city,
    "state":venue.state,
    "phone":venue.phone,
    "website":venue.website,
    "facebook_link":venue.facebook_link,
    "seeking_talent":venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link":venue.image_link,
    "past_shows":past_shows_data,
    "upcoming_shows":upcoming_shows_data,
    "past_shows_count":len(past_shows_data),
    "upcoming_shows_count":len(upcoming_shows_data)
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # Endpoint for creating new Venue
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    form = VenueForm(request.form)
    form.validate()
    new_venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      facebook_link=form.facebook_link.data,
      image_link=form.image_link.data,
      website=form.website_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data 
    )
    db.session.add(new_venue)
    db.session.commit()
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    error: True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  if error:
    abort(400)
  else :
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # End point for deleting the venue
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  if request.method == 'DELETE':
    try:
      Venue.query.filter(id == venue_id).delete()
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # End point for getting all the artists
  # TODO: replace with real data returned from querying the database
  data = Artist.query.with_entities(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Endpoint for searching artists. This works with case-insensitive.
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form['search_term']
  search_results = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  response = {
    "count": len(search_results),
    "data" :[]
  }
  for artist in search_results:
    response["data"].append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": artist.upcoming_shows_count
    })
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # Endpoint for retrieving artist based on artist Id
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artists = Artist.query.get(artist_id)
  shows = artists.shows
  past_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artists.id).filter(Show.start_time<datetime.now()).all()
  upcoming_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artists.id).filter(Show.start_time>datetime.now()).all()

  past_shows_data = []
  upcoming_shows_data = []
  for show in past_shows:
    venue_details = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    past_shows_data.append(venue_details)
  for show in upcoming_shows:
    venue_details = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    upcoming_shows_data.append(venue_details)
  data={
    "id": artists.id,
    "name":artists.name,
    "genres":artists.genres,
    "city":artists.city,
    "state":artists.state,
    "phone":artists.phone,
    "website":artists.website,
    "facebook_link":artists.facebook_link,
    "seeking_venue":artists.seeking_venue,
    "seeking_description":artists.seeking_description,
    "image_link":artists.image_link,
    "past_shows":past_shows_data,
    "upcoming_shows":upcoming_shows_data,
    "past_shows_count":len(past_shows_data),
    "upcoming_shows_count":len(upcoming_shows_data)
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # End point for editing artist details based on the data available in db
  form = ArtistForm()
  artist_data = Artist.query.get(artist_id)

  artist={
    "id": artist_data.id,
    "name": artist_data.name,
    "genres": artist_data.genres,
    "city": artist_data.city,
    "state": artist_data.state,
    "phone": artist_data.phone,
    "website": artist_data.website,
    "facebook_link": artist_data.facebook_link,
    "seeking_venue": artist_data.seeking_venue,
    "seeking_description": artist_data.seeking_description,
    "image_link": artist_data.image_link
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # Endpoint for editing the artist based on the details submitted from UI
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = db.session.query(Artist).filter_by(id=artist_id).first()
  form = ArtistForm(request.form)
  try:
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.website =form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    db.session.commit()
    flash("Artist {} updated successfully".format(artist.name))
  except :
    db.session.rollback()
    flash("Error updated Artist {}".format(artist.name))
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_data = Venue.query.get(venue_id)

  venue={
    "id": venue_data.id,
    "name": venue_data.name,
    "genres": venue_data.genres,
    "address": venue_data.address,
    "city": venue_data.city,
    "state": venue_data.state,
    "phone": venue_data.phone,
    "website": venue_data.website,
    "facebook_link": venue_data.facebook_link,
    "seeking_talent": venue_data.seeking_talent,
    "seeking_description": venue_data.seeking_description,
    "image_link": venue_data.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
# Endpoint for editing the venue based on the details submitted from UI
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = db.session.query(Venue).filter_by(id=venue_id).first()
  form = VenueForm(request.form)
  try:
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.genres = form.genres.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.website =form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    db.session.commit()
    flash("Venue {} updated successfully".format(venue.name))
  except :
    db.session.rollback()
    flash("Error while updating Venue {}".format(venue.name))
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # End point for craeting artists
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  form.validate()
  try:
    artist = Artist(
      name = form.name.data,
      city = form.name.data,
      state = form.state.data,
      phone = form.phone.data,
      genres = form.genres.data,
      facebook_link = form.facebook_link.data,
      image_link = form.image_link.data,
      website = form.website_link.data,
      seeking_venue = form.seeking_venue.data,
      seeking_description = form.seeking_description.data,
    )
    db.session.add(artist)
    db.session.commit()
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # Endpoint for displaying list of shows
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  data = []

  for show in shows:
    show_detail = {
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist_id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link ,
    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    data.append(show_detail)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  #End point for creating the show
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  form.validate()
  # new_show = Show()
  # new_show.artist_id = request.form['artist_id']
  # new_show.venue_id = request.form['venue_id']
  # new_show.start_time = request.form['start_time']

  try:
    new_show = Show(
      artist_id = form.artist_id.data,
      venue_id = form.venue_id.data,
      start_time = form.start_time.data.strftime("%m/%d/%Y, %H:%M:%S"),
    )
    db.session.add(new_show)
    db.session.commit()
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
