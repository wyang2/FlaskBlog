from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog import app, db, bcrypt, mail
from flask_mail import Message
from flask_login import current_user
import secrets,os
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created')
        return redirect(url_for('home'))
    return render_template('create_post.html', title = 'New Post', form=form)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title = post.title, post = post)

@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit(): #Deal with post method
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully','success')
        return redirect(url_for('post',post_id = post.id))
    elif request.method == 'GET': #Deal with get method
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title = 'Update Post', form = form, legend = 'Update Post')

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted successfully','success')
    return redirect(url_for('home'))

@app.route('/post/<string:username>')
def user_posts(username):
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user).order_by(Post.date.desc()).paginate(page=page, per_page = 5)
    return render_template('user_posts.html', user=user, posts=posts)

def send_request_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='w.yangcanada@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
     {url_for('reset_token', token = token, _external = True)}
     '''
    mail.send(msg)

@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home.html'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_request_email(user)
        flash('A validation email has been sent to you', 'success')
        return redirect(url_for('login.html'))
    return render_template('reset_request.html',title = 'Reset Password', form = form)

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated():
        return redirect(url_for('home.html'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = RequestPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #its now a string rather than binary type
        db.session.commit()
        flash('Your password has been successfully reset','success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title = 'Reset Password', form = form)




