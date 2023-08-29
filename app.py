from flask import Flask, render_template, redirect, flash, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_ckeditor import CKEditor

from datetime import datetime as dt
from forms import LoginForm, SignupForm, PostForm, UserForm, SearchForm

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECREK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable = False)
    name = db.Column(db.String(80), nullable = False)
    bio = db.Column(db.String(120), nullable=True)
    img_url = db.Column(db.String(400), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(200), nullable=False)
    date_joined = db.Column(db.DateTime, default=dt.now())

    posts = db.relationship('Post', backref='poster')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable = False)
    content = db.Column(db.Text)
    img_url = db.Column(db.String(400), nullable=False)
    # author = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.DateTime, default=dt.now())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/search', methods=['GET', 'POST'])
def get_search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        post_searched = form.searched.data
        # query db
        posts = posts.filter(Post.content.like('%' + post_searched + '%') | 
                            Post.title.like('%' + post_searched + '%'))
        posts = posts.order_by(Post.date_posted.desc()).all()
    

        return render_template('search.html', 
                               form=form, 
                               searched = post_searched,
                               posts=posts
                            )



@app.route('/profile/settings/<int:id>', methods=['GET', 'POST'])
@login_required
def profile_settings(id):
    profile_to_update = User.query.get_or_404(id)
    form = UserForm(
        obj = profile_to_update
    )
    if request.method == 'POST':
        profile_to_update.name = request.form['name']
        profile_to_update.username = request.form['username']
        profile_to_update.bio = request.form['bio']


        if request.form['img_url'] == '':
            profile_to_update.img_url = profile_to_update.img_url
        else:
            profile_to_update.img_url = request.form['img_url']


        try:
            db.session.commit()
            return redirect(url_for("profile", id=profile_to_update.id))
        except:
            flash('You have done something wrong. Try again!')
    return render_template('settings.html', form=form)


@app.route('/profile/<path:id>')
@login_required
def profile(id):
    user = User.query.get(id)
    print(user)
    return render_template('profile.html', user=user)

#------------ ROUTES ---------------#
@app.route('/delete/<int:id>')
def delete_post(id):
    post = Post.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()

        flash('Post has been deleted!')

        posts = Post.query.order_by(Post.date_posted.desc())
        return render_template('index.html', posts=posts)
    except:
        flash('Something went wrong. Try again!')



@app.route('/show_post/edit/<int:id>', methods=['GET', "POST"])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(
        obj=post
    )
    if form.validate_on_submit():
        post.title= form.title.data
        post.content = form.content.data
        post.img_url = form.img_url.data

        try:
            db.session.commit()
            return redirect(url_for("show_post", id=post.id))
        except:
            flash('Something went wrong!')
    return render_template('edit-post.html', form=form)

@app.route('/show_post/<int:id>')
def show_post(id):
    post = Post.query.get_or_404(id)
    return render_template('show-post.html', post=post)

@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        new_post = Post(
            title = form.title.data,
            content = form.content.data,
            img_url = form.img_url.data,
            author_id = poster
            
    )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('profile', id=current_user))
   
    return render_template('create-post.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        new_user = User.query.filter_by(email=form.email.data).first()
        if new_user is None:
            if form.password.data == form.password2.data:

                hash_password = generate_password_hash(form.password.data)
                
                new_user = User(
                    email = form.email.data,
                    password = hash_password,
                    name = form.name.data,
                    username = form.username.data,
                )
                
                db.session.add(new_user)
                db.session.commit()
                flash('Signed Up successfully! Time to Log In')
                return redirect('login')
            else:
                flash('Passwords must match!')
        else:
            flash('An account is already registered with your email')
        form.name.data = ''
        form.email.data = ''
        form.username.data = ''
        form.password.data = ''
        form.password2.data = ''
        

    return render_template('signup.html', form=form)
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('profile', id=user.id))
            else:
                flash('Wrong password')
        else:
            flash('That user doesn`t exist')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!")
    return redirect(url_for('login'))

@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)