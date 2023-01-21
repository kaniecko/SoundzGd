from operator import length_hint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', validators=[DataRequired(), Email()])

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