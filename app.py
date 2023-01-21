from flask import Flask, render_template
from sqlalchemy import create_engine, text
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import select
from sqlalchemy import Table, Column, Integer, String, MetaData

app = Flask(__name__)

meta = MetaData()
DATABASE_URL = "cockroachdb://lukas:8S5jNP4SEeQyNThMB2xPvA@ninth-warrior-8275.7tt.cockroachlabs.cloud:26257/SoundzGd?sslmode=verify-full"
engine = create_engine(DATABASE_URL)
conn = engine.connect()
artist = Table(
   'artist', meta,
   Column('artist_id', Integer, primary_key = True, nullable=False),
   Column('artist_name', String, nullable=False),
   Column('artist_bio', String(250), nullable=False),
   Column('username', String, nullable=False),
   Column('password', String, nullable=False),
   Column('youtube_link', String, nullable=False),
   Column('email', String, nullable=False),
   Column('genre_id', Integer, nullable=False),
   Column('band_lead', Integer, nullable=False),
   Column('band_id', Integer, nullable=False),
)
band = Table(
   'band', meta,
   Column('band_id', Integer, primary_key = True, nullable=False),
   Column('band_name', String, nullable=False),
   Column('band_bio', String(250), nullable=False),
   Column('genre_id', Integer, nullable=False),
   Column('song_id ', Integer, nullable=False),
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
def create_artist(id, name, bio, user, passw, yt_link, a_email, g_id, is_band_lead, b_id):
        stmt = (
                insert(artist).
                values(artist_id=id, artist_name=name, artist_bio=bio, username=user, password=passw, youtube_link=yt_link, email=a_email, genre_id=g_id, band_lead=is_band_lead, band_id=b_id)
        )
        conn.execute(stmt)

def get_all_artists():
        select_command = artist.select()
        rows = conn.execute(select_command)
        return rows

def is_artist(id):
        query = artist.select().where(artist.c.artist_id==id)
        rows = conn.execute(query).fetchall()
        if len(rows) == 0:
                return False
        else:
                return True

#App routes

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run()
