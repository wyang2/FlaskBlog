from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
    'author': 'Big Flower Cat',
    'title': 'catch mouse',
    'content':'How to catch mouse',
    'date_posted': 'May 17, 2019',
    },
    {
    'author': 'Big Flower Cat',
    'title': 'catch mouse',
    'content':'How to catch mouse',
    'date_posted': 'May 17, 2019',
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm() #Create an instance of the form that will send to application
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #its now a string rather than binary type
        user = User(username=form.username.data, email=form.email.data, password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created successfully!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm() #Create an instance of the form that will send to application
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(url_for('account')) if next_page else redirect(url_for('home'))
        else:
            flash('Wrong email or password please try again')
    return render_template('login.html',title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html',title="Account")

