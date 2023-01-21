from flask import Flask, render_template, flash, redirect, url_for
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from forms import RegistrationForm, LoginForm, BandForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'irEALLYdONTkNOWwHATiAMdOING'


#class User(db.Model, UserMixin):
 #   id = db.Column(db.Integer, primary_key=True)
  #  username = db.Column(db.String(20), nullable=False, unique=True)
   # password = db.Column(db.String(80), nullable=False)



@app.route('/home')
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.fullname.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)



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