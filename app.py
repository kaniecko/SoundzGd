from flask import Flask, render_template, flash, redirect, url_for
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine, text
from sqlalchemy import insert
from forms import RegistrationForm, LoginForm, BandForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'irEALLYdONTkNOWwHATiAMdOING'

meta = MetaData()
DATABASE_URL = "cockroachdb://lukas:8S5jNP4SEeQyNThMB2xPvA@ninth-warrior-8275.7tt.cockroachlabs.cloud:26257/SoundzGd?sslmode=verify-full"
engine = create_engine(DATABASE_URL)
conn = engine.connect()
artist = Table(
   'artist', meta,
   Column('artist_id', Integer, primary_key = True, nullable=False),
   Column('artist_name', String, nullable=False),
   Column('artist_bio', String(250), nullable=False),
   Column('username', String, nullable=False, unique=True),
   Column('password', String, nullable=False),
   Column('youtube_link', String, nullable=False),
   Column('email', String, nullable=False),
   Column('genre_id', Integer, nullable=False),
   Column('band_lead', Integer, nullable=False),
   Column('band_id', Integer, nullable=False),
   Column('instrument_id', Integer, nullable=False),
)
band = Table(
   'band', meta,
   Column('band_id', Integer, primary_key = True, nullable=False),
   Column('band_name', String, nullable=False),
   Column('band_bio', String(250), nullable=False),
   Column('genre_id', Integer, nullable=False),
   Column('song_id', Integer, nullable=False),
)
genre = Table(
   'genre', meta,
   Column('genre_id', Integer, primary_key = True, nullable=False),
   Column('genre_name', String, nullable=False),
)
instrument = Table(
   'instrument', meta,
   Column('instrument_id', Integer, primary_key = True, nullable=False),
   Column('instrument_name', String, nullable=False),
)
song = Table(
   'song', meta,
   Column('song_id', Integer, primary_key = True, nullable=False),
   Column('song_name', String, nullable=False),
)

# just to create all tables initially
def create_all_tables():
    meta.create_all(engine)

# to make a new artist
def create_artist(id, name, bio, user, passw, yt_link, a_email, g_id, is_band_lead, b_id, i_id):
        stmt = (
                insert(artist).
                values(artist_id=id, artist_name=name, artist_bio=bio, username=user, password=passw, youtube_link=yt_link, email=a_email, genre_id=g_id, band_lead=is_band_lead, band_id=b_id, instrument_id=i_id)
        )
        conn.execute(stmt)

def create_band(id, name, bio, g_id, s_id):
        stmt = (
                insert(band).
                values(band_id=id, band_name=name, band_bio=bio, genre_id=g_id, song_id=s_id)
        )
        conn.execute(stmt)

def create_song(id, name):
        stmt = (
                insert(song).
                values(song_id=id, song_name=name)
        )
        conn.execute(stmt)

def create_instrument(id, name):
        stmt = (
                insert(instrument).
                values(instrument_id=id, instrument_name=name)
        )
        conn.execute(stmt)

def create_genre(id, name):
        stmt = (
                insert(genre).
                values(genre_id=id, genre_name=name)
        )
        conn.execute(stmt)

def get_all_artists():
        select_command = artist.select()
        rows = conn.execute(select_command)
        return rows

# artist check
def is_artist(id):
        query = artist.select().where(artist.c.artist_id==id)
        rows = conn.execute(query).fetchall()
        if len(rows) == 0:
                return False
        else:
                return True

def get_artist_from_id(id):
        str_sql = text("""select artist.artist_name, artist.artist_bio, artist.username, band.band_name, genre.genre_name, instrument.instrument_name, artist.youtube_link
                     from artist 
                     join band on band.band_id = artist.band_id
                     join genre on genre.genre_id = artist.genre_id
                     join instrument on instrument.instrument_id = artist.instrument_id
                     where artist.artist_id = :a_id""")
        rows = conn.execute(str_sql, a_id=id).fetchone()
        array = []
        for row in rows:
                array.append(str(row))
        return array

def get_artists_by_instrument(instrument_id):
        str_sql = text("""select artist.artist_name, artist.artist_id
                     from artist
                     where artist.instrument_id = :a_id""")
        rows = conn.execute(str_sql, a_id=instrument_id).fetchone()
        if rows is not None:
                return rows
        else:
                return ()

def get_artists_by_genre(genre_id):
        str_sql = text("""select artist.artist_name, artist.artist_id
                     from artist
                     where artist.genre = :a_id""")
        rows = conn.execute(str_sql, a_id=genre_id).fetchone()
        if rows is not None:
                return rows
        else:
                return ()

def is_unique_email(email):
        str_sql = text("""select artist.email
                     from artist
                     where artist.email = :a_id""")
        rows = conn.execute(str_sql, a_id=email).fetchall()
        if rows is not None and len(rows) >= 1:
                return False
        else:
                return True

def is_unique_user(user):
        str_sql = text("""select artist.username
                     from artist
                     where artist.username = :a_id""")
        rows = conn.execute(str_sql, a_id=user).fetchall()
        if rows is not None and len(rows) >= 1:
                return False
        else:
                return True
 
#App routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.fullname.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/profile')
def profile():
    #member3 = get_artist_from_id(7)
    #print(member3)
    member = ["John", "hey, I'm John- a pianist", "Johnpianio13", "Joe Shmo", "Jazz", "Piano", "youtube_link"]
    member2 = ["James", "hey, I'm James- a guitarist", "James231", "Joe Shmo", "Jazz", "Guitar", "https://www.youtube.com/embed/Zg5fmnrRzbg"]
    member4 = ['Lukas', 'Im a CS student using CockRoachDB!', 'Lukas123', 'Lukas Band', 'Country', 'Piano', 'https://www.youtube.com/embed/COnYtI6VP4A']
    return render_template('profile.html', member=member2)




@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #if form.validate_on_submit():
       # if form.username.data #if found in database
          #  return redirect(url_for('home'))
        #else:
         #   flash('Login Unsuccessful. Please check username or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/createBand", methods=['GET', 'POST'])
def createBand():
    form = BandForm()
    if form.validate_on_submit():
        flash(f'Band created for {form.fullname.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('createBand.html', title='Band Form', form=form)


if __name__ == '__main__':
    app.run(debug=1)
