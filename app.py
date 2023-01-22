from flask import Flask, render_template, flash, redirect, url_for, session
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine, text
from sqlalchemy import insert
from sqlalchemy import delete
from sqlalchemy import update
from sqlalchemy import select
from forms import RegistrationForm, LoginForm, BandForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'irEALLYdONTkNOWwHATiAMdOING'


meta = MetaData()
DATABASE_URL = DATABASE_URL = "postgresql://postgres:getinhere123@database-1.cwkdawbglnge.us-east-1.rds.amazonaws.com:5432/theactualdatabase12378"
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

def is_user_exists(user):
        str_sql = text("""select artist.username
                     from artist
                     where artist.username = :a_id""")
        rows = conn.execute(str_sql, a_id=user).fetchall()
        if len(rows) >= 1:
                return True
        else:
                return False

def validate_password(user, passw):
        str_sql = text("""select artist.artist_id
                     from artist
                     where artist.username = :a_id and artist.password = :a_password""")
        rows = conn.execute(str_sql, a_id=user, a_password=passw).fetchone()
        if rows is not None:
                return rows[0]
        else:
                return None

def is_bandname_unique(b_name):
        str_sql = text("""select band.band_name
                     from band
                     where band.band_name = :name""")
        rows = conn.execute(str_sql, name=b_name).fetchall()
        if len(rows) >= 1:
                return False
        else:
                return True
         

def get_new_artist_id():
        str_sql = text("""select count(artist.artist_id)
                     from artist""")
        row = conn.execute(str_sql).fetchone()
        new_artist_id = row[0]
        while is_artist(new_artist_id):
                new_artist_id+=1
        return new_artist_id



def update_artist_bio(id, bio):
        if is_artist(id) == False:
                return False
        else:
                stmt = (
                        update(artist).
                        where(artist.c.artist_id == id).
                        values(artist_bio=bio)
                )
                conn.execute(stmt)
                return True

def is_band(id):
        str_sql = text("""select band.band_id
                     from band
                     where band.band_id = :b_id""")
        rows = conn.execute(str_sql, b_id=id).fetchall()
        if len(rows) == 0:
                return False
        else:
                return True

def update_band_bio(id, bio):
        if is_band(id) == False:
                return False
        else:
                stmt = (
                        update(band).
                        where(band.c.band_id == id).
                        values(band_bio=bio)
                )
                conn.execute(stmt)
                return True

def get_new_band_id():
        str_sql = text("""select count(band.band_id)
                     from band""")
        row = conn.execute(str_sql).fetchone()
        new_band_id = row[0]
        while is_band(new_band_id):
                new_band_id+=1
        return new_band_id


def get_band_members(id):
        if is_band(id) == False:
                return None
        str_sql = text("""select artist.username, instrument.instrument_name, artist.youtube_link, artist.band_lead
                        from artist
                        join instrument on instrument.instrument_id = artist.instrument_id
                        where artist.band_id = :b_id""")
        rows = conn.execute(str_sql, b_id=id).fetchall()
        band_members = []
        for row in rows:
                member_info = []
                member_info.append(row[0])
                member_info.append(row[1])
                member_info.append(row[2])
                member_info.append(row[3])
                band_members.append(member_info)
        return band_members

def get_band_info(id):
        if is_band(id) == False:
                return None
        str_sql = text("""select band.band_name, band.band_bio, genre.genre_name, song.song_name
                        from band
                        join genre on genre.genre_id = band.genre_id
                        join song on song.song_id = band.song_id
                        where band.band_id = :b_id""")
        row = conn.execute(str_sql, b_id=id).fetchone()
        info = []
        info.append(row[0])
        info.append(row[1])
        info.append(row[2])
        info.append(row[3])
        return info
        
def username_to_artist_id(user):
        str_sql = text("""select artist.artist_id
                        from artist
                        where username = :u
                        """)
        row = conn.execute(str_sql, u=user).fetchone()
        return row[0]

def bandname_to_band_id(b_name):
        str_sql = text("""select band.band_id
                        from band
                        where band_name = :name
                        """)
        row = conn.execute(str_sql, name=b_name).fetchone()
        return row[0]


#App routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #def create_artist(id, name, bio, user, passw, yt_link, a_email, g_id, is_band_lead, b_id, i_id)
        newID = get_new_artist_id()
        create_artist(newID, form.fullname.data, "", form.username.data, form.password.data, "", form.email.data, "", form.genre.data, 0, 0, form.instrument.data)
        flash(f'Account created for {form.fullname.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/profile')
def profile():
    member = ["John", "hey, I'm John- a pianist", "Johnpianio13", "Joe Shmo", "Jazz", "Piano", "youtube_link"]
    member2 = ["James", "hey, I'm James- a guitarist", "James231", "Joe Shmo", "Jazz", "Guitar", "https://www.youtube.com/embed/Zg5fmnrRzbg"]
    member4 = ['Lukas', 'Im a CS student using CockRoachDB!', 'Lukas123', 'Lukas Band', 'Country', 'Piano', 'https://www.youtube.com/embed/COnYtI6VP4A']
    
    if "userid" in session:
        user = session["userid"]
        m = get_artist_from_id(user)
        return render_template('profile.html', member=m)
    else:
        return redirect(url_for("login"))

@app.route('/band/')
def band():
    band_info = ["James", "hey, I'm James- a guitarist", "James231", "Joe Shmo", "Jazz", "Guitar",
               "https://www.youtube.com/embed/Zg5fmnrRzbg"]
    band_members = get_band_members(1)
    print(band_members)
    return render_template('band.html', band_info=band_info, band_members=band_members)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    upass = form.password.data

    if(is_user_exists(username)):
        id = validate_password(username, upass)
        if(id != None):
            session["userid"] = id
            return redirect(url_for("profile")) 
        else:  
            return render_template('login.html', title='Login', form=form)
    else:
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
