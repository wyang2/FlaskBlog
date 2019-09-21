from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app

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
    form = RegistrationForm() #Create an instance of the form that will send to application
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm() #Create an instance of the form that will send to application
    if form.validate_on_submit():

        return render_template('login.html', title='Login', form=form)
    return render_template('login.html',title='Login', form=form)