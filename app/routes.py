from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import RegistrationForm
from app.models import User

@app.route('/')
def index():
    return  render_template('index.html')

@app.route('/categories')
def categories():
    return 'Browse Categories'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations {}, you are now a registered user!'.format(user.username))
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)
