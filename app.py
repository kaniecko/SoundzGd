from flask import Flask, render_template

app = Flask(__name__)


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
