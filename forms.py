
from operator import length_hint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20), Regexp(r'^[\w.@+-]+$')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    genre = RadioField('Genre', choices=[('1','N/A'),('2','Country'),('3','EDM/Dance'),('4','Pop'),('5','Rock'),('6','Classical'),('7','R&B')])
    instrument = RadioField('Instrument', choices=[('1','Piano'),('2','Guitar'),('3','Drums'),('4','Vocals'),('5','Saxophone'),('6','Trumpet'),('7','Bass')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
  

class BandForm(FlaskForm):
    bandName = StringField('Band Name', validators=[DataRequired(), Length(min=2, max=250)])
    bandBio = StringField('Band Bio', validators=[DataRequired(), Length(min=2, max=250)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=2, max=250)])
    song = StringField('Song Name', validators=[DataRequired(), Length(min=2, max=250)])
    submit = SubmitField('Create Band')