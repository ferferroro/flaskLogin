from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

# instantiate the app
app =  Flask(__name__)

# app config
app.config['SECRET_KEY'] = 'sekreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate db
db = SQLAlchemy(app)

# instantiate and initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# create form
class loginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')

# create model class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

# user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# index route
@app.route('/', methods=['GET', 'POST'])
def index():
    form = loginForm()
    if request.method == 'GET':
        return render_template('index.html', form=form)
        
    if request.method == 'POST':

        if user := User.query.filter(User.username==form.username.data, User.password==form.password.data).first():
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash(u'Something went wrong!', 'alert alert-danger')
            return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)